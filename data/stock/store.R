allFiles = list.files(path = "./done")
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

print(indexes)
