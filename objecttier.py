##################################################################

"""
File: objecttier.py

Builds Movie-related objects from data retrieved through 
the data tier.

Original author:
  Prof. Joe Hummel
  U. of Illinois, Chicago
  CS 341, Spring 2022
  Project 02

New author:
   Zaid Awaidah
   UIC
   CS 341, Fall 2022
   Project 02
"""

"""
TODO: test case 8
"""

##################################################################

import datatier

##################################################################

"""
Movie:

Constructor(...)
Properties:
  Movie_ID: int
  Title: string
  Release_Year: string

"""
class Movie:
   def __init__(self, Movie_ID = 0, Title = "", Release = ""):
      self._Movie_ID = Movie_ID
      self._Title = Title
      self._Release_Year = Release

   @property
   def Movie_ID(self):
      return self._Movie_ID
   
   @property
   def Title(self):
      return self._Title
   
   @property
   def Release_Year(self):
      return self._Release_Year

##################################################################

"""
MovieRating:

Constructor(...)
Properties:
  Movie_ID: int
  Title: string
  Release_Year: string
  Num_Reviews: int
  Avg_Rating: float

"""
class MovieRating:
   def __init__(self,
      Movie_ID = 0,
      Title = '',
      Release = '',
      Num_Reviews = 0,
      Avg_Rating = 0.0,
   ):
      self._Movie_ID = Movie_ID
      self._Title = Title
      self._Release_Year = Release
      self._Num_Reviews = Num_Reviews
      self._Avg_Rating = Avg_Rating
   
   @property
   def Movie_ID(self):
      return self._Movie_ID
   
   @property
   def Title(self):
      return self._Title
   
   @property
   def Release_Year(self):
      return self._Release_Year

   @property
   def Num_Reviews(self):
      return self._Num_Reviews
   
   @property
   def Avg_Rating(self):
      return self._Avg_Rating
 
##################################################################

"""
MovieDetails:

Constructor(...)
Properties:
  Movie_ID: int
  Title: string
  Release_Date: string, date only (no time)
  Runtime: int (minutes)
  Original_Language: string
  Budget: int (USD)
  Revenue: int (USD)
  Num_Reviews: int
  Avg_Rating: float
  Tagline: string
  Genres: list of string
  Production_Companies: list of string

"""
class MovieDetails:
   def __init__(self,
      Movie_ID = 0,
      Title = '',
      Release_Date = '',
      Runtime = 0,
      Orig_Lang = "",
      Budget = 0,
      Revenue = 0,
      Num_Reviews = 0,
      Avg_Rating = 0.00,
      Tagline = "",
      Genres = [],
      Prod_Companies = []
   ):
      self._Movie_ID = Movie_ID
      self._Title = Title
      self._Release_Date = Release_Date
      self._Runtime = Runtime
      self._Original_Language = Orig_Lang
      self._Budget = Budget
      self._Revenue = Revenue
      self._Num_Reviews = Num_Reviews
      self._Avg_Rating = Avg_Rating
      self._Tagline = Tagline
      self._Genres = Genres
      self._Production_Companies = Prod_Companies
   
   @property
   def Movie_ID(self):
      return self._Movie_ID
   
   @property
   def Title(self):
      return self._Title
   
   @property
   def Release_Date(self):
      return self._Release_Date

   @property
   def Runtime(self):
      return self._Runtime
   
   @property
   def Original_Language(self):
      return self._Original_Language
   
   @property
   def Budget(self):
      return self._Budget
   
   @property
   def Revenue(self):
      return self._Revenue
   
   @property
   def Num_Reviews(self):
      return self._Num_Reviews
   
   @property
   def Avg_Rating(self):
      return self._Avg_Rating
   
   @property
   def Tagline(self):
      return self._Tagline
   
   @property
   def Genres(self):
      return self._Genres

   @property
   def Production_Companies(self):
      return self._Production_Companies

##################################################################

"""
get_queries

defines queries for get_movie_details
"""
def get_queries_movie_details():
   movieQuery =      """
                     SELECT DISTINCT Movies.Movie_ID,
                        Movies.Title,
                        DATE(Movies.Release_Date),
                        Movies.Runtime,
                        Movies.Original_Language,
                        Movies.Budget,
                        Movies.Revenue
                     FROM Movies
                     WHERE Movies.Movie_ID = ?
                     GROUP BY Movies.Movie_ID;
                     """

   ratingQuery =     """
                     SELECT COUNT(Ratings.Movie_ID),
                        AVG(Ratings.Rating)
                     FROM Ratings
                     WHERE Ratings.Movie_ID = ?
                     """

   genreQuery =      """
                     SELECT DISTINCT GROUP_CONCAT(Genres.Genre_Name, ', '),
                        Movie_Taglines.Tagline
                     FROM Genres
                     LEFT JOIN
                        Movie_Genres on Genres.Genre_ID = 
                           Movie_Genres.Genre_ID
                     LEFT JOIN
                        Movie_Taglines on Movie_Genres.Movie_ID = Movie_Taglines.Movie_ID
                     WHERE Movie_Genres.Movie_ID = ?
                     ORDER BY Genres.Genre_Name ASC;
                     """

   companiesQuery =  """
                     SELECT DISTINCT GROUP_CONCAT(Company_Name, ', ')
                     FROM Companies
                     JOIN
                        Movie_Production_Companies on Companies.Company_ID = 
                            Movie_Production_Companies.Company_ID
                     WHERE Movie_Production_Companies.Movie_ID = ?
                     """

   return movieQuery, ratingQuery, genreQuery, companiesQuery

##################################################################

"""
num_movies:

Returns: # of movies in the database; if an error returns -1
"""
def num_movies(dbConn):
   query =  """
            SELECT COUNT(Movie_ID)
            FROM Movies;
            """
   
   row = datatier.select_one_row(dbConn, query, [])
   if row is None:
      return -1
   
   return row[0]

##################################################################

"""
num_reviews:

Returns: # of reviews in the database; if an error returns -1
"""
def num_reviews(dbConn):
   query =  """
            SELECT COUNT(Rating)
            FROM Ratings;
            """
   
   row = datatier.select_one_row(dbConn, query, [])
   if row is None:
      return -1
   
   return row[0]


##################################################################

"""
get_movies:

gets and returns all movies whose name are "like"
the pattern. Patterns are based on SQL, which allow
the _ and % wildcards. Pass "%" to get all stations.

Returns: list of movies in ascending order by name; 
         an empty list means the query did not retrieve
         any data (or an internal error occurred, in
         which case an error msg is already output).
"""
def get_movies(dbConn, pattern):
   movies = []
   query =  """
            SELECT Movie_ID,
               Title,
               strftime('%Y', DATE(Release_Date))
            FROM Movies
            WHERE Title Like ?
            Order By Title ASC;
            """
   rows = datatier.select_n_rows(dbConn, query, [pattern])
   
   if rows is None:
      return []
   
   for row in rows:
      movie = Movie(row[0], row[1], row[2])
      movies.append(movie)
   
   return movies

##################################################################

"""
get_movie_details:

gets and returns details about the given movie; you pass
the movie id, function returns a MovieDetails object. Returns
None if no movie was found with this id.

Returns: if the search was successful, a MovieDetails obj
         is returned. If the search did not find a matching
         movie, None is returned; note that None is also 
         returned if an internal error occurred (in which
         case an error msg is already output).
"""
def get_movie_details(dbConn, movie_id):
   movieQuery, ratingQuery, genreQuery, companiesQuery = get_queries_movie_details()
   company = []
   genre = []
   avg_rating = 0.00

   movies = datatier.select_one_row(dbConn, movieQuery, [movie_id])
   if movies == () or movies == None:
      return None

   
   companies = datatier.select_one_row(dbConn, companiesQuery, [movie_id])
   if companies[0] is not None:
      company = companies[0].split(", ")
      company.sort()

   genres = datatier.select_one_row(dbConn, genreQuery, [movie_id])
   if genres[0] is not None:
      genre = genres[0].split(", ")
      genre.sort()
   
   if genres[1] is None:
      tagline = ""
   else:
      tagline = genres[1]
   
   ratings = datatier.select_one_row(dbConn, ratingQuery, [movie_id])
   if ratings[0] != 0:
      avg_rating = ratings[1]
   

   Movie = MovieDetails(movies[0], movies[1], movies[2], movies[3], movies[4],
      movies[5], movies[6], ratings[0], avg_rating, tagline, genre,
      company)

   return Movie
         
##################################################################

"""
get_top_N_movies:

gets and returns the top N movies based on their average 
rating, where each movie has at least the specified # of
reviews. Example: pass (10, 100) to get the top 10 movies
with at least 100 reviews.

Returns: returns a list of 0 or more MovieRating objects;
         the list could be empty if the min # of reviews
         is too high. An empty list is also returned if
         an internal error occurs (in which case an error 
         msg is already output).
"""
def get_top_N_movies(dbConn, N, min_num_reviews):
   movies = []
   query =  """
            Select Movies.Movie_ID,
               Title,
               strftime('%Y', DATE(Release_Date)),
               avg(Rating),
               count(Rating)
            From Movies
            Join Ratings
               on Movies.Movie_ID = Ratings.Movie_ID
            Group By Movies.Movie_ID
            Having count(Rating) >= ?
            Order By avg(Rating) desc
            Limit ?;
            """
   
   rows = datatier.select_n_rows(dbConn, query, [min_num_reviews, N])

   if rows is None:
      return []

   for row in rows:
      movie = MovieRating(row[0], row[1], row[2], row[4], row[3])
      movies.append(movie)
   
   return movies


##################################################################

"""
add_review:

Inserts the given review --- a rating value 0..10 --- into
the database for the given movie. It is considered an error
if the movie does not exist (see below), and the review is
not inserted.

Returns: 1 if the review was successfully added, returns
         0 if not (e.g. if the movie does not exist, or if
         an internal error occurred).
"""
def add_review(dbConn, movie_id, rating):
   # look for movie
   query =  """
            SELECT DISTINCT Movies.Movie_ID
            FROM Movies
            WHERE Movies.Movie_ID = ?
            GROUP BY Movies.Movie_ID;
            """
   movie = datatier.select_one_row(dbConn, query, [movie_id])

   if movie == None or movie == ():
      return 0
   else:
      query =  """
               INSERT INTO Ratings(Movie_ID, Rating)
               VALUES(?, ?);
               """
      try:
         insert_rating = datatier.perform_action(dbConn, query, [movie_id, rating])
         return insert_rating
      except Exception as err:
         return 0

##################################################################

"""
set_tagline:

Sets the tagline --- summary --- for the given movie. If
the movie already has a tagline, it will be replaced by
this new value. Passing a tagline of "" effectively 
deletes the existing tagline. It is considered an error
if the movie does not exist (see below), and the tagline
is not set.

Returns: 1 if the tagline was successfully set, returns
         0 if not (e.g. if the movie does not exist, or if
         an internal error occurred).
"""
def set_tagline(dbConn, movie_id, tagline):
   # look for movie
   query =  """
            SELECT DISTINCT Movies.Movie_ID
            FROM Movies
            WHERE Movies.Movie_ID = ?
            GROUP BY Movies.Movie_ID;
            """
   movie = datatier.select_one_row(dbConn, query, [movie_id])
   if movie == None or movie == ():
      return 0

   # look for taglines
   search_query =    """
                     SELECT EXISTS(SELECT Tagline FROM Movie_Taglines WHERE Movie_ID = ?);
                     """
   search = datatier.select_one_row(dbConn, search_query, [movie_id])
   
   # update tagline
   if search[0] == 1:
      query =  """
               UPDATE Movie_Taglines
                  SET Tagline = ?
                  WHERE Movie_ID = ?;
               """
      try:
         rating = datatier.perform_action(dbConn, query, [tagline, movie_id])
         return rating
      except Exception as err:
         return 0
   # insert tagline
   elif search[0] == 0:
      query =  """
               INSERT INTO Movie_Taglines(Movie_ID,Tagline)
               VALUES(?, ?);
               """
      try:
         rating = datatier.perform_action(dbConn, query, [movie_id,tagline])
         return rating
      except Exception as err:
         return 0
   
   

##################################################################
