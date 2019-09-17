#!/bin/bash

# Information:
# This script rasterizes one parameter of a given shapefile to match
# the spatial dimensions as well as the array dimensions of
# the clipped Sentinel-2 .tif file.
# Read README.md for information on setting the variables.
#
# full documentation of gdal_rasterize on:
# https://gdal.org/programs/gdal_rasterize.html

# variables to be set:
#
# rasterized parameter
PARAMETER=BOART_N
# spatial reference system code of all_bands.tif
COORD_SYS=EPSG:32633
# extents of all_bands.tif
X_MIN=395859.532
Y_MIN=5619109.477
X_MAX=411159.532
Y_MAX=5640849.477
# name of the shapefile (excluding .shp)
NAME=BK50neu_KL_mitBodenart1904


# path (doesn't need to be changed)
PATH_SHAPEFILE=${PWD}/data/shapefile


echo "rasterize parameter ${PARAMETER} of shapefile..."
gdal_rasterize -a ${PARAMETER} -a_srs ${COORD_SYS} -te ${X_MIN} ${Y_MIN} ${X_MAX} ${Y_MAX} -tr 10 -10 -l ${NAME} ${PATH_SHAPEFILE}/${NAME}.shp ${PATH_SHAPEFILE}/gt_params_files/${PARAMETER}.tif
