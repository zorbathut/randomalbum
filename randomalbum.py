# shows a user's playlists (need to be authenticated via oauth)

import sys
import os
import spotipy
import spotipy.util as util
import spotify_keys

def show_tracks(results):
	for i, item in enumerate(tracks['items']):
		track = item['track']
		print("   %d %32.32s %s" % (i, track['artists'][0]['name'].encode("utf-8"), track['name'].encode("utf-8")))


if __name__ == '__main__':
	if len(sys.argv) > 1:
		username = sys.argv[1]
	else:
		print("Whoops, need your username!")
		print("usage: python user_playlists.py [username]")
		sys.exit()

	token = util.prompt_for_user_token(username, "playlist-read-private playlist-modify-private", spotify_keys.client_id, spotify_keys.client_secret, "http://localhost:8888/callback")

	if token:
		sp = spotipy.Spotify(auth=token)
		playlists = sp.user_playlists(username)
		for playlist in playlists['items']:
			if playlist['owner']['id'] == username:
				print()
				print(playlist['name'].encode("utf-8"))
				print('  total tracks', playlist['tracks']['total'])
				results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
				tracks = results['tracks']
				show_tracks(tracks)
				while tracks['next']:
					tracks = sp.next(tracks)
					show_tracks(tracks)
	else:
		print("Can't get token for", username)