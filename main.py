import numpy
import matplotlib
from bs4 import BeautifulSoup
import requests
import re



#Profanity - Zack. Using @Genius.com
#Client ID - QozXjR8XK7UsT-1NbCj0fv3TUqv4mXrM5eyxiuLzAtX0qMpl-wPY81HiwZnToM-i
#Client access token - 2O5_mc8TLGMFJDuMwx1Qv-PrIiEQlEe2Ar2cwQJN6CLMTjn_5dYgB5A4tFSPkEAg
def search_song(title, artist, access_token):
    url = 'https://api.genius.com'
    headers = {'Authorization': f'Bearer {access_token}'}
    search_url = f'{url}/search'
    data = {'q': f'{title} {artist}'}
    response = requests.get(search_url, headers=headers, params=data)
    return response.json()

def scrape_lyrics(response):
    url_list = []
    for song_urls in response["response"]["hits"]:
        url_list.append(song_urls["result"]["url"])
    final_url = url_list[0]
    page = requests.get("https://web.archive.org/web/20241129124550/"+final_url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.findAll('span', class_='ReferentFragmentdesktop__Highlight-sc-110r0d9-1 jAzSMw')
    cleaned_lyric_list = [entry.get_text() for entry in lyrics]

    '''
    for lyric in cleaned_lyric_list:
        print(lyric)
    '''

    return cleaned_lyric_list

def count_bad_words(lyric_list, profane_words):
    num_words = 0
    # Normalize profane words for case-insensitive comparison
    profane_words_set = set(word.lower() for word in profane_words)
    for line in lyric_list:
        # Split the line into words, normalize them, and count matches
        words = line.lower().split()  # Convert to lowercase and split into words
        for word in words:
            # Remove punctuation from each word and check if it's profane
            cleaned_word = word.strip(".,!?;:()\"'")
            if cleaned_word in profane_words_set:
                num_words += 1
    return num_words


def main():
    print("Code Running...")
    song_json_resp = search_song("Lose Yourself", "Eminem", "smlHU9ET3K7s2NNWxrbGIaXCMteaYs7IZ2jLL8mFJot0jE4X78jPaNlz_uDVeWFH")
    #print(song_json_resp)
    #print(scrape_lyrics(song_json_resp))
    profane_words = ['damn', 'hell', 'crap', 'piss', 'ass', 'bastard', 'fuck', 'shit', 'dick', 'pussy']
    scraped_lyrics = scrape_lyrics(song_json_resp)
    print(count_bad_words(scraped_lyrics, profane_words))

if __name__ == "__main__":
    main()
