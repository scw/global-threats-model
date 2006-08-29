plotFertvsPest <- function () {
  library(maptools)
  d <- read.dbf('c:\\workspace\\cia_factbook\\master_table.dbf')
  d.lm <- lm(d$PEST ~ d$FERT)
  plot(d$FERT, d$PEST, main="Average Annual Pesticide Consumption vs. Fertilizer",xlab="Fertilizer(metric tons)",ylab="Pesticides(metric tons)",xlim=c(0,5e+06))
  abline(d.lm)
  summary(d.lm)
}
  
plotLogFertvsPest <- function () {
  library(maptools)
  d <- read.dbf('c:\\workspace\\cia_factbook\\master_table.dbf')
  d.lm <- lm(log(d$PEST) ~ log(d$FERT))
  plot(log(d$FERT), log(d$PEST), main="Average Annual Pesticide Consumption vs. Fertilizer\n (Log Scale)", xlab="Fertilizer -- Log(metric tons)",ylab="Pesticides -- Log(metric tons)")
  abline(d.lm)
  summary(d.lm)
}

plotLogGDPvsFert <- function () {
  library(maptools)
  d <- read.dbf('c:\\workspace\\cia_factbook\\master_table.dbf')
  d.lm <- lm(log(d$FERT) ~ log(d$GDPAG))
  plot(log(d$GDPAG), log(d$FERT), main="Gross Domestic Product from Agriculture\n vs. Fertilizer Consumption\n (Log Scale)", xlab="Agricultural GDP -- Log($)",ylab="Fertilizer -- Log(metric tons)")
  abline(d.lm)
  summary(d.lm)  
}

plotGDPvsFert <- function () {
  library(maptools)
  d <- read.dbf('c:\\workspace\\cia_factbook\\master_table.dbf')
  d.lm <- lm(d$FERT ~ d$GDPAG)
  plot(d$GDPAG,d$FERT, main="Gross Domestic Product from Agriculture\n vs. Fertilizer Consumption", xlab="Agricultural GDP ($)",ylab="Fertilizer (metric tons)")
  abline(d.lm)
  summary(d.lm)  
}

plotLogGDPvsPest <- function () {
  library(maptools)
  d <- read.dbf('c:\\workspace\\cia_factbook\\master_table_area.dbf')
  d.lm <- lm(log(d$PEST) ~ log(d$GDPAG))
  plot(log(d$GDPAG), log(d$PEST), main="Gross Domestic Product from Agriculture\n vs. Pesticide Consumption\n (Log Scale)", xlab="Agricultural GDP -- Log($)",ylab="Pesticide -- Log(metric tons)")
  abline(d.lm)
  summary(d.lm)  
}

plotGDPvsPest <- function () {
  library(maptools)
  d <- read.dbf('c:\\workspace\\cia_factbook\\master_table_area.dbf')
  d.lm <- lm(d$PEST ~ d$GDPAG)
  plot(d$GDPAG,d$PEST, main="Gross Domestic Product from Agriculture\n vs. Pesticide Consumption", xlab="Agricultural GDP ($)",ylab="Pesticide (metric tons)")
  abline(d.lm)
  summary(d.lm)  
}

mlrPestvsAll <- function() {
  library(maptools)
  d <- read.dbf('c:\\workspace\\cia_factbook\\master_table_area.dbf')
  d.lm <- lm(d$PEST ~ d$GDPAG + d$FERT + d$AREA)  
  summary(d.lm)
}

mlrFertvsAll <- function() {
  library(maptools)
  d <- read.dbf('c:\\workspace\\cia_factbook\\master_table_area.dbf')
  d.lm <- lm(d$FERT ~ d$GDPAG + d$PEST + d$AREA)  
  summary(d.lm)
}


logPredict <- function() {
  d <- read.csv('c:\\workspace\\cia_factbook\\master_table_area.csv')

  d.lm <- lm(log(d$PEST) ~ log(d$FERT))
  ## Adjusted R-squared: 0.6914 
  d$pestpredfert <- exp(-1.25832 + 0.79110*log(d$FERT))

  d.lm <- lm(log(d$FERT) ~ log(d$GDPAG))
  ## Adjusted R-squared: 0.6567 
  d$fertpredgdp <-  exp(-13.4064 + 1.0949 *log(d$GDPAG))

  d.lm <- lm(log(d$PEST) ~ log(d$GDPAG))
  ##  Adjusted R-squared: 0.4316
  d$pestpredgdp <-  exp(-12.29785 + 0.88956*log(d$GDPAG))

  d.lm <- lm(log(d$PEST) ~ log(d$GDPAG) + log(d$FERT))
  ## Adjusted R-squared: 0.6954
  d$pestpredgdpandfertpred <- exp(-0.43065 + -0.05227(d$GDPAG) + 0.82308(d$fertpredgdp))

  write.table(d, file = "c:\\workspace\\cia_factbook\\master_table_regression.csv", sep = ",", col.names = NA, qmethod = "double")
  
 }
