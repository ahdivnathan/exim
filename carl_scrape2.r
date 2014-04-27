#chose the file path
path = "./data/macros/"
files = list.files(path)

#this function returns the formatted dataframe from the csv
getdf = function(filename){
    each = read.csv(paste(path,filename,sep=""))
    each[1] = NULL
    each[2] = NULL
    each[2] = NULL
    names(each)[2:20] = seq(1995,2013)
    each = t(each)
    return(each)
}

#here we create all of the dataframes
co2emissions = getdf(files[1])
exportsGrowth = getdf(files[2])
gdpGrowth = getdf(files[3])
gdSaving = getdf(files[4])
infantMortality = getdf(files[5])
percentMigrantStock = getdf(files[6])
realInterestRate = getdf(files[7])
