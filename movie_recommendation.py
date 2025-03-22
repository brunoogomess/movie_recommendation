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
    1. movieid
    2. title
    3. genres
    '''
    movies = pd.read_csv("~/desktop/projects/movie_recommendation/ml-32m/movies.csv")
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
    chosen_genre = input(f"please choose a genre from the following list:\n{genre_list}\n")
    chosen_genre = sorted(chosen_genre.title().split(" "))
    for genre in chosen_genre:
        if genre not in genre_list:
            print(f"{genre} is not in the list. please choose a genre from the following list:\n{genre_list}\n")
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
    create_rating_df(chosen_genre_df, ratings)
    

def create_rating_df(chosen_genre_df, ratings):
    '''
    joins genres with ratings
    get th/e average rating for each movie
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
    movie_list = pd.merge(movie_list, links, left_on="movieId", right_on="movieId")
    print(movie_list.head(5))
    release_date_filter(movie_list, links)


def release_date_filter(movie_list, links):
    '''
    ask the user the decade of the movie
    get the release date from the title column
    display the movies with the proper links to imdb
    '''
    movie_list["release_date"] = movie_list["title"].str.strip().str[-5:-1]
    print(movie_list.head(5))
    chosen_decade = input("Please choose a release decade for the movie from the following list:\n1. 2020's\n2. 2010's\n3. 2000's\n4. 1990's\n5. 1980's\n6. Others\n")

    match chosen_decade:
        case "1":
            final_list = movie_list[movie_list["release_date"].astype(int) >= 2020]
            
        case "2":
            final_list =  movie_list[
            (movie_list["release_date"].astype(int) >= 2010) & 
            (movie_list["release_date"].astype(int) < 2020)]

        case "3":
            final_list =  movie_list[
            (movie_list["release_date"].astype(int) >= 2000) & 
            (movie_list["release_date"].astype(int) < 2010)]

        case "4":
            final_list =  movie_list[
            (movie_list["release_date"].astype(int) >= 1990) & 
            (movie_list["release_date"].astype(int) < 2000)]

        case "5":
            final_list =  movie_list[
            (movie_list["release_date"].astype(int) >= 1980) & 
            (movie_list["release_date"].astype(int) < 1990)]

        case "6":
            final_list = movie_list[movie_list["release_date"].astype(int) < 1980]

        case _:
            print("Incorrect Input!")
            return(release_date_filter(movie_list, links))

    final_list = pd.merge(final_list, links, right_on="movieId", left_on="movieId")
    print(final_list.head(50))
    
    
ask_genre()

'''
    TO-DO:
    3. Show the links to the movies and ask if the user wants more movies 
    4. Order by rating, release date, random (ask user)
'''


'''
    ISSUES:
    1.There is an issue with "IMAX", if the user just writes imax it converts to Imax, which is not a genre in the list

    2.If the user only choses a genre, should the movies that are recommended be only of that genre? i.e. user chooses action and gets action,  comedy and other atm, should he only get action itself?
'''








