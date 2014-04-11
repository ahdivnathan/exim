import csv
import os
from pandas import DataFrame
from numpy import array

def load_country_dict():
    f = open('country_codes.txt', 'rU')
    reader = csv.reader(f)
    country_dict = {}
    for row in reader:
        country_dict[row[0]] = row[1]
    return country_dict

def load_country_exrate(country):
    """
    Loading the exchange rates for a given country
    """

    f = open('data/exchange_rate/' + country + '_exc.csv', 'rU')
    reader = csv.reader(f)
    
    currency = []
    for row in reader:
        currency.append(row[:2])
    currency = currency[5:17]
    return currency


def load_all_countries():
    """
    Loading the exchange rates for all countries into a DataFrame (row = yr, col = country code)
    """
    
    country_tmp = load_country_dict()
    #country_tmp will be the full list of country code.
    tmp = []
    pure_exc = []
    for country in country_tmp:
        tmp.append(load_country_exrate(country))
    
    for i in tmp:
        for j in i:
            pure_exc.append(j[1])
    print pure_exc
    
    for i in pure_exc:
	i = i.replace(",", "")
        i = float(i)
    
        
    pure_exc = array(pure_exc)
    pure_exc = pure_exc.reshape(7,12)          # 7, which is the number of columns, will be len(country_tmp).
    
    years = ['2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000']
    
    df_exc = DataFrame(pure_exc).transpose()
    df_exc.index = years
    df_exc.columns = country_tmp
    
    print df_exc


    #print pure_exc
    #print len(pure_exc)
        
    #print tmp
    #df_tmp = DataFrame(tmp).transpose()
    #df_tmp.index = ['2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000']
    
    #years = []
    #for i in range(2000,2012):
     #   years.append(str(i))
      #  new_years = []
       # for i in years
    #print years

#""" want each entry to be just the float of exchange rate, cant change it in dataframe, need to change it before forming data frame"""
    #for i in df_tmp.index:
     #   for j in df_tmp.ix[i]:
      #      j = j[1]
       #     j = j.replace(',','')
         #   j = float(j)
           
        
    #print df_tmp


    
    
