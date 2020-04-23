# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 11:07:57 2020

@author: Jessica

Environmental Req: Python 2.7, numpy, pandas, sciencebasepy, arcGIS 10.4

# Create a function for retrieving the elevation min or max from hab map

def elev_from_map(gap_id, parameter):

    Assess GAP habitat map against elevation raster to determine the max
    or min elevation of suitable habitat grid cells (summer).
    
    Parameters:
    gap_id -- GAP species code
    parameter -- either "max" or "min"
    
    Example:
    elev = elev_from_map('bAMROx', 'max')

    ######## Not sure yet the best way to do this. arcpy? 
    # Return elevation
     return elevation
"""
python
from datetime import datetime
import pandas as pd
import os, glob, sys

sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.4/bin64')
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.4/ArcPy')
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.4/ArcToolBox/Scripts')

import arcpy
arcpy.env.overwriteOutput = True
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

projDir = "P:/Proj6/GAP-WVBA/"
gapDataDir = "P:/Proj3/USGap/Vert/Model/data/"
habitatDir = projDir + "Data/habmaps/"
fromLoc = "P:/Proj3/USGap/Vert/Model/data/Temp/"
toLoc = projDir + 'WV_GAPcover/2001/WVworkspace/'
arcpy.env.workspace = fromLoc
arcpy.env.workspace = toLoc
arcpy.env.snapRaster = fromLoc + "snapgrid"
arcpy.env.cellSize = "MINOF"
wvLC = toLoc + 'wvlc'
arcpy.BuildRasterAttributeTable_management(wvLC)

dataDir = projDir + "Data/"
habitatDir = projDir + "Data/habmaps/"
listDir = dataDir + 'Specieslists/WV_AtlasCodes.csv'
resultsCSV = projDir + "Results/elevation_summary.csv"
toDir = "C:/Temp/"

timestamp = str(datetime.now().strftime("%d%B%Y_%I%M%p"))
archiveCSV = projDir + "/Results/Archive/elevation_" + timestamp + ".csv"
elTable = pd.read_csv(resultsCSV, index_col = 'GAP_code', dtype={'GAP_code': 'string', 
                                     'common_name': 'string'})                        
i= elTable.index[8:9]
for i in elTable.index[8:9]:
    try:
        gap_id = i[0] + i[1:5].upper() + i[5]
        print(gap_id)
        gapRaster = habitatDir + gap_id + "_wv.tif"
        arcpy.BuildRasterAttributeTable_management(gapRaster)
        print("Performing Zonal Statistics as Table for " + gap_id)
        gapRas = arcpy.sa.SetNull(gapRaster, wvLC, "Value <> 1")
        gapRas.save(habitatDir + gap_id + "_wvred.tif")
        gapFiles = glob.glob(habitatDir + gap_id +'_wv.tif.*')
        for g in gapFiles:
            os.remove(g)
    except Exception as e:
        print(e)



