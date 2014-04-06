import csv
import os

def load_country_dict():
    """
    Here we are loading from a CSV the countries about which we are able to scrape data.  This list of countries was downloaded directly from http://atlas.media.mit.edu/about/data/country/.  The goal of this project was to scrape the import/export data, so we simply downloaded this data from the website.
    """
    f = open('country_codes.txt', 'rU')
    reader = csv.reader(f)
    country_dict = {}
    for row in reader:
        country_dict[row[0]] = row[1]
    return country_dict

def get_data(filename):
    f = open(filename, 'rU')
    reader = csv.reader(f)
    temp_array = []
    for row in reader:
        temp_array.append(row)
    for row in temp_array[1:]:
        print row