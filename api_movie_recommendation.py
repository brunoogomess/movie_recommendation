import requests
import credentials_file


headers = {
        "accept": "application/json",
        "Authorization": credentials_file.bearer_token
    }

def get_genre_list():
    '''
    gets all the genres on the API
    '''
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
    '''
    asks the user for the desired genre
    providing the list of all  genres
    '''
    chosen_genre = input(f"Please choose a genre from the following list:\n{genre_list}\n")
    chosen_genre = sorted(chosen_genre.title().split(" "))
    for genre in chosen_genre:
        if genre not in genre_list:
            print(f"{genre} is not in the list.") 
            return(ask_genre(genre_list, genre_dict))
        genre_id = genre_dict.get(genre)
        
        get_movie_list(genre_id)

def get_movie_list(genre_id):
    '''
    gets a list of movies (title:id)
    that belong to the desired genre
    '''
    movie_data = []
    #for page in range(1,1):
        #movies_filtered_by_genre_url = f'https://api.themoviedb.org/3/discover/movie?page={page}&with_genres={genre_id}&language=en-US&sort_by=popularity.desc'
    movies_filtered_by_genre_url = f'https://api.themoviedb.org/3/discover/movie?page=1&with_genres={genre_id}&language=en-US&sort_by=popularity.desc'
    response = requests.get(movies_filtered_by_genre_url, headers=headers).json()
    movie_data = [*movie_data, *response["results"]]
    print(movie_data)
    for movie in movie_data:
        movie_dict = {"title": movie["title"], "id": movie["id"], "popularity": movie["popularity"], "release_date": movie["release_date"]}
        print(movie_dict)

        
get_genre_list()




'''
TO DO:
1. add release date
3. should I convert this to a df and use the pandas code that i developed before?
'''
