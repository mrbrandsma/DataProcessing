#!/usr/bin/env python
# Name: Marije Brandsma
# Student number: 11389257
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib.pyplot as plt

# Global constants for the input file, first and last year
INPUT_CSV = "movies.csv"
START_YEAR = 2008
END_YEAR = 2018

# Creates an empty movie list
movie_list = []

# Stores movies from csv file in a dictionary
with open(INPUT_CSV, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        movie = (row['Title'], row['Rating'], row['Year'], row['Runtime'])
        movie_list.append(movie)

# Global dictionary for the data
data_dict = {str(key): [] for key in range(START_YEAR, END_YEAR)}

# Adds movie ratings to the list of the correct year
for item in movie_list:
    movie_rating = float(item[1])
    movie_year = item[2]
    data_dict[movie_year].append(movie_rating)

# Calculates averages for every year
avg_movie_ratings = {}
for year, rating in data_dict.items():
    avg_movie_ratings[year] = sum(rating)/ len(rating)

# Creates a plot that shows average ratings of 2008-2017
plt.plot(range(len(avg_movie_ratings)), list(avg_movie_ratings.values()))
plt.xticks(range(len(avg_movie_ratings)), list(avg_movie_ratings.keys()))
plt.ylabel('Average rating')
plt.xlabel('Year')
plt.show()

if __name__ == "__main__":
    print(data_dict)
