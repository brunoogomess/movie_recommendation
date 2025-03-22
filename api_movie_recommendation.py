import requests
import credentials_file

def get_genre_list():
    all_genres_url = 'https://api.themoviedb.org/3/genre/movie/list?language=en'

    headers = {
            "accept": "application/json",
            "Authorization": credentials_file.bearer_token
    }

    response = requests.get(all_genres_url, headers=headers).json()

    genre_dict = {genre["name"]: genre["id"] for genre in response["genres"]}

    genre_list = []

    for genre in genre_dict:
        genre_list.append(genre)
    ask_genre(genre_list, genre_dict)


def ask_genre(genre_list, genre_dict):
    chosen_genre = input(f"Please choose a genre from the following list:\n{genre_list}\n")
    chosen_genre = sorted(chosen_genre.title().split(" "))
    for genre in chosen_genre:
        if genre not in genre_list:
            print(f"{genre} is not in the list. please choose a genre from the following list:\n{genre_list}\n")
            return(ask_genre(genre_list, genre_dict))
    print(chosen_genre)
    get_movie_list(chosen_genre, genre_dict)

def get_movie_list(chosen_genre, genre_dict):
    chosen_genre_id = genre_dict.keys()
    print(chosen_genre_id)
    movies_filtered_by_genre_url = f'https://api.themoviedb.org/3/discover/movie?genre_id={genre_id}'



get_genre_list()
