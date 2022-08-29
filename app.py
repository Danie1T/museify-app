from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from functions import create_spotify_oauth, get_token, format_songs, format_artists

app = Flask(__name__)
app.secret_key = "SECRET KEY"
app.config["SESSION_COOKIE_NAME"] = "Current Session"


@app.route("/")
def index():
    # Obtain authorization from user
    return render_template("index.html")


@app.route("/login")
def login():
    # Create an OAuth object and redirect to the Spotify authorization page
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/authorize")
def authorize():
    # Create an OAuth object
    sp_oauth = create_spotify_oauth()

    # Ensure that the session is clear before setting the new token
    session.clear()

    # Obtain the OAuth code and convert it to a usable token for this session
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info

    return redirect(url_for("menu", _external=True))


@app.route("/menu")
def menu():
    # Redirect to desired page
    if request.method == "POST":

        choice = request.form.get("option")

        if choice == "tracks":
            return redirect(url_for("top_tracks"))
        elif choice == "artists":
            return redirect(url_for("top_artists"))
        elif choice == "recommendations":
            return redirect(url_for("recommendations"))

    # Render menu page
    return render_template("menu.html")


@app.route("/top-tracks")
def top_tracks():
    # Obtain the top tracks for different time frames and render the template to display it
    try:
        token_info = get_token()
    except:
        return redirect("/")

    sp = spotipy.Spotify(auth=token_info["access_token"])

    top_songs_short = sp.current_user_top_tracks(  # 4 weeks
        limit=30,
        offset=0,
        time_range="short_term"
    )

    top_songs_medium = sp.current_user_top_tracks(  # 6 months
        limit=30,
        offset=0,
        time_range="medium_term"
    )

    top_songs_long = sp.current_user_top_tracks(  # All time
        limit=30,
        offset=0,
        time_range="long_term"
    )

    short = format_songs(top_songs_short, "items")
    medium = format_songs(top_songs_medium, "items")
    long = format_songs(top_songs_long, "items")

    return render_template("top-tracks.html", short=short, medium=medium, long=long)


@app.route("/top-artists")
def top_artists():
    # Obtain the top artists for different time frames and render the template to display it
    try:
        token_info = get_token()
    except:
        return redirect("/")

    sp = spotipy.Spotify(auth=token_info["access_token"])

    top_artists_short = sp.current_user_top_artists(  # 4 weeks
        limit=30,
        offset=0,
        time_range="short_term"
    )

    top_artists_medium = sp.current_user_top_artists(  # 6 months
        limit=30,
        offset=0,
        time_range="medium_term"
    )

    top_artists_long = sp.current_user_top_artists(  # 4 weeks
        limit=30,
        offset=0,
        time_range="long_term"
    )

    short = format_artists(top_artists_short, "items")
    medium = format_artists(top_artists_medium, "items")
    long = format_artists(top_artists_long, "items")

    user = sp.current_user()

    print (user)

    return render_template("top-artists.html", short=short, medium=medium, long=long)


@app.route("/get-recommendations", methods=["GET", "POST"])
def get_recommendations():

    # if get: put the url list thing, do only one songs for now, then try to add more thru js
    # if post: send the urls, get the songs, then render the new page

    if request.method == "POST":

        try:
            token_info = get_token()
        except:
            return redirect("/")

        sp = spotipy.Spotify(auth=token_info["access_token"])

        url = request.form.get("url")
        if not url:
            return "invalid url"

        url = [url]

        get_recommendations = sp.recommendations(
            seed_tracks=url,
            limit=30
        )

        print (get_recommendations)

        format_recs = format_songs(get_recommendations, "tracks")

        this_user = sp.current_user()
        playlist = sp.user_playlist_create(
            user=this_user["id"],
            name="Museify",
            public=True,
            collaborative=False,
            description="Curated by Museify @ link"
        )

        uris = []
        for i in get_recommendations["tracks"]:
            uris.append(i["uri"])

        sp.user_playlist_add_tracks(
            user=this_user["id"],
            playlist_id=playlist["id"],
            tracks=uris,
            position=None)

        return render_template("show-recommendations.html", songs=format_recs)

    return render_template("get-recommendations.html")
