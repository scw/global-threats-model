r.out.gdal input=core_matrix_all_habs format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/core_matrix_all_habs.tif
python threat_model.py terrestrial_all_habs.csv terrestrial_all_habs
r.out.gdal input=terrestrial_all_habs format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/terrestrial_all_habs.tif
python threat_model.py acid.csv  acid
r.out.gdal input=acid format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/acid.tif
python threat_model.py artisanal.csv artisanal
r.out.gdal input=artisanal format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/artisanal.tif
python threat_model.py coral.csv coral
r.out.gdal input=coral format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/coral.tif
python threat_model.py core_matrix.csv core_matrix
r.out.gdal input=core_matrix format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/core_matrix.tif
python threat_model.py fert.csv fert
r.out.gdal input=fert format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/fert.tif
python threat_model.py fish1.csv fish1
r.out.gdal input=fish1 format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/fish1.tif
python threat_model.py fish2.csv fish2
r.out.gdal input=fish2 format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/fish2.tif
python threat_model.py fish3.csv fish3
r.out.gdal input=fish3 format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/fish3.tif
python threat_model.py fish4.csv fish4
r.out.gdal input=fish4 format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/fish4.tif
python threat_model.py fish5.csv fish5
r.out.gdal input=fish5 format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/fish5.tif
python threat_model.py flares.csv flares
r.out.gdal input=flares format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/flares.tif
python threat_model.py h0t060.csv h0t060
r.out.gdal input=h0t060 format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/h0t060.tif
python threat_model.py h2000p.csv h2000p
r.out.gdal input=h2000p format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/h2000p.tif
python threat_model.py h200to2000.csv h200to2000
r.out.gdal input=h200to2000 format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/h200to2000.tif
python threat_model.py h60to200.csv h60to200
r.out.gdal input=h60to200 format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/h60to200.tif
python threat_model.py impv.csv impv
r.out.gdal input=impv format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/impv.tif
python threat_model.py invasives.csv invasives
r.out.gdal input=invasives format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/invasives.tif
python threat_model.py kelp.csv kelp
r.out.gdal input=kelp format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/kelp.tif
python threat_model.py mgroves.csv mgroves
r.out.gdal input=mgroves format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/mgroves.tif
python threat_model.py pdeep.csv pdeep
r.out.gdal input=pdeep format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/pdeep.tif
python threat_model.py pelagic.csv pelagic
r.out.gdal input=pelagic format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/pelagic.tif
python threat_model.py pest.csv pest
r.out.gdal input=pest format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/pest.tif
python threat_model.py pollution.csv pollution
r.out.gdal input=pollution format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/pollution.tif
python threat_model.py pop.csv pop
r.out.gdal input=pop format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/pop.tif
python threat_model.py s0to60.csv s0to60
r.out.gdal input=s0to60 format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/s0to60.tif
python threat_model.py s2000p.csv s2000p
r.out.gdal input=s2000p format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/s2000p.tif
python threat_model.py s200to2000.csv s200to2000
r.out.gdal input=s200to2000 format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/s200to2000.tif
python threat_model.py s60to200.csv s60to200
r.out.gdal input=s60to200 format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/s60to200.tif
python threat_model.py seagrass.csv seagrass
r.out.gdal input=seagrass format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/seagrass.tif
python threat_model.py seamounts.csv seamounts
r.out.gdal input=seamounts format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/seamounts.tif
python threat_model.py shipping.csv shipping
r.out.gdal input=shipping format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/shipping.tif
python threat_model.py sst.csv sst
r.out.gdal input=sst format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/sst.tif
python threat_model.py uv.csv uv
r.out.gdal input=uv format=GTiff type=Float32 output=/mnt/storage/marine_threats_final/finished_models/tifs/full_extent/uv.tif

