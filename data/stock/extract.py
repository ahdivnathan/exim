import csv
import ystockquote

def googleExtract(country):
	pass


def csvExtract(filename, country):
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
