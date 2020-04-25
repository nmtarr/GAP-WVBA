# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:40:12 2020

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
wvElev = toLoc + 'wvElev'
arcpy.BuildRasterAttributeTable_management(wvElev)

resultsCSV = projDir + "Results/elevation_summary.csv"
toDir = "C:/Temp/"

timestamp = str(datetime.now().strftime("%d%B%Y_%I%M%p"))
archiveCSV = projDir + "/Results/Archive/elevation_" + timestamp + ".csv"
elTable = pd.read_csv(resultsCSV, index_col = 'GAP_code', dtype={'GAP_code': 'string', 
                                     'common_name': 'string'})                        
i= elTable.index[0:]
for i in elTable.index[0:]:
    try:
        gap_id = i[0] + i[1:5].upper() + i[5]
        print(gap_id)
        gapRaster = habitatDir + gap_id + "_wv.tif"
        arcpy.BuildRasterAttributeTable_management(gapRaster)
        print("Performing Zonal Statistics as Table for " + gap_id)
        OutRAS = toDir + gap_id + "_zs.dbf"
        OutTable = toDir + gap_id + "_zs.csv"
        arcpy.sa.ZonalStatisticsAsTable(gapRaster, "Value", wvElev, OutRAS)
        arcpy.TableToTable_conversion(OutRAS, toDir, gap_id + "_zs.csv")
        zsTable = pd.read_csv(OutTable)
        print("Writing min and max values to table for " + gap_id)
        MAP_maxElev = zsTable.loc[1, 'MAX']
        elTable.loc[i,'GAP_max_map'] = MAP_maxElev
        MAP_minElev = zsTable.loc[1, 'MIN']
        elTable.loc[i,'GAP_min_map'] = MAP_minElev
        elTable.to_csv(archiveCSV)
        elTable.to_csv(resultsCSV)
        gapFiles = glob.glob(habitatDir + gap_id +'_wv.tif.*')
        for g in gapFiles:
            os.remove(g)
    except Exception as e:
        print(e)




