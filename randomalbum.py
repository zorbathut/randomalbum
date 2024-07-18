# shows a user's playlists (need to be authenticated via oauth)

import sys
import os
import pprint
import random
import spotipy
import spotipy.util as util
import spotify_keys
import yaml

from atomicwrites import atomic_write

try:
	with open('cache.yaml', 'r') as f:
		cache = yaml.safe_load(f)
except IOError:
	cache = {}


def show_tracks(results):
	for i, item in enumerate(tracks['items']):
		track = item['track']
		print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))


def get_all_playlists(sp, username):
	accum = []
	offset = 0
	while True:
		chunk = sp.user_playlists(username, limit=50, offset=offset)
		items = chunk['items']
		accum += items
		offset += len(items)
		if len(items) < 50:
			break
	return accum


if __name__ == '__main__':
	username = spotify_keys.username
	token = util.prompt_for_user_token(username, "playlist-read-private playlist-modify-private",
	                                   spotify_keys.client_id, spotify_keys.client_secret, "http://localhost:8888/callback")

	if token:
		sp = spotipy.Spotify(auth=token)
		playlists = get_all_playlists(sp, username)
		print(f'found {len(playlists)} playlists')

		trackery = []
		artistry = {}
		albumry = {}

		for playlist in playlists:
			if playlist['owner']['id'] != username:
				continue

			if "Shuffle!" in playlist['name']:
				continue

			if playlist['name'] not in cache:
				cache[playlist['name']] = False

			if cache[playlist['name']]:
				continue

			if playlist['name'] == "Discover Weekly":
				continue

			print(playlist['name'])
			print('  total tracks', playlist['tracks']['total'])
			results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
			
			deeztracks = []
			tracks = results['tracks']
			deeztracks += tracks['items']
			show_tracks(tracks)
			while tracks['next']:
				tracks = sp.next(tracks)
				if 'items' in tracks:
					# this probably shouldn't ever fail, but right now it does on Toby Fox's Undertale album
					deeztracks += tracks['items']
					show_tracks(tracks)

			compiledtracks = [track['track']['id'] for track in deeztracks]
			trackery += [compiledtracks]
			artistry[deeztracks[0]['track']['artists'][0]['id']] = True
			albumry[deeztracks[0]['track']['album']['id']] = True
		
		for artist in artistry:
			albums = sp.artist_albums(artist, album_type="album", limit=50)
			albums = [album for album in albums['items'] if album['id'] not in albumry]
			
			if len(albums) == 0:
				continue

			chosenalbum = albums[random.randrange(len(albums))]
			
			print(f"Spicing it up with {chosenalbum['artists'][0]['name']} - {chosenalbum['name']}")
			albumdata = sp.album_tracks(chosenalbum['id'])
			albumtracks = [track['id'] for track in albumdata['items']]
			trackery += [albumtracks]

		random.shuffle(trackery)
		flattrack = [track for album in trackery for track in album]

		print("Creating . . .")
		pigl = sp.user_playlist_create(username, "Shuffle!", public=False)
		for offset in range(0, len(flattrack), 50):
			sp.user_playlist_add_tracks(username, pigl['id'], [
			                            track for track in flattrack[offset:offset+50]])
	else:
		print("Can't get token for", username)

with atomic_write('cache.yaml', overwrite=True) as f:
	yaml.dump(cache, f)
