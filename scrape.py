import json
import csv
import string
import requests
import os
from pandas import DataFrame
from numpy import array, ndarray, matrix
import numpy
import ystockquote

"""
This is a script that scrapes the Observatory of Economic Complexity at MIT's Media Lab.  For each country whose data we scrape, we are collecting data on who they import and export from, and what products they import and export.
"""

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

def get_product_data(year, country):
    """
    This function returns the JSON file that contains the data on each country from the URL specified below.  The JSON file is pulled as a dictionary, and is then scrubbed into a list of dictionaries, in which each dictionary contains information about a particular product that is imported or exported.
    """
    
    url = 'http://atlas.media.mit.edu/hs/export/' + str(year) + '/' + country + '/all/show/'
    page = requests.get(url)
    return page.json().values()[0]

def write_data_to_files():
    """
    This function uses get_product_data() and get_partner_data() to write files containing the data scraped from the Observatory of Economic Complexity.  These will be formatted as CSVs for easy access later.
    """
    
    country_dict = load_country_dict()
    countries = country_dict.keys()
    years = range(1995, 2012)
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
                if 'export_val' in part_raw_data[i].keys():
                    temp.append(part_raw_data[i]['export_val'])
                else:
                    temp.append(0)
                if 'import_val' in part_raw_data[i].keys():
                    temp.append(part_raw_data[i]['import_val'])
                else:
                    temp.append(0)
                to_write.append(temp)
            writer.writerows(to_write)
            f.close()
            f = open('data/prod/' + country + '/' + str(year) + '.txt', 'wb')
            writer = csv.writer(f)
            to_write = []
            prod_raw_data = get_product_data(year, country)
            for i in range(len(prod_raw_data)):
                temp = []
                temp.append(prod_raw_data[i]['hs_id'])
                if 'export_val' in prod_raw_data[i].keys():
                    temp.append(prod_raw_data[i]['export_val'])
                else:
                    temp.append(0)
                if 'import_val' in prod_raw_data[i].keys():
                    temp.append(prod_raw_data[i]['import_val'])
                else:
                    temp.append(0)
                to_write.append(temp)
            writer.writerows(to_write)
            f.close()
            
"""
No we will define the functions that we will call to scrape the stock index data for various countries.  Because not all countries have established indexes, we will only be gathering this data for a select list of countries.
"""
            
def csvExtract(filename, country):
    """
    This function takes a previously downloaded csv file of the historical daily prices for a stock index, and determines the average price for each year, storing the averages in another csv file with the designated country's name.
    """
    
	rawdata = []
	filepath = 'data/stock/manual/' + filename
	file2 = open(filepath, 'rU')
	reader2 = csv.reader(file2)
	for row in reader2:
		rawdata.append(row)

	currentYear = rawdata[1][0][-2:]
	prices = []
	data = []
	for i in range(1, len(rawdata)):
		if rawdata[i][0][-2:] == currentYear:
			prices.append(float(rawdata[i][4]))
		else:
			data.append([currentYear, float(sum(prices))/len(prices)])
			prices = []
			currentYear = rawdata[i][0][-2:]
			prices.append(float(rawdata[i][4]))

	count = 0
	for row in data:
		if count <= 12:
			row[0] = '20' + row[0]
			count += 1
		elif count >= 12:
			row[0] = '19' + row[0]
	data = sorted(data)

	with open('data/stock/done/' + country + '.csv', 'w') as file1:
		file1write = csv.writer(file1, delimiter = ',')
		file1write.writerows(data)

	file1.close()

def yahooExtract(ticker, country):
    """
    This function uses the python library 'ystockquote', which requests historical prices and returns them as dictionaries.  We then determine the average prices for each year, storing these averages in a csv file with the given country's name.
    """
    
	rawdata = ystockquote.get_historical_prices(ticker, '1995-01-01', '2011-12-31')

	prices = {}
	for date in rawdata.keys():
		if date[0:4] in prices.keys():
			prices[date[0:4]].append(float(rawdata[date]['Close']))
		else:
			prices[date[0:4]] = []
			prices[date[0:4]].append(float(rawdata[date]['Close']))

	data = []
	for year in sorted(prices.keys()):
		data.append([year, float(sum(prices[year]))/len(prices[year])])

	with open('data/stock/done/' + country + '.csv', 'w') as file1:
		file1write = csv.writer(file1, delimiter = ',')
		file1write.writerows(data)

	file1.close()
    
def getIndexPrices():
    """
    Now that we have defined all of the functions required, we run through a previously defined csv file that links each country to its stock index data source.  We also use the standard 3-letter country codes when making new csv files.
    """
    
    filename = 'data/stock/country_indexes.csv'
    
    indexes = {}
    
    csvfile = open(filename, 'rU')
    reader = csv.reader(csvfile)
    
    for row in reader:
        indexes[row[0]] = row[1:]
    countryCodes = {}
    csvfile2 = open('data/stock/country_codes.txt', 'rU')
    reader2 = csv.reader(csvfile2)
    for row in reader2:
        countryCodes[row[1].lower()] = row[0]
    
    csvfile2.close()
    
    for country in indexes.keys():
        countryCode = countryCodes[country.lower()]
        if indexes[country][1] == 'manual':
            csvExtract(indexes[country][2], countryCode)
        else:
            yahooExtract(indexes[country][1], countryCode)
    csvfile.close()