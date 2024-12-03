import numpy
import matplotlib
from bs4 import BeautifulSoup
import requests



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

def scrape_lyrics(title,artist,access_token):
    response = search_song(title,artist, access_token)
    url_list = []
    for song_urls in response["response"]["hits"]:
        url_list.append(song_urls["result"]["url"])
    final_url = url_list[0]
    page = requests.get(final_url)
    html = BeautifulSoup(page.text, 'html.parser')
    print(html)
    #lyrics = html.find('div', class_='lyrics').get_text()
    #return lyrics

def main():
    print("Code Running...")
    scrape_lyrics("Lose Yourself", "Eminem", "2O5_mc8TLGMFJDuMwx1Qv-PrIiEQlEe2Ar2cwQJN6CLMTjn_5dYgB5A4tFSPkEAg")
    

if __name__ == "__main__":
    main()
