# This file will take the scraped data from our csv files and put it into R Data Frames for easy analysis.  The output of each function will be a Data Frame with years for rows and countries for columns.  Additionally, we will make some basic plots to identify areas of analysis that we should explore more thoroughly.

indexFiles = list.files(path = "./data/stock/done")
indexCountries = c()
new = TRUE
for (i in 1:length(indexFiles)) {
  indexCountries[i] = substring(indexFiles[i], 1, 3)
  filePath = paste("./data/stock/done/", indexFiles[i], sep='')
  rawData = read.csv(filePath, header = FALSE)
  startYear = rawData[1][1,]
  if (startYear != 1995) {
    dummyYears = 1995:(startYear-1)
    V2 = rep(NaN, length(dummyYears))
    dummyData = data.frame(V2)
    prices = rbind(dummyData, rawData[2])
  }
  if (new == TRUE) {
    indexes = prices
    new = FALSE
  }
  else {
    indexes = cbind(indexes, prices)
  }
}

years = 1995:2011
rownames(indexes) = years
colnames(indexes) = indexCountries

# Since the prices are in the countries' respective currencies, we normalize them with respect to the first available year (1995 or later) with a base of 100.  This way, our data will show only the relative changes, which is what we are interested in, rather than the noisy nominal values in different currencies.

for (i in colnames(indexes)) {
  k = 1995
  while (as.character(indexes[i][as.character(k),]) == "NaN") {
    k = k + 1
  }
  base = indexes[i][as.character(k),]
  indexes[i][as.character(k),] = 100
  for (j in (k+1):2011) {
    indexes[i][as.character(j),] = indexes[i][as.character(j),]/base*100
  }
}
    
# Now we will pull the macroeconomic indicator data from the csv files we have gathered from the World Bank Macroeconomic Indicators database.  The "gatherMacroData" function fits all of our macroeconomic indicators because the data was downloaded in a standardized format.

macroPath = "./data/macros/"
macroFiles = list.files(macroPath)

gatherMacroData = function(filename) {
  macro = read.csv(paste(macroPath, filename, sep=""))
  macro[1] = NULL
  macro[2] = NULL
  macro[2] = NULL
  names(macro)[2:20] = seq(1995, 2013)
  macro = t(macro)
  return(macro)
}

co2Emissions = gatherMacroData(macroFiles[1])
exportsGrowth = gatherMacroData(macroFiles[2])
gdpGrowth = gatherMacroData(macroFiles[3])
gdSaving = gatherMacroData(macroFiles[4])
infantMortality = gatherMacroData(macroFiles[5])
percentMigrantStock = gatherMacroData(macroFiles[6])
realInterestRate = gatherMacroData(macroFiles[7])

# Now we will pull the exchange rate data from the csv files we have gathered from Oanda, an open source ForEx database.

exchangePath = "./data/exchange_rate/"
exchangeFiles = list.files(exchangePath)

exchangeCountries = c()
exchangeNew = TRUE
for (i in 1:length(exchangeFiles)) {
  exchangeCountries[i] = substring(exchangeFiles[i], 1, 3)
  exchangeFilePath = paste("./data/exchange_rate/", exchangeFiles[i], sep="")
  exchangeRawData = read.csv(exchangeFilePath, header = FALSE)
  exchangeRawData = exchangeRawData[-1,]
  exchangeRawData = exchangeRawData[-1,]
  exchangeRawData = exchangeRawData[-1,]
  exchangeRawData = exchangeRawData[-dim(exchangeRawData)[1],]
  exchangeRawData = exchangeRawData[-dim(exchangeRawData)[1],]
  exchangeRawData = exchangeRawData[-dim(exchangeRawData)[1],]
  exchangeRawData = exchangeRawData[c(dim(exchangeRawData)[1]:1),]
  exchangeRawData = exchangeRawData[2]
  if (dim(exchangeRawData)[1]<17) {
    dummyYears = 1:(17-dim(exchangeRawData)[1])
    V2 = rep(NaN, length(dummyYears))
    dummyData = data.frame(V2)
    exchangePrices = rbind(dummyData, exchangeRawData)
  }
  else {
    exchangePrices = exchangeRawData
  }
  if (exchangeNew == TRUE) {
    exchanges = exchangePrices
    exchangeNew = FALSE
  }
  else {
    exchanges = cbind(exchanges, exchangePrices)
  }
}

years = 1995:2011
rownames(exchanges) = years
colnames(exchanges) = exchangeCountries

