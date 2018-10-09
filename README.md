So I was all, "hey, I want to play entire albums, but play them in a random order! That would be neat!" And I sat down to learn the Spotify API and I made this little test program and then I just forgot about it for like two years, but, I mean, shit happens.

I finally remembered it and said "I bet I could whip this up in like three hours, I mean, my test program worked and all, this'll be easy, maybe I'll even put it up on /r/spotify or something, that probably exists, that'd be neat", so I came home and petted my cat a bunch and then sat down to the documentation and realized that spotipy doesn't recognize folders as things.

Like.

Let that sink in.

Folders don't exist. You cannot recognize them using the Spotify official API.

This isn't a thing I concluded after study, this is a thing they [straight-up said](https://github.com/spotify/web-api/issues/38). Apparently folders don't have IDs so they can't expose them. I mean, I'm looking at them in the client, they clearly are a thing, you know how you can expose folders? *With whatever system the client uses to recognize them. Come on, people. This is not rocket science.*

My original plan was that I'd ask people to choose a folder and it would generate a big playlist of random albums from within that folder, like, that sounded pretty cool to me. But now I need to . . . hack the Spotify protocol? I found a thing that tries to hook into the console client protocol and it was buggy and nearly wiped out all my playlists I think, so, yeah, I'm not touchin' that. Or I could set up this big interface so people can choose the playlists they want.

So tl;dr fuck this whole idea.

This package makes a big list of your albums in cache.yaml as a dictionary. If they're filtered out, the value is true. If they're not, the value is false. I probably should have done that the other way around. I checked in my album list because I frankly suspect nobody besides me is ever going to look at this and I don't want to lose that.

Consider this an example of how to use spotipy as well as an example of why not to use spotipy.

Look on my works, ye Mighty, and despair.

----

I guess this is dual-licensed under MIT and Unlicense because that's the thing I've been doing lately.

----

Edit: I don't know why Github decided to use exploding camel emojis for the .gitattributes. I frankly suspect this repository is cursed. Gonna go see if there's a slab I need to return, brb
