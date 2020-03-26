# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 16:26:40 2020

@author: nmtarr

Description: Clips CONUS GAP habitat maps (summer) to the WV boundary.
"""
import os, sys 
import fiona
import rasterio
import rasterio.mask
import rasterio.drivers
import pandas as pd
import matplotlib
import matplotlib.pyplot
from rasterio.plot import show


# Set paths to data
#projDir = "P:/Proj6/GAP-WVBA/"
#CONUSDir = "P:/Proj3/USGap/Vert/Model/Output/CONUS/01/Summer/"
projDir = "C:/Users/jhpage/"
dataDir = projDir + "Data/"
rangDir = dataDir + 'USGap/Vert/Model/Output/CONUS/01/Summer/'
clipDir = dataDir + 'habmaps'
listDir = dataDir + 'Specieslists/WV_AtlasCodes.csv'
wvBoundary = projDir + 'WV_GAPcover/2001/WVworkspace/wv_bound.shp'

# Get a list of GAP species codes to process

# Loop through the list use species codes to pull map temporarily from database and clip each species' summer habitat map to WV.
# Generates empty list to allow for iteration through codes

shapefile = fiona.open(wvBoundary)
shapes = [feature['geometry'] for feature in shapefile]
rasterio.Env(GDAL_TIFF_INTERNAL_MASK=True)  
df = pd.read_csv(listDir, dtype={'strUC': 'string'}) 
dataset = rangDir + 'bwothx_CONUS_01S_2001v1.tif'
with rasterio.open(dataset) as src: 
    show(src)
#i = df.iloc[21]   
#for i in df['strUC'] : 
        #try:
            #i = i[:1] + i[1:5].upper() + i[-1:]
            #print(i) 
            dataset = rangDir + i + '_CONUS_01S_2001v1.tif'  
            #with rasterio.open(dataset) as src:
                #show(src, 2)
            #with rasterio.open(dataset, mode='w+', driver='GTiff', width=154137, height=97170, count=1, crs= 'EPSG:4269', 
            #transform= 'Affline(30.0, 0.0, -2361141.227, 0.0, -30.0, 3177272.0779999997)', nodata='nan') as src:
                #out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                #out_meta = src.meta
                #print(src.meta)
                #show(out_image)
                #out_image(clipDir+ '/' + i + '_wv.tif')
                #out_meta.update({"driver": "GTiff","height": out_image.shape[1], "width": out_image.shape[2], "transform": out_transform})
                #with rasterio.open(dataset, "w", **out_meta) as dest:
                    #dest.write(out_image)
            print('IT WORKED!!!!')
        except:
            print('Something went wrong with ' + i + '_wv') 




