'''
this is a python program to recommend movies for me and my gf to see, since she's always so undecisive 
and always ask me to choose and I can't choose because I'm undecisive too and we never end up watching anything.
'''

import pandas as pd


'''
the ratings csv file contains the following:
1. userID
2. movieId 
3. rating 
4. timestamp
'''
ratings = pd.read_csv("~/Desktop/projects/movie_recommendation/ml-32m/ratings.csv")
#print(ratings.head())

'''
the links csv file contains the following:
1. movieId
2. imdbID
3. tmdbID
'''
links = pd.read_csv("~/Desktop/projects/movie_recommendation/ml-32m/links.csv")
#print(links.head())


def ask_genre():
    '''
    the movies csv file contains the following:
    1. movieId
    2. title
    3. genres
    '''
    movies = pd.read_csv("~/Desktop/projects/movie_recommendation/ml-32m/movies.csv")
    #print(movies.head())
    '''
    this part gets all the genres of all the movies listed,
    sorts them and removes the duplicates,
    providing a list of all the genres available for the user to choose
    '''
    genres = movies["genres"].str.split('|')
    genre_list_unsorted = []
    for i in genres:
        for x in i:
            genre_list_unsorted.append(x)

    genre_list = sorted(set(genre_list_unsorted))
    genre_list.pop(0) #this just removes the "no genres"
    chosen_genre = input(f"Please choose a genre from the following list:\n{genre_list}\n")
    chosen_genre = sorted(chosen_genre.title().split(" "))
    for genre in chosen_genre:
        if genre not in genre_list:
            print(f"{genre} is not in the list. Please choose a genre from the following list:\n{genre_list}\n")
            return(ask_genre())
    create_genre_df(chosen_genre, movies)


def create_genre_df(chosen_genre, movies):
    '''
    gets all the movies that have all the chosen genres
    if there is none, recursively get the movies that have the first n-1 genres
    '''
    chosen_genre_df = movies[movies['genres'].apply(lambda g: all(genre in g.split('|') for genre in chosen_genre))]
    if chosen_genre_df.empty:
        print(f"There are no movies with all the specified genres. Removing {chosen_genre[-1]}")
        chosen_genre.pop()
        create_genre_df(chosen_genre, movies)
    #print(chosen_genre_df.head(20))
    create_rating_df(chosen_genre_df, ratings)
    

def create_rating_df(chosen_genre_df, ratings):
    '''
    joins genres with ratings
    get the average rating for each movie
    ask user what is the desired rating
    returns a df with all the movies that comply
    '''
    chosen_rating = input("Please choose a rating for the movie from 1 to 5 stars.\n")
    if chosen_rating not in ("12345"):
        print("Please insert a valid number from 1 to 5")
        return(create_rating_df(chosen_genre_df, ratings))
    ratings_mean_df = ratings.groupby('movieId')['rating'].mean().round(0)
    chosen_genres_with_ratings_df = pd.merge(chosen_genre_df, ratings_mean_df, left_on="movieId", right_on="movieId") 
    movie_list = chosen_genres_with_ratings_df[chosen_genres_with_ratings_df["rating"] == float(chosen_rating)]

    print(movie_list.head(5))

ask_genre()

'''
TO-DO:
1.Do another join with the links file and provide the imdb link 
'''


'''
ISSUES:
1.There is an issue with "IMAX", if the user just writes imax it converts to Imax, which is not a genre in the list

2.If the user only choses a genre, should the movies that are recommended be only of that genre? i.e. user chooses action and gets action,  comedy and other atm, should he only get action itself?
'''








