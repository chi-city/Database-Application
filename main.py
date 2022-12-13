# ----------------------------------------------------------------

"""
File: main.py

executes application of python program, presentation tier
5 main commands:
    1. lookup movies by name/pattern,
    2. lookup details about a specific movie,
    3. top N movies by average rating,
    4. insert a review, and
    5. set a movie's tagline. 

Original Author:
   Zaid Awaidah
   UIC
   CS 341, Fall 2022
   Project 02
"""

# ----------------------------------------------------------------

import sqlite3
import objecttier

# ----------------------------------------------------------------

"""
findMovie

command_4 and command_5
helper funct

searches for movie before
inserting a review
"""
def findMovie(dbConn, movie_id):
    query =  """
            SELECT DISTINCT Movies.Movie_ID
            FROM Movies
            WHERE Movies.Movie_ID = ?
            GROUP BY Movies.Movie_ID;
            """
    movie = objecttier.datatier.select_one_row(dbConn, query, [movie_id])
    return movie

# ----------------------------------------------------------------

"""
print_stats

prints general stats about
movie database
"""
def print_stats(dbConn):
    num_Movies = objecttier.num_movies(dbConn)
    num_Reviews = objecttier.num_reviews(dbConn)
    print("General stats:")
    print(f" # of movies:  {num_Movies:,}")
    print(f" # of reviews:  {num_Reviews:,}\n")

# ----------------------------------------------------------------

"""
command_1

calls get_movies from objecttier to 
find a movie according to user input,
returns one or a list of movies.
"""
def command_1(dbConn):
    name = input("\nEnter movie name (wildcards _ and % supported): ")
    movies = objecttier.get_movies(dbConn, name)

    if movies != None:
        print("\n# of movies found: ", len(movies))
        print()

        if len(movies) >= 100:
            return print("There are too many movies to display,"
               + " please narrow your search and try again...")

        for movie in movies:
            print(f"{movie.Movie_ID} : {movie.Title} ({movie.Release_Year})")
    print()

# ----------------------------------------------------------------

"""
command_2

inputs movie_id and then outputs
detailed movie information based
on movie_id
"""
def command_2(dbConn):
    movie_ID = input("\nEnter movie id: \n")
    movie = objecttier.get_movie_details(dbConn, movie_ID)

    if movie != None:
        print(f"{movie.Movie_ID} : {movie.Title}")
        print(f" Release date: {movie.Release_Date}\n"
              + f" Runtime: {movie.Runtime} (mins)\n"
              + f" Orig language: {movie.Original_Language}\n"
              + f" Budget: ${movie.Budget:,} (USD)\n"
              + f" Revenue: ${movie.Revenue:,} (USD)\n"
              + f" Num reviews: {movie.Num_Reviews}")
        if movie.Avg_Rating is None:
            print(" Avg rating: 0.00 (0..10)")
        else:
            print(f" Avg rating: {movie.Avg_Rating:.2f} (0..10)")
        if movie.Genres == []:
            print(" Genres: ")
        else:
            print(" Genres: {}".format(', '.join(movie.Genres) +","))
        if movie.Production_Companies == []:
            print(" Production companies: ")
        else:
            print(" Production companies: {},".format(', '.join(movie.Production_Companies)))
        print(f" Tagline: {movie.Tagline}")
    else:
        return print("\nNo such movie...")

# ----------------------------------------------------------------

"""
command_3

Output the top N movies based on their average 
rating  *and* with a minimum number of reviews. 
"""
def command_3(dbConn):
    N = int(input("\nN? "))
    if N <= 0:
        return print("Please enter a positive value for N...\n")
    reviews  = int(input("min number of reviews? "))
    if reviews <= 0:
        return print("Please enter a positive value for min number of reviews...\n")
    movies = objecttier.get_top_N_movies(dbConn, N, reviews)
    
    print()
    for movie in movies:
        print(f"{movie.Movie_ID} : {movie.Title} ({movie.Release_Year})"
                + f", avg rating = {movie.Avg_Rating:.2f} ({movie.Num_Reviews} reviews)")
    print()

# ----------------------------------------------------------------

"""
command_4

Inserts a new review into the database.
The program inputs a movie id and
a rating (0..10), and then inserts
the review after validating the input:
"""
def command_4(dbConn):
    rating = int(input("\nEnter rating (0..10): "))
    if rating < 0  or rating > 10:
        return print("Invalid rating...\n")
    
    movie_ID = input("Enter movie id: ")
    movie = findMovie(dbConn, movie_ID)

    if movie is None or movie == ():
        return print("\nNo such movie...\n")
    
    # insert
    insert_rating = objecttier.add_review(dbConn, movie_ID, rating)
    
    if insert_rating > 0:
      return print("\nReview successfully inserted\n")


# ----------------------------------------------------------------

"""
command_5

Sets the tagline for a given movie,
either by inserting (if not already there)
or updating (if already there)
"""
def command_5(dbConn):
    tagline = input("\ntagline? ")
    movie_id = input("movie id? ")

    movie = findMovie(dbConn, movie_id)
    
    if movie is None or movie == ():
        return print("\nNo such movie...\n")

    result = objecttier.set_tagline(dbConn, movie_id, tagline)

    if result > 0:
      return print("\nTagline successfully set\n")
    

# ----------------------------------------------------------------

"""
call_commands

calls respective commands
based off of user input
"""
def call_commands(command, dbConn):
    if command == "1":
        command_1(dbConn)
    elif command == "2":
        command_2(dbConn)
    elif command == "3":
        command_3(dbConn)
    elif command == "4":
        command_4(dbConn)
    elif command_5(dbConn):
        command_5(dbConn)
    elif command == "x":
        return
    
# ----------------------------------------------------------------

"""
main
"""
def main():
    print("** Welcome to the MovieLens app **\n")
    command = ""
    dbConn = sqlite3.connect('MovieLens.db')

    # General Stats
    print_stats(dbConn)

    # command-loop
    while command != "x":
        command = input("Please enter a command (1-5, x to exit): ")
        if command != "x":
            call_commands(command, dbConn)

    pass

# ----------------------------------------------------------------

"""
call main at runtime
"""
if __name__ == "__main__":
    main()

# ----------------------------------------------------------------