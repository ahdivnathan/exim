# This file will take the scraped data from our csv files and put it into R Data Frames
# for easy analysis.  The output of each function will be a Data Frame with years for
# rows and countries for columns.  Additionally, we will make some basic plots to identify
# areas of analysis that we should explore more thoroughly.

gatherIndexData = function() {
  # This function will gather the stock index data for each of the 25 countries whose
  # index data we have scraped and placed in csv files.  We will pull the data from
  # each csv and clean it such that we have relative changes rather than nominal values
  
  indexFiles = list.files(path = "./data/stock/done")
  indexCountries = c()
  new = TRUE
  for (i in 1:length(indexFiles)) {
    indexCountries[i] = substring(indexFiles[i], 1, 3)
    filePath = paste("./data/stock/done/", indexFiles[i], sep="")
    rawData = read.csv(filePath, header=FALSE)
    startYear = rawData[1][1,]
    if (startYear != 1995) {
      dummyYears = 1995:(startYear-1)
      V2 = rep(NaN, length(dummyYears))
      dummyData = data.frame(V2)
      prices = rbind(dummyData, rawData[2])
    }
    else {
      prices = rawData[2]
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
  
  # Since the prices are in the countries' respective currencies, we will use annual
  # returns to measure the performance of the index.  This way, our data will show
  # only the relative changes as opposed to the noisy nominal values in different
  # currencies.
  
  for (i in colnames(indexes)) {
    k = 1995
    while (as.character(indexes[i][as.character(k),]) == "NaN") {
      k = k + 1
    }
    
    base = indexes[i][as.character(k),]
    indexes[i][as.character(k),] = NaN
    for (j in (k+1):2011) {
      temp = indexes[i][as.character(j),]
      indexes[i][as.character(j),] = indexes[i][as.character(j),]/base*100
      base = temp
    }
  }
  return(indexes)
}

# Now we will pull the macroeconomic indicator data from the csv files we have gathered
# from the World Bank Macroeconomic Indicators database.  The "gatherMacroData" function
# fits all of our macroeconomic indicators because the data was downloaded in a
# standardized format.  We will be making a function for each indicator so that we can
# import these functions in our analysis script.

gatherMacroData = function(filename) {
  macro = read.csv(filename)
  macro[1] = NULL
  macro[2] = NULL
  macro[2] = NULL
  names(macro)[2:20] = seq(1995, 2013)
  macro = t(macro)
  return(macro)
}

getCO2Emissions = function() {
  return(gatherMacroData("./data/macros/co2emissions.csv"))
}
getExportsGrowth = function() {
  return(gatherMacroData("./data/macros/exportsGSGrowth.csv"))
}
getGDPGrowth = function() {
  return(gatherMacroData("./data/macros/gdpGrowth.csv"))
}
getGDSaving = function() {
  return(gatherMacroData("./data/macros/gdSaving.csv"))
}
getInfantMortality = function() {
  return(gatherMacroData("./data/macros/infantMortality.csv"))
}
getNetMigration = function() {
  return(gatherMacroData("./data/macros/netMigration.csv"))
}
getRealInterestRates = function() {
  return(gatherMacroData("./data/macros/realInterestRate.csv"))
}

# Now we will pull the exchange rate data from the csv files we have gathered from
# Oanda, an open source ForEx database.

gatherExchangeData = function() {
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
  return(exchanges)
}

# Now we will gather the trade data that we have stored in the csv files.  Each of the
# csv files contains the variance of the particular category for each country in each
# year.  We will gather the trade data in order to understand how diversity of trade
# affects countries' economic performance

gatherTradeData = function(filename) {
  trade = read.csv(filename)
  years = 1995:2011
  rownames(trade) = years
  return(trade)
}

getExportPartnerVariances = function() {
  return(gatherTradeData("./data/trade/export_part.csv"))
}
getExportProductVariances = function() {
  return(gatherTradeData("./data/trade/export_prod.csv"))
}
getImportPartnerVariances = function() {
  return(gatherTradeData("./data/trade/import_part.csv"))
}
getImportProductVariances = function() {
  return(gatherTradeData("./data/trade/import_prod.csv"))
}
getTradeIndex = function() {
  return(gatherTradeData("./data/trade/trade_index.csv"))
}