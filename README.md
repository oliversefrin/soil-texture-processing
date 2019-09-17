[![DOI](https://zenodo.org/badge/209043786.svg)](https://zenodo.org/badge/latestdoi/209043786)

![GitHub](https://img.shields.io/github/license/oliversefrin/soil-texture-processing)

# Processing Sentinel-2 images and Shapefiles with GDAL

This git repository provides tools to generate training and classification data for machine learning purposes from multispectral Sentinel-2 satellite images and and a .shp file that lies in the area of the Sentinel-2 image.

Training data can be randomly split into train, test and validation tiles resulting in the example image shown below.

**License:** [3-Clause BSD license](LICENSE)

**Authors:**

* [Oliver Sefrin](https://github.com/oliversefrin)
* [Felix M. Riese](https://github.com/felixriese)
* [Sina Keller](https://github.com/sinakeller)

**Citation:** See [citation](#citation) and [bibliography.bib](bibliography.bib).

<img src="/data/training_data/subset_split_map.png" alt="Example image of a subset split map" title="Example image of a subset split map" style="zoom:15%; float: center;" />

## Content

1. [Usage Instructions](#usage-instructions)
2. [Files and file structure](#files-and-file-structure)
3. [Scripts](#scripts)



<a name="usage-instructions">

## 1. Usage Instructions

</a>

**How to use this repository?**

1. Install Python 3, e.g. with [Anaconda](https://www.anaconda.com/)

2. Install the required packages

   > conda install --file requirements.txt

3. Execute the `.py` and `.sh` in the terminal

4. To open and execute the Jupyter Notebook `05_subset_split.ipynb`:

   1. Start jupyter

      > jupyter notebook

   2. Open the notebook folder in this repository in the Jupyter browser and select the notebook `05_subset_split.ipynb`



<a name="files-and-file-structure">

## 2. Files and file structure

</a>

To operate the scripts easily, the file structure should be held as indicated.

As such the `.shp` file and all auxiliary files are in subdirectory *shapefile* (without further subdirectories).

An `overallshape.shp` file (plus its auxiliary files) that contains the shape of the area in the shapefile is needed, there's a separate subdirectory *overallshape* to put it.

Finally, the Sentinel-2 data just needs to be unzipped and the whole folder should be moved to the subdirectory of *sentinel* corresponding to the processing level.



<a name="scripts">

## 3. Scripts

</a>

#### 01_clip_sentinel.sh

##### Usage

Execute the script as

`./01_clip_sentinel.sh DATE LEVEL`

with *DATE*: date of the Sentinel-2 image

and *LEVEL*: its processing level (either L1C or L2A are valid).

No paths or parameters need to be changed.

##### Description

The output file `DATE_LEVEL_all_bands.tif` contains all bands of the processing level in a .`tif` file that is cropped to the dimensions of the shapefile area. and is saved in the directory of the Sentinel-2 image.



#### 02_rasterize_shapefile.sh

##### Usage

Execute the script as

`./02_rasterize_shapefile.sh`.

Be aware that variables need to be set specifically in the script.

##### Description

Rasterize one parameter from a given `.shp` file as a Geotiff file that matches the geospatial dimensions of the previously created `DATE_LEVEL_all_bands.tif`.

The parameter is expected to be of type `float`. If this is not the case, simply open the shapefile in a Jupyter Notebook as a pandas Dataframe using *geopandas* and add a column in which you converted the desired parameter to `float`.

The variable *PARAMETER* has to be the name of the column in the DataFrame you want to rasterize.
The variable *NAME* is expected to be the name of the shapefile (without the `.shp` file ending).
The variables *X_MIN*, *X_MAX*, *Y_MIN*, *Y_MAX* and *COORD_SYS* have to match the corresponding values of the file `DATE_LEVEL_all_bands.tif`. To get these values, open a terminal in the subdirectory of the Sentinel-2 image containing the `DATE_LEVEL_all_bands.tif` file. There, execute the command

`gdalinfo DATE_LEVEL_all_bands.tif` (of course, replace DATE and LEVEL with the actual values).


#### 03_create_area_tif.py

##### Usage

Simply execute the script as

`python 03_create_area_tif.py`.

Once executed, there is no need to create another `area.tif` another time (assuming neither the shapefile nor the Sentinel-2 image tile have changed).

##### Description

Creates the file `area.tif` in the subdirectory *data/shapefile/gt_params_files*.

This Geotiff file consists of one band containing only ones and zeros: ones in the intersection of the satellite image and the shapefile area, zeros for pixel outside either one or both of these areas.

Such a `.tif` file might come in handy at several occasions as it masks the area of interest.


#### 04_merge_tifs.sh

##### Usage

Execute the script as

`./04_merge_tifs.sh DATE LEVEL USE`

with *DATE* (YYYYMMDD), *LEVEL* (L1C/L2A) being the date and processing level of the Sentinel-2 image.

If *USE*=*TRAIN*, the rasterized Ground Truth created by script no. 02 will be added as the last band to `DATE_LEVEL_all_bands.tif`.
If *USE*=*NEW*, the `area.tif` will be added as the last band to `DATE_LEVEL_all_bands.tif`.

##### Description

This script allows to merge the preprocessed Sentinel-2 image file, `DATE_LEVEL_all_bands.tif`, either with the Ground Truth `.tif` file or the `area.tif`.
The output `DATE_LEVEL_merged.tif` is saved in a separate *DATE_data* subdirectory of either *data/training_data* or *data/new_data*, depending of the intended use.

Setting *USE*=*TRAIN* allows to use the result for training of a Machine Learning model with the Sentinel-2 bands as X and the Ground Truth as Y.
*USE*=*NEW* on the other hand allows to predict on the Sentinel-2 image whilst the band representing the `area.tif` restricts the area of interest.


#### 05_subset_split.ipynb

##### Usage

Start a Jupyter Kernel as described above ([Usage Instructions](#usage-instructions), point 4.) and open the `05_subset_split.ipynb` Notebook.

Set the variables in section *1. Set variables and dictionaries*.

Execute the cells in order, note that subsection 3.2 is purely optional and project specific and subsection 3.5 is meant as an example which doesn't need to be executed.

##### Description

This script uses a `DATE_LEVEL_merged.tif`  that has the Ground Truth as the last band, i.e. that is training data. The pixel of the `.tif` file are separated in tiles of specified tilesize with a specified gap between the tiles. Next, the tiles are randomly (although with fixed random seed for repeatability) split into 3 subsets *train*, *test* and *validation* and saved as .csv files. The fraction of train, test and validation data can be specified as well.

Subset splits are saved in the subdirectory *data/training_data/DATE_data/* as *DATE_LEVEL_tilesize_TILESIZE_train.csv* (with *DATE, LEVEL, TILESIZE*: the corresponding values) or with *validation* or *test*, respectively.

#### 06_create_full_csv.py

##### Usage

Execute the script as

`python 06_create_full_csv.py DATE LEVEL`

with *DATE* (YYYYMMDD), *LEVEL* (L1C/L2A) being the date and processing level of the Sentinel-2 image.

##### Description

This script creates a `.csv` file that contains the Sentinel-2 data. Each column is a Sentinel-2 band, each row is a single pixel.

The output `.csv` file is saved in the subdirectory *data/new_data/DATE_data* with *DATE* being the date specified upon calling the script.

Please note that only pixel within the area of interest, i.e. pixel with value 1 in the `area.tif`, are saved in the `.csv` file. Therefore, the number of rows is expected to be smaller than the total number of pixel in the `DATE_LEVEL_merged.tif` (*height\*width*).

To go back from a 1-dimensional list of pixel to a 2D array (i.e. a map), use the indices in the `.csv` file. These number the pixel as if the 2D array was flattened row by row (C-ordering), which it was in fact. Hence, to get the row and column number, use the following (pseudo-)code:

`row_nr = index_nr // width`

`col_nr = index_nr % width`


## Citation

TODO
