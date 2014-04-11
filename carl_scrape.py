import csv
import os
import pandas
#Code for the Macros files in the format from the World Development Indicators

#change the file path
files = os.listdir("C:\Users\Carl\src\exim\data\macros")
path = "C:/Users/Carl/src/exim/data/macros/"

def get_data(filename):
	
#importing the csv and then removing columns and renaming headers

    joy = pandas.read_csv(filename)
    list = range(1995,2014)
    index = range(19)
    list1 = []
    for each in index:
        list1.append(str(list[each]))
    curnames = []
    for each in list1:
        curnames.append(each + ' [YR' + each + ']')
    for num in index:
        joy.rename(columns={curnames[num]:list[num]},inplace=True)
    dropnames=['Country Name','Indicator Name','Indicator Code']
    for each in dropnames:
        joy.pop(each)
    joy = joy.transpose()
    return joy
    

fl = len(files)
flr = range(fl)
dfdict = {}
names = []
dflist = []
for filename in files:
    names.append('df_'+ filename)
    dflist.append(get_data(path+filename))

length = len(names)
lenr = range(length)
for i in lenr:
    dfdict[names[i]] = dflist[i]



    



    


