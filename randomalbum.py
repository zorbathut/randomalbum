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
		cache = yaml.load(f)
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
	if len(sys.argv) > 1:
		username = sys.argv[1]
	else:
		print("Whoops, need your username!")
		print("usage: python user_playlists.py [username]")
		sys.exit()

	token = util.prompt_for_user_token(username, "playlist-read-private playlist-modify-private",
	                                   spotify_keys.client_id, spotify_keys.client_secret, "http://localhost:8888/callback")

	if token:
		sp = spotipy.Spotify(auth=token)
		playlists = get_all_playlists(sp, username)
		print(f'found {len(playlists)} playlists')

		trackery = []

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
				deeztracks += tracks['items']
				show_tracks(tracks)
			trackery += [deeztracks]

		random.shuffle(trackery)
		flattrack = [track for album in trackery for track in album]

		pp = pprint.PrettyPrinter(indent=4)

		print("Creating . . .")
		pigl = sp.user_playlist_create(username, "Shuffle!", public=False)
		for offset in range(0, len(flattrack), 50):
			sp.user_playlist_add_tracks(username, pigl['id'], [
			                            track['track']['id'] for track in flattrack[offset:offset+50]])
	else:
		print("Can't get token for", username)

with atomic_write('cache.yaml', overwrite=True) as f:
	yaml.dump(cache, f)
