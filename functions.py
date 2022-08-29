from flask import Flask, url_for, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import config

CLIENT_ID = config.api_id
CLIENT_SECRET = config.api_secret

sp_scope = "playlist-modify-public, playlist-modify-private, user-library-read, user-top-read"

def create_spotify_oauth():
    # Return upon receiving Spotify authorization
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for("authorize", _external=True),
        scope=sp_scope)


def get_token():
    # Get token from session
    token_info = session.get("token_info", None)
    if not token_info:
        raise "exception"

    # If token expires within next 2 minutes, refresh it
    current_time = int(time.time())
    expiration = token_info["expires_at"] - current_time < 120
    if (expiration):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])

    return token_info


def format_songs(song_dict, key):
    post_songs = []

    for i in song_dict[key]:
        artists = []
        for j in i["artists"]:
            artists.append(j["name"])
        name = i["name"]
        image = i["album"]["images"][0]["url"]

        song = {"name": name, "artists": artists, "image": image}

        post_songs.append(song)

    return post_songs


def format_artists(artists_dict, key):
    post_artists = []

    for i in artists_dict[key]:
        name = i["name"]
        popularity = i["popularity"]
        image = i["images"][0]["url"]

        artist = {"name": name, "popularity": popularity, "image": image}

        post_artists.append(artist)

    return post_artists