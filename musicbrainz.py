import sqlite3
import requests
import re
import random
import time

from datetime import datetime
from bs4 import BeautifulSoup

def setup_database():
    conn = sqlite3.connect("songs.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artist_name TEXT,
        song_title TEXT,
        release_year TEXT
    )
    """)
    conn.commit()
    return conn

#standardize to year only
def process_release_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").year
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y").year
        except ValueError:
            return "N/A"

def fetch_song_data(artist_name, song_title):
    base_url = "https://musicbrainz.org/ws/2/recording/"
    params = {
        "query": f'artist:"{artist_name}" AND recording:"{song_title}"',
        "fmt": "json"
    }
    headers = {"User-Agent": "MusicDataCollector/1.0 (user@example.com)"}
    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "recordings" in data and data["recordings"]:
            #sort by first release date (handles multiple recordings)
            sorted_recordings = sorted(data["recordings"], key=lambda x: x.get("first-release-date", "9999-99-99"))
            first_recording = sorted_recordings[0]
            release_date = first_recording.get("first-release-date", "Unknown")
            return process_release_date(release_date)
    return "N/A"

def insert_into_database(conn, artist_name, song_title, release_year):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO songs (artist_name, song_title, release_year)
    VALUES (?, ?, ?)
    """, (artist_name, song_title, release_year))
    conn.commit()

def read_songs_from_file(file_path):
    songs = []
    with open(file_path, 'r') as file:
        for line in file:
            if " - " in line:
                artist_name, song_title = line.strip().split(" - ", 1)
                songs.append({"artist_name": artist_name, "song_title": song_title})
    return songs

#ZACK - Profanity Counter ####################################################################################################################
def song_profanity(artist, song, profanity_list):
    artist_stripped = re.sub(r'[^\w]', '', artist).lower()
    #print(artist_stripped)
    song_stripped = re.sub(r'[^\w]', '', song).lower()
    #print(song_stripped)
    url = f"https://www.azlyrics.com/lyrics/{artist_stripped}/{song_stripped}.html"


    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    song_tag = soup.find("b", string=f'"{song}"')
    if song_tag is None:
        song_tag = soup.find("b", string=f'"{song.lower()}"')
        if song_tag is None:
            return "Error"

    lyrics_div = song_tag.find_next("div")
    if lyrics_div is None:
        return "Error"

    lyrics = lyrics_div.get_text().strip()
    words_in_lyrics = re.findall(r'\b\w+\b', lyrics.lower())

    num_profane_words = 0
    for word in words_in_lyrics:
        for profane_word in profanity_list:
            if profane_word in word:
                num_profane_words += 1

    return f"{song} - {num_profane_words}"


def song_list_profanity(file_path, profanity_list):
    song_list = read_songs_from_file(file_path)
    results = []

    for song in song_list:
        time.sleep(random.uniform(1, 5))

        indv_prof = song_profanity(song["artist_name"], song["song_title"], profanity_list)
        print(indv_prof)
        results.append(indv_prof)

    return results



def main():
    print("Code Running...")
    profanity_list = ['bitch', 'fuck', "fuckin'", "shit", "motherfuckin'", "ass", "pussy"]
    file_path = "songs.txt"

    print("Zack - Profanity Counter")
    print("########################")

    song_list_profanity(file_path, profanity_list)
    

    '''
    #Nathaniel - Release Dates
    songs = read_songs_from_file("songs.txt") 
    conn = setup_database()
    for song in songs:ch
        artist_name = song["artist_name"]
        song_title = song["song_title"]
        print(f"Fetching data for {artist_name} - {song_title}...")
        release_year = fetch_song_data(artist_name, song_title)
        print(f"Found: Release Year: {release_year}")
        insert_into_database(conn, artist_name, song_title, release_year)
        time.sleep(1)  #musicbrainz rate limits
    conn.close()
    '''

if __name__ == "__main__":
    main()
