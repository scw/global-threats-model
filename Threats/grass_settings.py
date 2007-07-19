#!/usr/bin/env python

from socket import gethostname

# global settings
settings  = {'GRASS_GUI' : 'TEXT'}

ebm = {
    'PATH' : '/usr/local/grass-6.3.cvs/bin:/usr/local/grass-6.3.cvs/scripts:/usr/local/bin:/bin:/usr/bin',
    'GRASS_VERSION' : '6.3.cvs',
    'GISBASE': '/usr/local/grass-6.3.cvs',
    'LD_LIBRARY_PATH' : '/usr/local/grass-6.3.cvs/lib',
}

helios = {
    'PATH' : '/opt/grass/grass-6.0.2/bin:/opt/grass/grass-6.0.2/scripts:/usr/kerberos/bin:/opt/FWTools/bin_safe:/usr/local/bin:/bin:/usr/bin:/usr/X11R6/bin:/opt/bin:/opt/matlab/2007a/mexnc:',
    'GRASS_VERSION' : '6.0.2',
    'GISBASE' : '/opt/grass/grass-6.0.2',
    'LD_LIBRARY_PATH' : '/opt/grass/grass-6.0.2/lib'
}

rocks = {
    'PATH' : '/usr/lib/grass-6.0.0/bin:/usr/lib/grass-6.0.0/scripts:/opt/gridengine/bin/lx26-x86:/usr/kerberos/bin:/opt/gridengine/bin/lx26-x86:/usr/local/bin:/bin:/usr/bin:/usr/X11R6/bin:/opt/ganglia/bin:/opt/ganglia/sbin:/opt/rocks/bin:/opt/rocks/sbin',
    'GRASS_VERSION' : '6.0.0',
    'GISBASE': '/usr/lib/grass-6.0.0',
    'LD_LIBRARY_PATH' : '/usr/lib/grass-6.0.0/lib',
}

host = gethostname().split('.')[0]

# known hosts:
hosts = ['ebm', 'helios']

if host in hosts:
    settings.update(eval(host))
else:
    settings.update(rocks)
