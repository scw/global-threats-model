Quick overview of the modeling process (more docs to come):

* Import all of the raw threat and habitat rasters as "prethreat_*" and "prehabitat_*"
* Run scale_threats.py and scale_habitats.py to scale them 0 to 1
* There should be a bunch of "threat_*" and habitat_* layers, use these names in the header of your matrix file (csv)
* Run generate_combos.py on the matrix file which will generate a combined raster for each threat/habitat combo

These steps should only need to be done ONCE assuming the models input data doesn't change

To run iterations of the model, adjust the matrix file (if needed) and run :
  threat_model.py matrixi1.csv model1output




