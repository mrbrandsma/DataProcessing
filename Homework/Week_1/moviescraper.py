#!/usr/bin/env python
# Name: Marije Brandsma
# Student number: 11389257
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'


def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry contains the following fields:
    - Title
    - Rating
    - Year of release
    - Runtime
    """

    # Parses the movie list from IMDB with BeautifulSoup
    imdb_soup = BeautifulSoup(html, "lxml")
    list_soup = imdb_soup.find_all('div', {'class':'lister-item-content'})

    # Creates an empty movie list
    movie_list = []

    # Loops through every movie in the list
    for movies in list_soup:

        # Parses the title of the movie
        movie_title = movies.find('h3')
        movie_title = movie_title.a.string

        # Parses the rating of the movie
        movie_rating = movies.find('strong')
        movie_rating = float(movie_rating.string)

        # Parses the year of release of the movie
        movie_year = movies.find('span', {'class':'lister-item-year text-muted unbold'})
        movie_year = movie_year.string
        movie_year = ''.join(c for c in movie_year if c not in '()I ')

        # Parses the runtime of the movie
        movie_runtime = movies.find('span', {'class':'runtime'})
        movie_runtime = movie_runtime.string
        movie_runtime = ''.join(c for c in movie_runtime if c not in ' min')

        # Adds all the parsed information to a movie dict and adds the movie to
        # movie_list
        movie_details = dict()
        movie_details['title'] = movie_title
        movie_details['rating'] = movie_rating
        movie_details['year'] = movie_year
        movie_details['runtime'] = movie_runtime
        movie_list.append(movie_details)

    # Returns movie_list
    return [movie_list]


def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    writer = csv.writer(outfile)
    writer.writerow(['Title', 'Rating', 'Year', 'Runtime'])

    # Writes the movies to the disk
    for movie in movies:
        writer.writerow([movie['title'], movie['rating'], movie['year'], movie['runtime']])


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # Gets HTML content at target URL
    html = simple_get(TARGET_URL)

    # Saves a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # Parses the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # Extracts the movies (using the function you implemented)
    movies = extract_movies(dom)
    movies = movies[0]

    # Writes the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
