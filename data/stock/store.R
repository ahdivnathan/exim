<<<<<<< HEAD
# Now we want to store the generated csv files from extract.py into data frames in R for easy analysis. The output is a single data frame with rows as years and columns as countries. We have a total of 25 countries and years ranging from 1995 to 2011.

allFiles = list.files(path = "./done")
=======
allFiles = list.files(path = "done")
>>>>>>> e56c2b7aabd4c7b997c76d886996cd29fa61a6a5
countries = c()
new = TRUE
for (i in 1:length(allFiles)) {
	countries[i] = substring(allFiles[i], 1, 3)
	filePath = paste("./done/", allFiles[i], sep = '')
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
colnames(indexes) = countries

# Since the prices are in respective currencies, we normalize them with respect to the first available year (starting from 1995) to a base of 100. This way, our data would show the relative changes only, which is what we are interested in, instead of noisy nominal values in different currencies.

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

print(indexes)
