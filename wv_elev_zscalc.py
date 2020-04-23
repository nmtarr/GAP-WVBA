# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:40:31 2020

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
fromLoc = "P:/Proj3/USGap/Vert/Model/data/Temp/"
toLoc = projDir + 'WV_GAPcover/2001/WVworkspace/'
resLoc = projDir + "/Results/"
arcpy.env.workspace = fromLoc
arcpy.env.workspace = toLoc
arcpy.env.snapRaster = fromLoc + "snapgrid"
arcpy.env.cellSize = "MINOF"
wvElev = toLoc + 'wvElev'
arcpy.BuildRasterAttributeTable_management(wvElev)
wvLC = toLoc + 'wvLC'
arcpy.BuildRasterAttributeTable_management(wvLC)                   

try:
    print("Performing Zonal Statistics as Table for wvLC")
    OutRAS = toLoc + "wvLC_El.dbf"
    OutTable = toLoc + "wvLC_El.csv"
    arcpy.sa.ZonalStatisticsAsTable(wvLC, "Value", wvElev, "wvLC_EL.dbf")
    arcpy.TableToTable_conversion(OutRAS, resLoc, "wvLC_EL.csv")
    zsTable = pd.read_csv(OutTable)
    print(OutTable)
except Exception as e:
    print(e)

