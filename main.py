# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from dotenv import load_dotenv
import os
from flask import Flask, url_for, request, redirect,session
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
from downloadSongs import DownloadFromTitles

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'sdmp3 cookie'
TOKEN_INFO = "token_info"
load_dotenv()

_id = os.getenv("CLIENT_ID")
_secret = os.getenv("SECRET_KEY")
@app.route('/')
def index():
    spotify_oauth = create_spotify_oauth()
    auth_url = spotify_oauth.get_authorize_url()
    return redirect(auth_url)
@app.route('/redirect')
def redirectPage():
    spotifu_oauth = create_spotify_oauth()
    session.clear()
    access_code = request.args.get('code')
    token_info = spotifu_oauth.get_cached_token(access_code)
    session['TOKEN_INFO'] = token_info

    return redirect(url_for('getTracks', _external= True))
@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("User Not logged in")
        return redirect('/')

    token = spotipy.Spotify(auth=token_info['access_token'])
    playlistId = getPlaylist(token)

    names = list(playlistId.keys())
    for name in range(len(names)):
        print(f'{name} : {names[name]}')
    choice = int(input(''))
    play = playlistId[names[choice]]

    songs = []
    for song in token.playlist_items(play ,limit=50 ,offset=0):
        songs.append(song['track']['name'])

    DownloadFromTitles(songs)
    return "Completed Successfully"
def getPlaylist(token):

    playListId = {}
    for id in token.current_user_playlists(limit=50 ,offset=0)['items']:
        playListId[str(id['name'])] = str(id['id'])
        print(playListId[str(id['name'])])

    return playListId
def get_token():
    token_info = session.get(TOKEN_INFO ,None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_Expried = token_info['expires_at'] - now < 60
    if (is_Expried):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = '930ceceacc1e487c81539ec6004f40eb',
        client_secret = '47974613722a46b585d1c3f4d4e91348',
        redirect_uri = url_for('redirectPage',_external = True),
        scope = "user-library-read"
    )
if __name__ == '__main__':

    app.run(debug = False)