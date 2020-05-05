# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:03:19 2020

@author: Jessica
"""
import sys
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.4/bin64')
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.4/ArcPy')
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.4/ArcToolBox/Scripts')

import arcpy
arcpy.env.overwriteOutput = True
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
#import sys
#sys.path.append("T:/Gap/Data")
#sys.path.append('T:/Scripts/GAPage')
#import gapage as gp

projDir = "P:/Proj6/GAP-WVBA/"
gapDataDir = "P:/Proj3/USGap/Vert/Model/data/"
fromLoc = "P:/Proj3/USGap/Vert/Model/data/Temp/"
toLoc = projDir + 'WV_GAPcover/2001/WVworkspace/'
arcpy.env.workspace = fromLoc
arcpy.env.workspace = toLoc
arcpy.env.snapRaster = fromLoc + "snapgrid"

in_point_features = toLoc + "BBA_datapoints.shp"
wvElev = toLoc + 'wvElev'
wvLC = toLoc + 'wvLC'
in_rasters = [wvElev, wvLC]

arcpy.sa.ExtractMultiValuesToPoints(in_point_features, in_rasters)

