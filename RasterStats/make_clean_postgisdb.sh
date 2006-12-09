#!/bin/bash

if [ $# -ne 1 ]; then
  echo "make_clean_db.sh database-name"
  exit
fi

dropdb $1
createdb $1
createlang -d $1 plpgsql
psql -d $1 -f /usr/local/share/postgresql/contrib/lwpostgis.sql
psql -d $1 -f /usr/local/share/postgresql/contrib/spatial_ref_sys.sql
psql -d $1 -f /home/perry/scripts/discrete_pivot.sql
