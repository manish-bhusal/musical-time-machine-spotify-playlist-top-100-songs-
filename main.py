import requests
from bs4 import BeautifulSoup

year = input(
    "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(
    f"https://www.billboard.com/charts/hot-100/{year}")
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")
song_tags = soup.select(
    selector="li .c-title", id="title-of-a-story")
song_titles = [song.getText().strip() for song in song_tags]
print(song_titles)
