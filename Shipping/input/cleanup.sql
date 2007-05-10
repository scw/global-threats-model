-- generate a lat-long pair version of the geometry
BEGIN;

ALTER TABLE shipping ADD ll_geom Geometry;
UPDATE shipping set ll_geom = GeometryFromText('Point(' || lon || ' ' || lat || ')', 4326);

COMMIT;

BEGIN;
CREATE TABLE shipping_clean AS
    SELECT gid, lat, lon, id,
           CAST(regexp_replace(date_,
             '([0-9]{2})([0-9]{2})$',
            E'\\1 \\2:00'
           ) AS timestamp) AS date,
           ll_geom AS the_geom
    FROM shipping;
COMMIT;


-- tables for the final cleaned up line and point data
BEGIN;

CREATE TABLE ship_lines 
    (id varchar(15), count int, date_min timestamp, date_max timestamp, the_geom Geometry);

CREATE TABLE ship_points 
    (id varchar(15), date timestamp, the_geom Geometry);

COMMIT;    
