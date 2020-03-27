# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 16:26:40 2020

@author: nmtarr

Description: Clips CONUS GAP habitat maps (summer) to the WV boundary.
"""
import fiona
import rasterio
import rasterio.mask
import rasterio.drivers
import pandas as pd
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

shapefile = fiona.open(wvBoundary)
shapes = [feature['geometry'] for feature in shapefile]
rasterio.Env(GDAL_TIFF_INTERNAL_MASK=True)  
df = pd.read_csv(listDir, dtype={'strUC': 'string'}) 
#i = "bWOTHx"  
for i in df['strUC'] : 
    try:
        i = i[:1] + i[1:5].upper() + i[-1:]
        print(i) 
        dataset = rangDir + i + '_CONUS_01S_2001v1.tif'  
        with rasterio.open(dataset) as src:
            out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
            out_meta = src.meta
            print(src.meta)
            #show(out_image)
            out_meta.update({"driver": "GTiff", "height": out_image.shape[1], 
                             "width": out_image.shape[2], 
                             "transform": out_transform})
            out_file = clipDir+ '/' + i + '_wv.tif'
            with rasterio.open(out_file, "w", **out_meta) as dest:
                dest.write(out_image)
                show(out_image)
                print('IT WORKED!!!!')
    except Exception as e:
        print('Something went wrong with ' + i + '_wv') 
        print(e)




