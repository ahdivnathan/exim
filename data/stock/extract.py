import csv
import ystockquote

# We first define the functions that we will call, depending where the data
# will be available. These are namely Google finance, manually downloaded csv
# files, or Yahoo finance.

def googleExtract(country):

# We will define this function if we do not have sufficient number of
# countries/amount of data, since this requires text-scrapping.

	pass


def csvExtract(filename, country):

# This function takes a previously downloaded csv file on the historical daily
# prices, and determine the average price within each year, storing these
# averages into another csv file in a separate folder.

	rawdata = []
	filepath = 'manual/' + filename
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

	with open('done/' + country + '.csv', 'w') as file1:
		file1write = csv.writer(file1, delimiter = ',')
		file1write.writerows(data)

	file1.close()

def yahooExtract(ticker, country):

# This function uses the built-in python library 'ystockquote', which inquires
# historical prices and return them as dictionaries. We then determine the
# average prices within each year, storing these averages into a csv file in a
# separate folder.

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

	with open('done/' + country + '.csv', 'w') as file1:
		file1write = csv.writer(file1, delimiter = ',')
		file1write.writerows(data)

	file1.close()

def getIndexPrices(filename):

# Now that we have defined all functions required, we run through a previously
# defined csv file that refers each country to its stock index data source. We
# also use the standard 3-letter country codes when making new csv files.

	indexes = {}

	csvfile = open(filename,'rU')
	reader = csv.reader(csvfile)
	for row in reader:
		indexes[row[0]] = row[1:]

	countryCodes = {}
	csvfile2 = open('country_codes.txt', 'rU')
	reader2 = csv.reader(csvfile2)
	for row in reader2:
		countryCodes[row[1].lower()] = row[0]

	csvfile2.close()

	for country in indexes.keys():
		countryCode = countryCodes[country.lower()]
		if indexes[country][1] == 'unknown' or indexes[country][1] == 'dow':
			pass
		elif indexes[country][1] == 'google':
			googleExtract(country)
		elif indexes[country][1] == 'manual':
			csvExtract(indexes[country][2], countryCode)
		else:
			yahooExtract(indexes[country][1], countryCode)

	csvfile.close()

getIndexPrices('country indexes.csv')
