import urllib2
import json
import csv
import string
import requests
import os

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

def get_partner_data(year, country):
    """
    This function returns the JSON file that contains the data on each country from the URL specified below. The JSON file is pulled as a dictionary, and is then scrubbed into a list of dictionaies, in which each dictionary contains information about an import or export destination.
    """
    
    url = 'http://atlas.media.mit.edu/hs/export/' + str(year) + '/' + country + '/show/all/'
    page = requests.get(url)
    return page.json().values()[0]

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

def load_country_product_data(year, country):
    """
    This function explores the data that has been previously scraped and written to files by the function write_data_to_files(), and loads an array of the products imported and exported by a given country for a given year.
    """
    
    f = open('data/prod/' + country + '/' + str(year) + '.txt', 'rU')
    reader = csv.reader(f)
    product_array = []
    for row in reader:
        product_array.append(row)
    f.close()
    return product_array

def load_country_partner_data(year, country):
    """
    This function explores the data that has been previously scraped and written to files by the function write_data_to_files(), and loads an array of the import and export partners for a given country for a given year.
    """
    
    f = open('data/part/' + country + '/' + str(year) + '.txt', 'rU')
    reader = csv.reader(f)
    partner_array = []
    for row in reader:
        partner_array.append(row)
    f.close()
    return partner_array

def get_product_breakdown(year, country):
    """
    This function breaks down each product to give us the percentage mix of a given country's imports and exports for a given year.
    """
    
    product_array = load_country_product_data(year, country)
    total_exports = 0
    total_imports = 0
    for i in range(len(product_array)):
        total_exports += float(product_array[i][1])
        total_imports += float(product_array[i][2])
    product_mix_array = []
    for i in range(len(product_array)):
        temp = []
        temp.append(product_array[i][0])
        temp.append(float(product_array[i][1])/float(total_exports)*float(100))
        temp.append(float(product_array[i][2])/float(total_imports)*float(100))
        product_mix_array.append(temp)
    return product_mix_array

def get_partner_breakdown(year, country):
    """
    This function breaks down each partner to give us the percentage mix of a given country's imports and exports for a given year.
    """
    
    partner_array = load_country_partner_data(year, country)
    total_exports = 0
    total_imports = 0
    for i in range(len(partner_array)):
        total_exports += float(partner_array[i][1])
        total_imports += float(partner_array[i][2])
    product_mix_array = []
    for i in range(len(partner_array)):
        temp = []
        temp.append(partner_array[i][0])
        temp.append(float(partner_array[i][1])/float(total_exports)*float(100))
        temp.append(float(partner_array[i][2])/float(total_imports)*float(100))
        partner_array.append(temp)
    return partner_array

def categorize_products(year, country):
    """
    This function breaks down the product mix into the 21 categories provided in order to find the diversity of trade.
    """
    
    product_mix_array = get_product_breakdown(year, country)
    product_export_mix_dict = {}
    product_import_mix_dict = {}
    for i in range(len(product_mix_array)):
        hs4_id = product_mix_array[i][0]
        if hs4_id[0:2] in product_export_mix_dict.keys():
            product_export_mix_dict[hs4_id[0:2]] += float(product_mix_array[i][1])
        else:
            product_export_mix_dict[hs4_id[0:2]] = float(product_mix_array[i][1])
        if hs4_id[0:2] in product_import_mix_dict.keys():
            product_import_mix_dict[hs4_id[0:2]] += float(product_mix_array[i][2])
        else:
            product_import_mix_dict[hs4_id[0:2]] = float(product_mix_array[i][2])
    return product_export_mix_dict, product_import_mix_dict

def categorize_partners(year, country):
    """
    This function breaks down the partner mix into the 6 main continents provided in order to find the diversity of trade.
    """
    
    partner_mix_array = get_partner_breakdown(year, country)
    partner_export_mix_dict = {}
    partner_import_mix_dict = {}
    for i in range(len(partner_mix_array)):
        dest_id = partner_mix_array[i][0]
        if dest_id[0:2] in partner_export_mix_dict.keys():
            partner_export_mix_dict[dest_id[0:2]] += float(partner_mix_array[i][1])
        else:
            partner_export_mix_dict[dest_id[0:2]] = float(partner_mix_array[i][1])
        if dest_id[0:2] in partner_import_mix_dict.keys():
            partner_import_mix_dict[dest_id[0:2]] += float(partner_mix_array[i][2])
        else:
            partner_import_mix_dict[dest_id[0:2]] = float(partner_mix_array[i][2])
    return partner_export_mix_dict, partner_import_mix_dict