#!/usr/bin/env python
# Name: Marije Brandsma
# Student number: 11389257
"""
This script parses a database and analyzes/visualizes the data in it.
"""

import csv
import pandas
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

INPUT_CSV = 'input.csv'
OUTPUT_CSV = 'data.csv'

def read_csv(infile):
    """
    Reads the infile, cleans the data and saves the data in a list.
    """
    reader = csv.reader(infile)
    list = []

    # Loops through all countries in the infile, skips empty rows
    for item in reader:
        try:
            # Stores the needed data in a variable
            country = (item[0],item[1],item[4],item[7],item[8])

            # Stores country name and removes space at the end
            country_name = country[0]
            country_name = country_name.rstrip()

            # Stores region, removes spaces at the end and corrects capitalization
            country_region = country[1]
            country_region = country_region.rstrip()
            country_region = country_region.title()

            # Stores population density, replaces empty values with -1
            country_pop_density = country[2]
            if country_pop_density == 'unknown':
                country_pop_density = -1
            else:
                country_pop_density = country_pop_density.replace(',','.')
                country_pop_density = float(country_pop_density)

            # Stores infant mortality, replaces empty values with -1
            country_inf_mortality = country[3]
            if country_inf_mortality == 'unknown':
                country_inf_mortality = -1
            else:
                country_inf_mortality = country_inf_mortality.replace(',','.')
                country_inf_mortality = float(country_inf_mortality)

            # Stores GDP, replaces empty values with -1
            country_gdp = country[4]
            if country_gdp == 'unknown':
                country_gdp = -1
            country_gdp = ''.join(c for c in country_gdp if c not in ' dollars')
            country_gdp = int(country_gdp)

            # Create dictionary of country and add to list
            country_data = dict()
            country_data['country'] = country_name
            country_data['region'] = country_region
            country_data['pop_density'] = country_pop_density
            country_data['inf_mortality'] = country_inf_mortality
            country_data['gdp'] = country_gdp
            list.append(country_data)

        except:
            pass

    return(list)

def make_dataframe(infile):
    """
    Changes clean data to pandas format.
    """

    data = pandas.read_csv(clean_data)
    print("Clean data pd:")
    print(data)


def save_csv(outfile):
    """
    Output a CSV file with the parsed data of the infile.
    """
    writer = csv.writer(outfile)
    writer.writerow(['Country', 'Region', 'Pop. Density (per sq. mi.)', 'Infant mortality (per 1000 births)', 'GDP ($ per capita) dollars'])

    with open(INPUT_CSV, 'r', newline='') as input_file:
        clean_data = read_csv(input_file)
        print(clean_data)

    for country in clean_data:
        writer.writerow([country['country'], country['region'], country['pop_density'], country['inf_mortality'], country['gdp']])


if __name__ == "__main__":
    # Writes the CSV file to the disk
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file)

    clean_data = 'data.csv'
    make_dataframe(clean_data)
