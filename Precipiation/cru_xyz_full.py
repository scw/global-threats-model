# convert CRU 10 minute climate data to XYZ file
#from Numeric import *

workspace = 'f:/dev/cru_10m/'
flist = ['dtr', 'reh', 'tmp', 'elv', 'rd0', 'sunp', 'wnd']

for ftype in flist:

    filename_in = workspace + 'grid_10min_' + ftype + '.dat'
    filename_out = workspace + '10m_' + ftype + '.csv'
    
    fin = open(filename_in, 'r')
    fout = file(filename_out, 'w')

    line = fin.readline().split()
    fout.write('Latitude,Longitude,' + ftype + '_avg\n')
    while line:
        lat = line[0]
        long = line[1]
        ftype_values = line[2:]
        z_value = 0
            
        for i in ftype_values:
            z_value = z_value + float(i)

        z_value = z_value / 12
        fout.write("%s,%s,%.2f\n" % (lat, long, z_value))
        line = fin.readline().split()
        
    fout.close()
    print "file " + filename_out + " successfully written out.\n"    