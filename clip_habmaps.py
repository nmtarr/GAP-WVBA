# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 16:26:40 2020

@author: nmtarr

Description: Clips CONUS GAP habitat maps (summer) to the WV boundary.
"""
import os, sys, fiona
import rasterio
import rasterio.mask

# Set paths to data
projDir = "P:/Proj6/GAP-WVBA/"
CONUSDir = "P:/Proj3/USGap/Vert/Model/Output/CONUS/"
dataDir = projDir + "Data/"
clipDir = dataDir + "habmaps/"
listDir = dataDir + '/Specieslists/WV_AtlasCodes.csv'
wvBoundary = projDir + 'WV_GAPcover/2001/WVworkspace/wv_bound.shp'
outputGDB = projDir + 'WV_GAPcover/2001/WVworkspace/Temp'  ##Temp file for spp maps to be downloaded to


# Get a list of GAP species codes to process

# Loop through the list use species codes to pull map temporarily from database and clip each species' summer habitat map to WV.
# Generates empty list to allow for iteration through codes
uniqueIDs = []
sc = SearchCursor("listDir")
row = sc.next()
while row:
    if row.getValue("strUC") not in uniqueIDs:
        uniqueIDs.append(row.getValue("strUC"))
    row = sc.next()
uid = uniqueIDs[0]

for uid in uniqueIDs:
    print "Retreiving habitat map for " + str(uid)
    try:
        #add repo code here, ask Nathan 
        
        #save clipped map to clipDir with spp code
        with fiona.open("wvBoundary", "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile] #value raster is a placeholder for the current downloaded hab data
    except:																									##Print when route region group is not successfully performed
        print "Something went wrong with " + str(uid) + "."  


