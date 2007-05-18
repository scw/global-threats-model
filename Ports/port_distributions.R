# port_distibutions.R
# calculate the distributions of our port data:
# port pollution        <aggregate formula>
# invasive species      <aggregate formula>

# load the maptool library, parses dbfs
library(maptools)

# store the current directory
initial.dir<-getwd()
# data directory
setwd("/mnt/storage/marine_threats/work/Ports/corrected_ports")

# output file
sink("ports_distributions.log")

# load dbf
portinv  <- read.dbf("invasives/ports_snapped_20km.dbf")
portpol <- read.dbf("pollution/pollution_ports.dbf")

print ("Threshold values")
print ("----------------")
print ("Port Pollution <aggregate formula>:")
classes<-c(0.00005, 0.0001, 0.0005, 0.05,0.10,0.25,0.50,0.75)
pollution<-ifelse(portpol$Pollution == 0, NA, portpol$Pollution)

quantile(sort(pollution), prob=classes)

print ("Invasive Species <aggregate formula>:")
invasives<-ifelse(portinv$Invas == 0, NA, portinv$Invas)
quantile(sort(invasives), prob=classes)

# close up shop
sink()
detach("package:maptools")
setwd(initial.dir)
