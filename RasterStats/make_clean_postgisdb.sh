#!/bin/bash

if [ $# -ne 1 ]; then
  echo "make_clean_postgisdb.sh database-name"
  exit
fi

export POSTGIS_SRC=/usr/local/src/postgis-1.2.1/
export USER=postgres

dropdb $1 

createdb $1 -U $USER

createlang -d $1 plpgsql

psql -d $1 -f ${POSTGIS_SRC}/lwpostgis.sql

psql -d $1 -f ${POSTGIS_SRC}/spatial_ref_sys.sql

psql -d $1 -f discrete_pivot.sql
