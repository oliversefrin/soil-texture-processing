"""
Create a .csv file that contains the Sentinel-2 values
with the bands as columns and the indivual pixel as rows.

Call script as
    python 06_create_full_csv.py DATE LEVEL
with
DATE: date of Sentinel-2 image as YYYYMMDD
LEVEL: processing level of Sentinel-2 image (either L1C or L2A)
"""

import sys
import numpy as np
import pandas as pd
from skimage.io import imread

# arguments upon executing script
date = sys.argv[1]
level = sys.argv[2]

print(f'Open {date}_{level}_merged.tif and convert pixel in area to .csv file...', end=' ')

# read tif
data = imread(f'data/new_data/{date}_data/{date}_{level}_merged.tif')
height, width = data.shape[0], data.shape[1]

if level == 'L1C':
    bands = ['b1', 'b2', 'b3',
             'b4', 'b5', 'b6',
             'b7', 'b8', 'b9',
             'b10', 'b11', 'b12',
             'b8a']
elif level == 'L2A':
    bands = ['b1', 'b2', 'b3',
             'b4', 'b5', 'b6',
             'b7', 'b8', 'b9',
             'b11', 'b12', 'b8a',
             'AOT', 'WVP', 'CLD',
             'SCL', 'SNW']
else:
    print(f'{level} is not a valid LEVEL argument, choose either L1C or L2A.')

# flatten array from shape (height, width, channels) to (height*width, channels)
data_flat = np.zeros((height*width, len(bands)+1))

for i in range(len(bands)+1):
    data_flat[:, i] = data[:, :, i].flatten()

# transform to pd.DataFrame
df = pd.DataFrame(data=data_flat,
                  columns=bands+['is_in_area'])

# drop pixel outside of area of interest
df = df[df['is_in_area']==1]
df = df.drop(columns=['is_in_area'])

# save as csv
df.to_csv(f'data/new_data/{date}_data/{date}_{level}_full.csv',
          sep=',',
          encoding='utf-8')

print('done.')
