# %%
import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import cv2

# %% 
##ERROR_MAPPING DATASET

mypath = r'C:/Users/iviac/OneDrive/Escritorio/BOLOGNA_EXCHANGE/raw_data/image_data_&_annot_rename/error_mapping/TB_err_map/'
pngimage = []
txtfiles = []
jsonfiles = []
depthfiles = []

for images in os.listdir(mypath):
 
    # check if the image ends with png
    if (images.startswith("img") & images.endswith(".png")):
        pngimage.append(images)
        
    elif(images.endswith(".txt")):
        txtfiles.append(images)

    elif(images.endswith(".json")):
        jsonfiles.append(images)
    
    elif(images.startswith("depth")):
        depthfiles.append(images)

# %%

fileserr = pd.DataFrame({'IMG': pngimage, 
                         'DEPTH': depthfiles,
                         'TXT': txtfiles,
                         'JSON': jsonfiles},
                         columns= ['IMG', 'DEPTH', 'TXT', 'JSON'])

# %%
##PERSPECTIVE DATASET

mypath = r'C:\Users\iviac\OneDrive\Escritorio\BOLOGNA_EXCHANGE\raw_data\image_data_&_annot_rename\perspective\Presp_Apple'
mypath1 = r'C:\Users\iviac\OneDrive\Escritorio\BOLOGNA_EXCHANGE\raw_data\image_data_&_annot_rename\perspective\Presp_Tball'

pngimage = []
txtfiles = []
jsonfiles = []
depthfiles = []

for images in os.listdir(mypath):
 
    # check if the image ends with png
    if (images.startswith("img") & images.endswith(".png")):
        pngimage.append(images)
        
    elif(images.endswith(".txt")):
        txtfiles.append(images)

    elif(images.endswith(".json")):
        jsonfiles.append(images)
    
    elif(images.startswith("depth")):
        depthfiles.append(images)

for images in os.listdir(mypath1):
 
    # check if the image ends with png
    if (images.startswith("img") & images.endswith(".png")):
        pngimage.append(images)
        
    elif(images.endswith(".txt")):
        txtfiles.append(images)

    elif(images.endswith(".json")):
        jsonfiles.append(images)
    
    elif(images.startswith("depth")):
        depthfiles.append(images)
# %%

filesPersp = pd.DataFrame({'IMG': pngimage, 
                         'DEPTH': depthfiles,
                         'TXT': txtfiles,
                         'JSON': jsonfiles},
                         columns= ['IMG', 'DEPTH', 'TXT', 'JSON'])

filesPersp

# %%
##XYZ_POSITIONING_AND_SIZING_ERROR DATASET

mypath = r'C:\Users\iviac\OneDrive\Escritorio\BOLOGNA_EXCHANGE\raw_data\image_data_&_annot_rename\xyz_positioning_and_sizing_error\2D'
mypath1 = r'C:\Users\iviac\OneDrive\Escritorio\BOLOGNA_EXCHANGE\raw_data\image_data_&_annot_rename\xyz_positioning_and_sizing_error\3D'

pngimage = []
txtfiles = []
jsonfiles = []
depthfiles = []

for images in os.listdir(mypath):
 
    # check if the image ends with png
    if (images.startswith("img") & images.endswith(".png")):
        pngimage.append(images)
        
    elif(images.endswith(".txt")):
        txtfiles.append(images)

    elif(images.endswith(".json")):
        jsonfiles.append(images)
    
    elif(images.startswith("depth")):
        depthfiles.append(images)

for images in os.listdir(mypath1):
 
    # check if the image ends with png
    if (images.startswith("img") & images.endswith(".png")):
        pngimage.append(images)
        
    elif(images.endswith(".txt")):
        txtfiles.append(images)

    elif(images.endswith(".json")):
        jsonfiles.append(images)
    
    elif(images.startswith("depth")):
        depthfiles.append(images)

# %%

filesXYZ = pd.DataFrame({'IMG': pngimage, 
                         'DEPTH': depthfiles,
                         'TXT': txtfiles,
                         'JSON': jsonfiles},
                         columns= ['IMG', 'DEPTH', 'TXT', 'JSON'])
# %%
filesXYZ

# %%

import os
import cv2
import numpy
import matplotlib.pyplot as plt
import json

# file containing the reference data
GROUND_TRUTHING_DATA_PATH = r'C:\Users\iviac\OneDrive\Escritorio\BOLOGNA_EXCHANGE\raw_data\ground_truthing_dataset\Organized_2024_GroundTruth.xlsx'
FOLDER_PATH2D = r'C:\Users\iviac\OneDrive\Escritorio\BOLOGNA_EXCHANGE\raw_data\image_data_&_annot_rename\xyz_positioning_and_sizing_error\2D'
FOLDER_PATH3D = r'C:\Users\iviac\OneDrive\Escritorio\BOLOGNA_EXCHANGE\raw_data\image_data_&_annot_rename\xyz_positioning_and_sizing_error\3D'


gtruth_data = pd.read_excel(GROUND_TRUTHING_DATA_PATH)
# setting the item position as index of the df
gtruth_data = gtruth_data.set_index('item')
gtruth_attributes = gtruth_data.columns  
#print(gtruth_data.loc[1, :])


for idx, row in filesXYZ.iterrows():

    file = str(row['IMG']).split('_')
    trial_code = f'{file[1]}_{file[2]}'
    print(f'{trial_code= }')

    # create the image file path
    im_file = os.path.join(FOLDER_PATH2D, row['IMG'])
    if not os.path.isfile(im_file):
            im_file = os.path.join(FOLDER_PATH3D, row['IMG'])

    #print(im_file)
    # create the annotation path
    ann_file = os.path.join(FOLDER_PATH2D, row['TXT'])
    if not os.path.isfile(ann_file):
            ann_file = os.path.join(FOLDER_PATH3D, row['TXT'])

    # open the json and get the description (item)
    description = 1  # change 

    # get gtruth data
    bbox_gtruth = gtruth_data.iloc[description, :]

    attributes = [attr for attr in gtruth_attributes if attr.find(trial_code) != -1]

    # data referring to the specific object at the give position (that is the json description) on the trial (trial_code)
    bbox_gtruth_data = gtruth_data.loc[description, attributes].copy()

    # removing the trial_code from the attribute name to keep it clear    
    for info in bbox_gtruth_data.index:
        *_, information = info.split('_')
        print(information)

    # open the annotation as df
    ann_df = pd.read_csv(ann_file, names=['cls', 'x', 'y', 'w', 'h'], sep = ' ')  # cls, x, y, w, h (relative)

    #print(ann_df.head(3))
    # open image as RGB
    im = cv2.imread(im_file)[:,:,::-1]
    H, W, c = im.shape

    for idx2, annot in ann_df.iterrows():
        bbox_x = int(annot['x'] * W)
        bbox_y = int(annot['y'] * H)
        bbox_w = int(annot['w'] * W)
        bbox_h = int(annot['h'] * H)

        # transfporm to absolute coordinates
        bbox_abs_x1 = int(bbox_x - (bbox_w / 2))
        bbox_abs_y1 = int(bbox_y - (bbox_h / 2))
        bbox_abs_x2 = int(bbox_x + (bbox_w / 2))
        bbox_abs_y2 = int(bbox_y + (bbox_h / 2))

        #print(bbox_abs_x1, bbox_abs_x2, bbox_abs_y1, bbox_abs_y2)
        # plot bbox absolute coordinates
    
        im[bbox_abs_y1 : bbox_abs_y2, bbox_abs_x1 : bbox_abs_x2] = (255, 0, 0)


    # rotate the image if h > w

    if H < W:
        im = np.rot90(im, k=3)

    plt.imshow(im)
    plt.show()






# # %%

# groundTr = pd.read_excel(GROUND_TRUTHING_DATA_PATH)
# groundTr.columns
# %%
