import urllib2
import json
import csv
import string
import requests

"""
This is a script that scrapes the Observatory for Economic Complexity
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

def get_year_data(year):
    """
    This function returns a dictionary of data for a particular year of
    every country in the world.  It utilizes the 'get_data' function above
    to aggregate all of the data for a particular year, and utilizes the
    'load_country_dict' function to scrape data for that year.
    
    Returns: A dictionary for which the keys are countries and the values are
    the countries' export/import data for the given year.
    """
    
    year_dict = {}
    country_dict = load_country_dict()
    for country in country_dict.keys():
        year_dict[country] = get_data(year, country)
    return year_dict

def get_country_data(country):
    """
    This function returns a dictionary of data for a particular country,
    with data for every year from 1995 to 2011.  Some countries may not
    have data for all of these years, or for any.
    
    Returns: A dictionary for which the keys are years and the values are
    the country's export/import data for that particular year
    """
    
    year_dict = {}
    for i in range(1995, 2012):
        data = get_data(i, country)
        if data:
            year_dict[str(i)] = data
    return year_dict

def get_all_data():
    """
    This function returns a dictionary of data for all years, in which
    the keys are years, and the values are all countries' import/export
    data for that particular year.
    """
    
    main_dict = {}
    for i in range(1995, 2012):
        data = get_year_data(i)
        if data:
            main_dict[str(i)] = data
    return main_dict