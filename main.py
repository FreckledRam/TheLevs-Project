import numpy
import matplotlib
from bs4 import BeautifulSoup
import requests
import re



#Profanity - Zack. Using @Genius.com
def name_to_lyrics(artist, song, profanity_list):
    url = f"https://www.azlyrics.com/lyrics/{artist.lower().replace(" ", "-")}/{song.lower().replace(" ", "")}.html"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        lyrics_div = soup.find("b", string=f'"{song}"').find_next("div")

        lyrics = lyrics_div.get_text().strip()
        
        words_in_lyrics = re.findall(r'\b\w+\b', lyrics.lower())  # Extract words, ignoring punctuation

        num_profane_words = 0
        for word in words_in_lyrics:
            for profane_word in profanity_list:
                # Check if the word matches any profane word exactly
                 if profane_word in word:
                    num_profane_words += 1
        return num_profane_words
        '''
        profane_words_found = [word for word in words_in_lyrics if word in profanity_list]

        # Print the results
        print (words_in_lyrics)
        print("Number of profane words found:", len(profane_words_found))  
        '''

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


def main():
    song_name = "Lose Yourself"
    artist = "Eminem"

    print("Code Running...")
    profanity = ['bitch', 'fuck', "fuckin'", "shit", "motherfuckin'", "ass", "pussy"]
    print(artist+ " - " +song_name)
    print ("Number of profane words: " +str((name_to_lyrics(artist, song_name, profanity))))
    
if __name__ == "__main__":
    main()
