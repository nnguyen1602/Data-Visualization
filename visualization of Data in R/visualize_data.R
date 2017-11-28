rm(list=ls());
set.seed(2);

baseDir <- getwd()
dataDir  <- paste(baseDir, "Data", sep="/")
setwd(dataDir)
trainingData <- readRDS(file = "waterDataTraining.RDS")
summary(trainingData)

# quite alot NA
# try to remove NA's values
sum.NA.values<-sum(is.na(trainingData))
any(is.na(trainingData))
number.row <-nrow(trainingData)

#data after remove NA
ndata<- na.omit(trainingData)

# replace the NA values with the lastest values before it
library(zoo)
require(data.table)
replaceNaWithLatest <- function(
  dfIn,
  nameColNa = names(dfIn)[1]
){
  dtTest <- data.table(dfIn)
  setnames(dtTest, nameColNa, "colNa")
  dtTest[, segment := cumsum(!is.na(colNa))]
  dtTest[, colNa := colNa[1], by = "segment"]
  dtTest[, segment := NULL]
  setnames(dtTest, "colNa", nameColNa)
  return(dtTest)
}
ndata <- replaceNaWithLatest(trainingData,names(trainingData)[2])
ndata <- replaceNaWithLatest(ndata,names(ndata)[3])
ndata <- replaceNaWithLatest(ndata,names(ndata)[4])
ndata <- replaceNaWithLatest(ndata,names(ndata)[5])
ndata <- replaceNaWithLatest(ndata,names(ndata)[6])
ndata <- replaceNaWithLatest(ndata,names(ndata)[7])
ndata <- replaceNaWithLatest(ndata,names(ndata)[8])
ndata <- replaceNaWithLatest(ndata,names(ndata)[9])
ndata <- replaceNaWithLatest(ndata,names(ndata)[10])
summary(ndata)

# line plot for each of indicators
par(mfrow=c(3,2))
plot(ndata$Time~ndata$Time,type="l") # interesting
plot(ndata$Tp~ndata$Time,type="l")
plot(ndata$Cl~ndata$Time,type="l")
plot(ndata$pH~ndata$Time,type="l")
plot(ndata$Redox~ndata$Time,type="l")
plot(ndata$Leit~ndata$Time,type="l")

# draw all of them in the same scale (not suitable)
library(ggplot2)
library(reshape)
data <- data.frame(time=ndata$Time, ndata$Tp, ndata$Cl, ndata$pH, ndata$Redox, ndata$Leit)
data <- data.frame(time=ndata$Time, ndata$Tp, ndata$pH)
data <- data.frame(time=ndata$Time, ndata$pH)
data <- data.frame(time=ndata$Time, ndata$Cl)
Molten <- melt(data, id.vars = "time")
ggplot(Molten, aes(x = time, y = value, colour = variable)) + geom_line()








