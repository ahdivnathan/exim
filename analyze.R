source("./clean.R")

# Use the functions from clean.R to create instances of the data frames in this script

indexData = gatherIndexData()
co2Emissions = getCO2Emissions()
exportsGrowth = getExportsGrowth()
gdpGrowth = getGDPGrowth()
gdSaving = getGDSaving()
infantMortality = getInfantMortality()
netMigration = getNetMigration()
realInterestRates = getRealInterestRates()
exchangeData = gatherExchangeData()
trade = getTradeIndex()
tradeIndex = trade[,colSums(is.na(trade)) != nrow(trade)]

# Now we will create new Data Frames that take slices of the trade Data Frame such that
# we can easily regress trade on our macroeconomic indicators.  The new Data Frames
# will be specific to each indicator

sliceTrade = function(df) {
  indCols = colnames(df)
  tradeCols = colnames(tradeIndex)
  commonCols = intersect(indCols, tradeCols)
  
  indRows = rownames(df)
  tradeRows = rownames(tradeIndex)
  commonRows = intersect(indRows, tradeRows)
  return(list(df[commonRows, commonCols], tradeIndex[commonRows, commonCols]))
}

indexSlice = sliceTrade(indexData)
co2Slice = sliceTrade(co2Emissions)
exportsSlice = sliceTrade(exportsGrowth)
gdpSlice = sliceTrade(gdpGrowth)
gdsSlice = sliceTrade(gdSaving)
infMortSlice = sliceTrade(infantMortality)
netMigSlice = sliceTrade(netMigration)
realIntSlice = sliceTrade(realInterestRates)
exchangeSlice = sliceTrade(exchangeData)

prepVectors = function(slice) {
  indVector1 = as.vector(as.matrix(slice[[1]]))
  indVector1 = as.numeric(indVector1)
  tradeVector = as.vector(as.matrix(slice[[2]]))
  indVector2 = c()
  tradeVector2 = c()
  for (i in 1:length(indVector1)) {
    if (is.na(indVector1[i]) | is.na(tradeVector[i])) {
    }
    else {
      indVector2 = append(indVector2, indVector1[i])
      tradeVector2 = append(tradeVector2, tradeVector[i])
    }
  }
  return(list(indVector2, tradeVector2))
}

prepVectors2 = function(slice) {
  df1 = slice[[1]]
  df2 = slice[[2]]
  df1 = df1[-1,]
  df2 = df2[-nrow(df2),]
  indVector1 = as.vector(as.matrix(df1))
  indVector1 = as.numeric(indVector1)
  tradeVector = as.vector(as.matrix(df2))
  indVector2 = c()
  tradeVector2 = c()
  for(i in 1:length(indVector1)) {
    if (is.na(indVector1[i]) | is.na(tradeVector[i])) {
    }
    else {
      indVector2 = append(indVector2, indVector1[i])
      tradeVector2 = append(tradeVector2, tradeVector[i])
    }
  }
  return(list(indVector2, tradeVector2))
}

prepVectors3 = function(slice) {
  df1 = slice[[1]]
  df2 = slice[[2]]
  df1 = df1[-nrow(df1),]
  df1 = df1[-nrow(df1),]
  df2 = df2[-1,]
  df2 = df2[-1,]
  indVector1 = as.vector(as.matrix(df1))
  indVector1 = as.numeric(indVector1)
  tradeVector = as.vector(as.matrix(df2))
  indVector2 = c()
  tradeVector2 = c()
  for(i in 1:length(indVector1)) {
    if (is.na(indVector1[i]) | is.na(tradeVector[i])) {
    }
    else {
      indVector2 = append(indVector2, indVector1[i])
      tradeVector2 = append(tradeVector2, tradeVector[i])
    }
  }
  return(list(indVector2, tradeVector2))
}

regressVectors = function(vectors) {
  depVariable = vectors[[1]]
  indVariable = vectors[[2]]
  fit = lm(depVariable ~ indVariable)
  summary(fit)
}

correlateVectors = function(vectors) {
  myMatrix = matrix(vectors[[1]])
  myMatrix = cbind(myMatrix, vectors[[2]])
  cor(myMatrix, use="all.obs", method="pearson")
}

plotVectors = function(vectors) {
  plot(vectors[[1]], vectors[[2]], main="Scatterplot attempt")
}

clusterTrade = function() {
  tradeIndex = t(tradeIndex)
  tradeIndex = tradeIndex[rowSums(is.na(tradeIndex)) == 0,]
  clustered = kmeans(tradeIndex, 5)
  years = 1995:2011
  center1 = clustered$centers[1,]
  center2 = clustered$centers[2,]
  center3 = clustered$centers[3,]
  center4 = clustered$centers[4,]
  center5 = clustered$centers[5,]
  plot(years, center1, type="l", col="red", ylim=c(0, 700), ylab="Center Means", xlab="Years")
  par(new=TRUE)
  plot(years, center2, type="l", col="green", ylim=c(0, 700), ylab="Center Means", xlab="Years")
  par(new=TRUE)
  plot(years, center3, type="l", col="blue", ylim=c(0, 700), ylab="Center Means", xlab="Years")
  par(new=TRUE)
  plot(years, center4, type="l", col="cyan", ylim=c(0, 700), ylab="Center Means", xlab="Years")
  par(new=TRUE)
  plot(years, center5, type="l", col="black", ylim=c(0, 700), ylab="Center Means", xlab="Years")
}

clusterExchange = function() {
  exchangeData = t(exchangeData)
  exchangeData = apply(as.matrix(exchangeData), 1, as.numeric)
  exchangeData = exchangeData[,colSums(is.na(exchangeData)) == 0]
  exchangeData = t(exchangeData)
  clustered = kmeans(exchangeData, 5)
  years = 1995:2011
  center1 = clustered$centers[1,]
  center2 = clustered$centers[2,]
  center3 = clustered$centers[3,]
  center4 = clustered$centers[4,]
  center5 = clustered$centers[5,]
  plot(years, center1, type="l", col="red", ylim=c(0, 700), ylab="Center Means", xlab="Years")
  par(new=TRUE)
  plot(years, center2, type="l", col="green", ylim=c(0, 700), ylab="Center Means", xlab="Years")
  par(new=TRUE)
  plot(years, center3, type="l", col="blue", ylim=c(0, 700), ylab="Center Means", xlab="Years")
  par(new=TRUE)
  plot(years, center4, type="l", col="cyan", ylim=c(0, 700), ylab="Center Means", xlab="Years")
  par(new=TRUE)
  plot(years, center5, type="l", col="black", ylim=c(0, 700), ylab="Center Means", xlab="Years")
}