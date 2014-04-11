import pandas
import os
import csv

allfiles = os.listdir('done')

indexData = {}
for filename in allfiles:
    filepath = 'done/' + filename
    csvfile = open(filepath, 'rU')
    filereader = csv.reader(csvfile)
    yearlyData = {}
    for row in filereader:
        yearlyData[row[0]] = row[1]
    indexData[filename[0:3]] = yearlyData

indexDataFrame = pandas.DataFrame(indexData).transpose()
