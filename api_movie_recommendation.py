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

    response = requests.get(all_genres_url, headers=headers).json()

    genre_dict = {genre["name"]: genre["id"] for genre in response["genres"]}

    genre_list = []

    for genre in genre_dict:
        genre_list.append(genre)
    ask_user_input(genre_list, genre_dict)


def ask_user_input(genre_list, genre_dict):
    '''
    asks the user for the desired genre
    providing the list of all  genres
    '''
    chosen_genre = input(f"Please choose a genre from the following list:\n{genre_list}\n")
    chosen_genre = sorted(chosen_genre.title().split(" "))
    genre_id_list = []
    for genre in chosen_genre:
        if genre not in genre_list:
            print(f"{genre} is not in the list.") 
            return(ask_user_input(genre_list, genre_dict))
        genre_id = genre_dict.get(genre)
        genre_id_list.append(genre_id)

    while True:
        chosen_rating = input("Please choose a rating from 1 to 10: \n")
        if chosen_rating in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'):
            break
        print("Incorrect rating")

    chosen_decade = input("Please choose a release decade for the movie from the following list:\n1. 2020's\n2. 2010's\n3. 2000's\n4. 1990's\n5. 1980's\n6. Others\n")

    match chosen_decade:
        case "1":
           release_date_lte = "2020-01-01" 
           release_date_gte = "2040-01-01" 
        case "2":
           release_date_lte = "2010-01-01" 
           release_date_gte = "2000-01-01" 

        case "3":
           release_date_lte = "2000-01-01" 
           release_date_gte = "1990-01-01" 
        case "4":
           release_date_lte = "1990-01-01" 
           release_date_gte = "1980-01-01" 
        case "5":
           release_date_lte = "1980-01-01" 
           release_date_gte = "1970-01-01" 
        case "6":
           release_date_lte = "1950-01-01" 
           release_date_gte = "1970-01-01" 

        case _:
            print("Incorrect Input!")

    get_movie_list(genre_id_list, chosen_rating, release_date_gte, release_date_lte)


def get_movie_list(genre_id_list, chosen_rating, release_date_gte, release_date_lte):
    '''
    gets a list of movies (title:id)
    that belong to the desired genre
    '''
    genre_ids = ','.join(map(str, genre_id_list))
    print(genre_ids)
    movie_data = []
    movies_filtered_url = f'https://api.themoviedb.org/3/discover/movie?page=1&with_genres={genre_ids}&vote_average.gte={chosen_rating}&language=en-US&sort_by=vote_count.desc&vote_count.gte=500&primary_release_date.gte={release_date_gte}&primary_release_date.lte={release_date_lte}'
    response = requests.get(movies_filtered_url, headers=headers).json()
    movie_data = [*movie_data, *response["results"]]
    for movie in movie_data:
        movie_dict = {"title": movie["title"], "id": movie["id"], "popularity": movie["popularity"], "release_date": movie["release_date"], "rating": movie["vote_average"], "vote count": movie["vote_count"]}
        print(f"Movie Title: {movie_dict['title']}\nLink: https://www.themoviedb.org/movie/{movie_dict['id']}\n")


        
get_genre_list()



'''
TO DO:
1. Make output prettier
2. Add the direct link to TMDB

USER INPUT FLOW:
1. choose genre
2. choose rating from 1-5
3. choose decade for release date
'''
