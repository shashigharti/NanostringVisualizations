python georeference_scans.py
terracotta optimize-rasters --overwrite -o opt_tifs raw_tifs/*.tif
rm -r raw_tifs/*.tif
