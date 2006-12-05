# convert CRU 10 minute climate data to XYZ file
#from Numeric import *

fin = open('f:/dev/geo scripts/grid_10min_pre.dat', 'r')
fout = file('f:/dev/geo scripts/cru_out.csv', 'w')
line = fin.readline().split()
fout.write('Latitude,Longitude,Precip MM per YR\n')

while line:
    
    #print 'lat: %s long: %s' % (line[0], line[1])
    lat = line[0]
    long = line[1]
    precip_values = line[2:14]
    z_value = 0
    
    for i in precip_values:
        z_value = z_value + float(i)
        
    fout.write("%s,%s,%.2f\n" % (lat, long, z_value))
    line = fin.readline().split()

print "file sucessfully written out.\n"    
fout.close()
