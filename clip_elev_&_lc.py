# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 17:09:58 2020

@author: nmtarr

Description: Similar to clip_habmaps but clip the elevation and land cover
rasters to WV.  Save in "/Data"
"""
# Paths
projDir = "P:/Proj6/GAP-WVBA/"
gapDataDir = "P:/Proj3/USGap/Vert/Model/data/"
#seElev = gapDataDir + "Elev/elev_se"
#neElev = gapDataDir + "Elev/elev_ne"
#seLC = gapDataDir + "LandCover/lcgap_se"
#neLC = gapDataDir + "LandCover/lcgap_ne"
seElev = gapDataDir + "Temp/elev_se.tif"
neElev = gapDataDir + "Temp/elev_ne.tif"
seLC = gapDataDir + "Temp/lcgap_se.tif"
neLC = gapDataDir + "Temp/lcgap_ne.tif"
usElev= gapDataDir + "Temp/elev"
usLC= gapDataDir + "Temp/lcgap"
Elev = gapDataDir + "Elev/"
LCov = gapDataDir + "LandCover/"
wvBoundary = projDir + 'WV_GAPcover/2001/WVworkspace/wv_bound.shp'

import fiona
import rasterio
import rasterio.mask
import rasterio.drivers

"""
#Mosaic together NE and SE Landcover data,  should be used with caution as the
#datasets do not match along the edges and this code prioritizes the SE data

import rasterio.merge
from rasterio.merge import merge


src3 = rasterio.open(seElev)
src4 = rasterio.open(neElev)
shapefile = fiona.open(wvBoundary)
shapes = [feature['geometry'] for feature in shapefile]

#Height and Width manually determind from the bounding box. Input was rounded
#down the the nearest number to determine row and column count
srcs_to_mosaic = [src3, src4]
bounds= [-58528.37890609764, 262166.4984406226, 
         2262947.646331542, 3013025.0470320634]
width= ((src3.bounds.left *-1) + (src4.bounds.right))/30.000000000000007
height= ((src4.bounds.top) - (src3.bounds.bottom))/30.000000000000007

arr, out_trans = merge(srcs_to_mosaic, bounds, "", (-int(32768)))
out_mosaic = Elev + "eElev.tif"
with rasterio.open(out_mosaic, "w", "GTiff", 77382, 
                   91695, 1, src3.crs, out_trans, 
                   "int16", (-int(32768)), "", compress= "LZW") as dest:
    dest.write(arr.astype("int16"))
    
rasterio.Env(GDAL_TIFF_INTERNAL_MASK=True)  
with rasterio.open(Elev + "eElev.tif") as src1:
    out_image, out_transform = rasterio.mask.mask(src1, shapes, crop=True)
    out_meta = src1.meta
    print(src1.meta)
    out_meta.update({"driver": "GTiff", "height": out_image.shape[1], 
                     "width": out_image.shape[2], 
                     "transform": out_transform})
    out_file = Elev + "wvElev.tif"
    with rasterio.open(out_file, "w", **out_meta) as dest:
        dest.write(out_image)
print('WV Clipped Succesfully!!')  
 

# Mosiac together NE and SE Landcover data and clip to West Virginia
src5 = rasterio.open(seLC)
src6 = rasterio.open(neLC)
shapefile = fiona.open(wvBoundary)
shapes = [feature['geometry'] for feature in shapefile]

srcs_to_mosaic = [src5, src6]
bounds= [-58521.226999999955, 262172.078, 
         2262947.6463315417, 3013025.047032063]
width= ((src5.bounds.left *-1) + (src6.bounds.right))/30.000000000000007
height= ((src6.bounds.top) - (src5.bounds.bottom))/30.000000000000007

arr, out_trans = merge(srcs_to_mosaic, bounds, "", (-int(32768)))
out_mosaic = LCov + "eLCov.tif"
with rasterio.open(out_mosaic, "w", "GTiff", 77382, 
                   91695, 1, src5.crs, out_trans, 
                   "int16", (-int(32768)), "", compress= "LZW") as dest:
    dest.write(arr.astype("int16"))
    
rasterio.Env(GDAL_TIFF_INTERNAL_MASK=True)  
with rasterio.open(LCov + "eLCov.tif") as src2:
    out_image2, out_transform2 = rasterio.mask.mask(src2, shapes, crop=True)
    out_meta2 = src2.meta
    print(src2.meta)
    out_meta2.update({"driver": "GTiff", "height": out_image2.shape[1], 
                     "width": out_image2.shape[2], 
                     "transform": out_transform2})
    out_file2 = LCov + "wvLCov.tif"
    with rasterio.open(out_file2, "w", **out_meta2) as dest:
        dest.write(out_image2)
print('WV Clipped Succesfully!!') 
"""


#Option to skip mosiac steps and clip using the national datasets 
#(other code must be commented out)
shapefile = fiona.open(wvBoundary)
shapes = [feature['geometry'] for feature in shapefile]
rasterio.Env(GDAL_TIFF_INTERNAL_MASK=True)  

with rasterio.open(usElev) as src1:
    out_image, out_transform = rasterio.mask.mask(src1, shapes, crop=True)
    out_meta = src1.meta
    print(src1.meta)
    out_meta.update({"driver": "GTiff", "height": out_image.shape[1], 
                     "width": out_image.shape[2], 
                     "transform": out_transform})
    out_file = Elev + "wvElev_us.tif"
    with rasterio.open(out_file, "w", **out_meta) as dest:
        dest.write(out_image)
print('WV Clipped Succesfully!!')  

with rasterio.open(usLC) as src2:
    out_image2, out_transform2 = rasterio.mask.mask(src2, shapes, crop=True)
    out_meta2 = src2.meta
    print(src2.meta)
    out_meta2.update({"driver": "GTiff", "height": out_image2.shape[1], 
                     "width": out_image2.shape[2], 
                     "transform": out_transform2})
    out_file2 = LCov + "wvLCov_us.tif"
    with rasterio.open(out_file2, "w", **out_meta2) as dest:
        dest.write(out_image2)
print('WV Clipped Succesfully!!') 