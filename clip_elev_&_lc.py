# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 17:09:58 2020

@author: nmtarr

Description: Similar to clip_habmaps but clip the elevation and land cover
rasters to WV.  Save in "/Data"
"""
# Paths
projDir = "P:/Proj6/GAP-WVBA/"
gapDataDir = "P:/Proj3/USGap/Vert/Model/Data/"
seElev = gapDataDir + "Elev/Elev_se"
neElev = gapDataDir + "Elev/Elev_ne"
seLC = gapDataDir + "LandCover/lcgap_se"
neLC = gapDataDir + "LandCover/lcgap_ne"
wvBoundary = projDir + 'WV_GAPcover/2001/WVworkspace/wv_bound.shp'

import fiona
import rasterio
import rasterio.mask
import rasterio.drivers
import rasterio.merge
import pandas as pd
from rasterio.plot import show

#Merge Elev rasters  
rasterio.merge.merge({seElev,neElev}, bounds=None, res=None, nodata=None, 
                     precision=10, indexes=None, method='first') as out_image :
    out_file = gapDataDir + "Elev/Elev_wv"
    with rasterio.open(out_file, "w", **out_meta) as dest:
        dest.write(out_image)

#Merge LC rasters
rasterio.merge.merge({seLC,neLC}, bounds=None, res=None, nodata=None, 
                     precision=10, indexes=None, method='first') as out_image:
    out_file = gapDataDir + "Elev/LC_wv"
    with rasterio.open(out_file, "w", **out_meta) as dest:
        dest.write(out_image)



shapefile = fiona.open(wvBoundary)
shapes = [feature['geometry'] for feature in shapefile]
rasterio.Env(GDAL_TIFF_INTERNAL_MASK=True) 
 
with rasterio.open(Elev) as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta
    print(src.meta)
    out_meta.update({"driver": "GTiff", "height": out_image.shape[1], 
                     "width": out_image.shape[2], 
                     "transform": out_transform})
    out_file = gapDataDir + "Elev/Elev_wv"
    with rasterio.open(out_file, "w", **out_meta) as dest:
        dest.write(out_image)
        #show(out_image)
print('IT WORKED!!!!')
   
with rasterio.open(LC) as src2:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src2.meta
    print(src.meta)
    out_meta.update({"driver": "GTiff", "height": out_image.shape[1], 
                     "width": out_image.shape[2], 
                     "transform": out_transform})
    out_file2 = gapDataDir + "Elev/LC_wv"
    with rasterio.open(out_file, "w", **out_meta) as dest:
        dest.write(out_image)
        #show(out_image)
        print('IT WORKED!!!!')      