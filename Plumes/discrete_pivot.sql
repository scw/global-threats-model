CREATE OR REPLACE FUNCTION discrete_pivot(master_table text, pct_table text, rastername text) RETURNS integer AS $$
DECLARE
    myclass RECORD;
BEGIN

    FOR myclass IN EXECUTE 'SELECT distinct(class) as class FROM ' || pct_table LOOP
        EXECUTE 'ALTER TABLE ' || master_table || ' ADD COLUMN ' || rastername || myclass.class || ' numeric';
        EXECUTE 'UPDATE ' || master_table || ' SET ' || rastername ||  myclass.class || ' = s.percentage
                   FROM ' || pct_table || ' s
                   WHERE s.class = ' || myclass.class || ' 
                   AND s.fid = ' || master_table || '.fid_join' ;
    END LOOP;

    RETURN 1;
END;
$$ LANGUAGE plpgsql;

