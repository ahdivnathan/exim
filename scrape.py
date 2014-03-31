import urllib2
import json
import csv
import string
import requests
import os

"""
This is a script that scrapes the Observatory of Economic Complexity
at MIT's Media Lab.  For each country whose data we scrape, we are collecting
various pieces of information regarding who they import and export from, and
what products they import and export.
"""

def load_country_dict():
    """
    Here we are loading from a CSV the countries about which we are able
    to scrape data.  This list of countries was downloaded directly from
    http://atlas.media.mit.edu/about/data/country/.  The goal of this project
    was to scrape the import/export data, so we simply downloaded this data
    from the website.
    """
    f = open('country_codes.txt', 'rU')
    reader = csv.reader(f)
    country_dict = {}
    for row in reader:
        country_dict[row[0]] = row[1]
    return country_dict

def get_partner_data(year, country):
    """
    This function returns the JSON file that contains the data on each
    country from the URL specified below. The JSON file is pulled as a
    dictionary, and is then scrubbed into a list of dictionaies, in which
    each dictionary contains information about an import or export
    destination.
    """
    
    url = 'http://atlas.media.mit.edu/hs/export/' + str(year) + '/' + country + '/show/all/'
    page = requests.get(url)
    return page.json().values()[0]

def get_product_data(year, country):
    """
    This function returns the JSON file that contains the data on each
    country from the URL specified below.  The JSON file is pulled as a
    dictionary, and is then scrubbed into a list of dictionaries, in which
    each dictionary contains information about a particular product that is
    imported or exported.
    """
    
    url = 'http://atlas.media.mit.edu/hs/export/' + str(year) + '/' + country + '/all/show/'
    page = requests.get(url)
    return page.json().values()[0]

def write_data_to_files():
    """
    This function uses get_product_data() and get_partner_data() to write
    files containing the data scraped from the Observatory of Economic
    Complexity.  These will be formatted as CSVs for easy access later.
    """
    
    country_dict = load_country_dict()
    countries = country_dict.keys()
    years = range(1995, 2013)
    for country in countries:
        os.makedirs('data/part/' + country)
        os.makedirs('data/prod/' + country)
        for year in years:
            f = open('data/part/' + country + '/' + str(year) + '.txt', 'wb')
            writer = csv.writer(f)
            to_write = []
            part_raw_data = get_partner_data(year, country)
            for i in range(len(part_raw_data)):
                temp = []
                temp.append(part_raw_data[i]['dest_id'])
                temp.append(part_raw_data[i]['export_val'])
                temp.append(part_raw_data[i]['import_val'])
                to_write.append(temp)
            writer.writerows(to_write)
            f.close()
            f = open('data/prod/' + country + '/' + str(year) + '.txt', 'wb')
            writer = csv.writer(f)
            to_write = []
            prod_raw_data = get_product_data(year, country)
            for i in range(len(part_raw_data)):
                temp = []
                temp.append(prod_raw_data[i]['dest_id'])
                temp.append(prod_raw_data[i]['export_val'])
                temp.append(prod_raw_data[i]['import_val'])
                to_write.append(temp)
            writer.writerows(to_write)
            f.close()
    