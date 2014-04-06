import pandas
import os

allfiles = os.listdir('done')

indexData = {}
for filename in allfiles:
    filepath = 'done/' + filename
    indexData[filename[0:3]] = pandas.read_csv(filepath, header = None)
