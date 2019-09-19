"""
Create a .tif file that shows the area of interest.

Only pixel with non-zero values for both the .tif generated from the shapefile
and the .tif processed from the Sentinel-2 image get value 1,
other pixel get value 0.
Basically, the area.tif generated is the logical conjunction
of the shapefile and the Sentinel-2 image.

Checking for zero values in the Sentinel-2 image has the
purpose of restricting the area.tif to the inside of the Sentinel-2 image.
As the spectral intensities never quite reach 0 even for low reflectance,
this procedure shouldn't falsely exclude pixel within the area of the
Sentinel-2 image.
"""

from glob import glob
import numpy as np
import rasterio

print('creating area.tif...', end=' ')

# search for the parameter tiff
tif_filename = glob('data/shapefile/gt_params_files/*.tif')[0]
# or set its name by hand:
# tif_name = './data/shapefile/gt_params_files/NAME.tif'

# same for all_bands.tif
# it doesn't matter, which date or processing level is chosen
# in the case of multiple Sentinel-2 images
all_bands_filename = glob('data/sentinel/*/*/*_all_bands.tif')[0]


# open tiff files
shape_data = rasterio.open(tif_filename).read(1)

sentinel_tif = rasterio.open(all_bands_filename)
sentinel_meta = sentinel_tif.profile
# only first sentinel band is checked for non-zero values
sentinel_data = sentinel_tif.read(1)

for i in range(shape_data.shape[0]):
    for j in range(shape_data.shape[1]):
        if shape_data[i, j] != 0 and sentinel_data[i, j] != 0:
            shape_data[i, j] = 1
        else:
            shape_data[i, j] = 0

# write the new area.tif
new_dataset = rasterio.open('data/shapefile/gt_params_files/area.tif', 'w',
                            driver=sentinel_meta['driver'],
                            height=shape_data.shape[0],
                            width=shape_data.shape[1],
                            count=1,
                            dtype=shape_data.dtype,
                            crs=sentinel_meta['crs'],
                            transform=sentinel_meta['transform'])

new_dataset.write(shape_data, 1)

new_dataset.close()
print('done.')
