'''
this is a python program to recommend movies for me and my gf to see, since she's always so undecisive 
and always ask me to choose and I can't choose because I'm undecisive too and we never end up watching anything.
'''

import fireducks.pandas as pd


'''
the ratings csv file contains the following:
1. userID
2. movieID 
3. rating 
4. timestamp
'''
ratings = pd.read_csv("~/Desktop/projects/movie_recommendation/ml-32m/ratings.csv")
#print(ratings.head())

'''
the links csv file contains the following:
1. movieID
2. imdbID
3. tmdbID
'''
links = pd.read_csv("~/Desktop/projects/movie_recommendation/ml-32m/links.csv")
#print(links.head())


def ask_genre():
    '''
    the movies csv file contains the following:
    1. movieID
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
            ask_genre()
    print(chosen_genre)

    '''
    TO DO:
    get all the movies that have all those genres
    if there is none, get the movies that have the first n-1 genres
    if theres still none do the same (loop)
    '''

    chosen_genre_df = movies[movies['genres'].apply(lambda g: all(genre in g.split('|') for genre in chosen_genre))]
    print(chosen_genre_df.head(20))


ask_genre()












