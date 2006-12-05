# convert CRU 10 minute climate data to XYZ file
#from Numeric import *

fin = open('f:/dev/geo scripts/grid_10min_pre.dat', 'r')
fout = file('f:/dev/geo scripts/cru_precip.csv', 'w')
cout = file('f:/dev/geo scripts/cru_precip_cv.csv', 'w')
line = fin.readline().split()
fout.write('Latitude,Longitude,MM_YR\n')
cout.write('Latitude,Longitude,CV_AVG\n')

while line:
    
    #print 'lat: %s long: %s' % (line[0], line[1])
    lat = line[0]
    long = line[1]
    precip_values[2:14]
    cv_values = line[15:]
    z_value = 0
    cv_value = 0
    
    for i in precip_values:
        z_value = z_value + float(i)

    for j in cv_values:
        cv_value = cv_value + float(j)

    cv_value = cv_value / 12        
    fout.write("%s,%s,%.2f\n" % (lat, long, z_value))
    cout.write("%s,%s,%.2f\n" % (lat, long, cv_value))
    line = fin.readline().split()

print "file sucessfully written out.\n"    
fout.close()
cout.close()
