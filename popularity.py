import requests
import sqlite3

API_KEY = "f7d0e8e04446da906c47fd70f8e7029c"
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

# Setup SQLite database
def setup_database():
    conn = sqlite3.connect("lastfm_songs.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artist_name TEXT,
        song_title TEXT,
        popularity INTEGER,
        genres TEXT
    )
    """)
    conn.commit()
    return conn

# Fetch data from Last.fm API
def fetch_lastfm_data(artist_name, song_title):
    params = {
        "method": "track.getInfo",
        "artist": artist_name,
        "track": song_title,
        "api_key": API_KEY,
        "format": "json"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if "track" in data:
            track_info = data["track"]
            popularity = int(track_info.get("playcount", 0))  # Scrobble count
            genres = [tag["name"] for tag in track_info.get("toptags", {}).get("tag", [])]
            return {
                "artist_name": artist_name,
                "song_title": song_title,
                "popularity": popularity,
                "genres": ", ".join(genres) if genres else "Unknown"
            }
    return None

# Insert song data into the database
def insert_into_database(conn, song_data):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO songs (artist_name, song_title, popularity, genres)
    VALUES (?, ?, ?, ?)
    """, (song_data["artist_name"], song_data["song_title"],
          song_data["popularity"], song_data["genres"]))
    conn.commit()

# Read songs from a file
def read_songs_from_file(file_path):
    songs = []
    with open(file_path, 'r') as file:
        for line in file:
            if " - " in line:
                artist_name, song_title = line.strip().split(" - ", 1)
                songs.append({"artist_name": artist_name, "song_title": song_title})
    return songs

# Main function
def main():
    conn = setup_database()
    songs = read_songs_from_file("songs.txt")  # File with "Artist - Song" per line

    for song in songs:
        data = fetch_lastfm_data(song["artist_name"], song["song_title"])
        if data:
            insert_into_database(conn, data)
            print(f"Inserted: {data}")
        else:
            print(f"Could not fetch data for: {song['artist_name']} - {song['song_title']}")

    print("Data successfully stored in the database.")
    conn.close()

if __name__ == "__main__":
    main()