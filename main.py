import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID_SPOTIFY = os.getenv("CLIENT_ID")
CLIENT_SECRET_SPOTIFY = os.getenv("CLIENT_SECRET")
URL_REDIRECT = "http://example.com"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private", redirect_uri=URL_REDIRECT,
                     client_id=CLIENT_ID_SPOTIFY, client_secret=CLIENT_SECRET_SPOTIFY, show_dialog=True, cache_path="token.txt"))

user_id = sp.current_user().get("id")

date = input(
    "Which date do you want to travel to? Type the date in this format YYYY-MM-DD: ")

year = date.split("-")[0]

response = requests.get(
    f"https://www.billboard.com/charts/hot-100/{date}")
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")
song_tags = soup.select(
    selector="li .c-title", id="title-of-a-story")
song_titles = [song.getText().strip() for song in song_tags]

song_uris = []

for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        # print(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# print(user_id)
playlist = sp.user_playlist_create(
    user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
