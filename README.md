# Museify
#### Video Demo:  <https://youtu.be/SZPktPKVwQU>
#### Description:

Museify is an app created for Harvard University's online CS50x final assignment. It's purpose is to cleanly display any Spotify user's top tracks and artists along with the ability to create a playlist with song recommendations based on a provided song URL.

The app utilizes the following tools:
- Python
- Flask
- HTML
- CSS
- Javascript
- Spotify API
- Spotipy Library

In order to access user Spotify information, OAuth was used in accordance Spotify's regulations through Spotipy's Authorization Code Flow. Upon opening the app through the index.html file, the user is redirected to the Spotify website and prompted to authorize Museify to access and alter their Spotify data. Once authorization is provided, a token is provided to Museify by Spotify, allowing the app to access API data regarding the user.

There are three main funtionalities in Museify: Obtaining top tracks, top artists, and providing song recommendations.

The methods of obtaining and displaying a user's top tracks and top artists are similar. Using Spotipy's functions, Museify calls on Spotify's API to obtain the stored information for both tracks and artists. This is done three seperate times for both the tracks and the users to gather information for three distinct time frames. From the large dictionaries returned by the API call, Museify slices them down to store only the required information. This information is then sent to the top-tracks.html and top-artists.html files where they are neatly rendered.

In order to provide song recommendations, the user is prompted to input a Spotify song URL. Using another Spotipy function, Museify accesses Spotify's API to determine a list of songs that contain features similar to those of the provided song. Upon obtaining these songs, Museify creates a playlist containing all of these songs named _Museify_ in the user's library. Museify then splices down the dictionary containing the song information in order to store only the needed information for displaying. It is them sent to show-recommendations.html where each song is neatly rendered.

This project was difficult but fulfilling and provided me with new learning that is very transferable. Having to learn OAuth and understanding how to utilize Spotipy to create calls on the Spotify API was new information for me and required a lot of self-learning. While difficult, I was successful in implementing all of these concepts and I am extremely satisfied with the result.