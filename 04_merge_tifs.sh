#!/bin/bash

#############################
## preliminary information ##
#############################
# open script as './04_merge_tifs.sh DATE LEVEL USE'
# DATE as YYYYMMDD without quotes
# LEVEL: processing level of the sentinel data, either L1C or L2A
# USE: either TRAIN to generate training data (parameter files are appended)
#      or NEW to generate data for classfication (area file is appended)
DATE=$1
LEVEL=$2
USE=$3

PARAM=BOART_N

###############
## set paths ##
###############
# get path of current directory
CHDIR=$PWD

# set path to Bodenart tif files
PATH_TIF=${CHDIR}/data/shapefile/gt_params_files

if [ ${USE} = TRAIN ]
then
  PATH_DATA=${CHDIR}/data/training_data/${DATE}_data
else
  PATH_DATA=${CHDIR}/data/new_data/${DATE}_data
fi

if [ ! -d ${PATH_DATA} ]
then
  mkdir ${PATH_DATA}
fi


# set path to all_bands.tif:
#
PATH_SENTINEL=${CHDIR}/data/sentinel/level_${LEVEL}
# find corresponding subdirectory by looking for the right date
FILE_DIR=$( ls ${PATH_SENTINEL} | egrep ${DATE} )
# build full path to ..._all_bands.tif
PATH_SENTINEL=${PATH_SENTINEL}/${FILE_DIR}

# merge files
if [ ${USE} = TRAIN ]
then
  echo
  echo "merge sentinel file with rasterized file of parameter ${PARAM}..."
  gdal_merge.py -separate -of GTiff -ot float64 -o ${DATE}_${LEVEL}_merged.tif ${PATH_SENTINEL}/${DATE}_${LEVEL}_all_bands.tif ${PATH_TIF}/${PARAM}.tif
else
  echo
  echo "merge sentinel file with area.tif..."
  gdal_merge.py -separate -of GTiff -ot float64 -o ${DATE}_${LEVEL}_merged.tif ${PATH_SENTINEL}/${DATE}_${LEVEL}_all_bands.tif ${PATH_TIF}/area.tif
fi

mv ${DATE}_${LEVEL}_merged.tif ${PATH_DATA}
