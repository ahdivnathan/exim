import pandas
import os
import csv

allfiles = os.listdir('done')

indexData = {}
years = range(1995, 2012)
for filename in allfiles:
    filepath = 'done/' + filename
    csvfile = open(filepath, 'rU')
    filereader = csv.reader(csvfile)
    yearlyData = {}
    for year in years:
    	yearlyData[year] = None
    for row in filereader:
        yearlyData[row[0]] = row[1]
    indexData[filename[0:3]] = yearlyData

indexDataFrame = pandas.DataFrame(indexData).transpose()
