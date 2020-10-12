# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:13:37 2020

@author: Jessie Jordan

Description: Clip and summarizes GAP_types to L4 ecoregions in WV
NOTE: Code must be run in a Python 2.7 environment
"""

import repo_functions as fun
import sys
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.4/bin64')
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.4/ArcPy')
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.4/ArcToolBox/Scripts')

import arcpy
arcpy.env.overwriteOutput = True
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = 1

#Using Arc with Proj6 may or may not work due to permissions access, revisit if import fails
#projDir = "C:/Users/jhpage/"
valueRaster = fun.dataDir + "LandCover/WVworkspace/wvLC.tif"
inputFC = fun.dataDir + "LandCover/WVworkspace/wv_eco.shp"
##  new output database for tables, or gdb to be overwritten
outputLoc = fun.dataDir + "LandCover/WVworkspace/ecoclip/"
selectVal = "US_L3NAME"

##  set input value raster as snap raster
arcpy.env.snapRaster = valueRaster

##  make input feature class a feature layer, to access information
##  and allow for selection of features by attribute or location
arcpy.MakeFeatureLayer_management(inputFC,"polygonLayer")

##  create empty list variable to populate
##  with uniqe IDs, based on values in "OBJECTID" 
uniqueIDs = []
##  create search cursor to access attribute table of input feature class
sc = arcpy.SearchCursor("polygonLayer")
##  advance search cursor to first row in table
row = sc.next()

##  while there is still a row in the table to read
while row:
    ##  if the value in the "rteno" field is not in the
    ##  list of uniqueIDs...
    if row.getValue(selectVal) not in uniqueIDs:
        uniqueIDs.append(row.getValue(selectVal))
    row = sc.next()

##  for each unique id...
#####Code currently fails at Select by Attribute tool
for uid in uniqueIDs:
    print ('Creating Layer for ' + str(uid))
    ##  select the polygon feature with the current id
    arcpy.SelectLayerByAttribute_management("polygonLayer","NEW_SELECTION",
                                            'US_L3NAME = ' + str(uid))
    arcpy.Clip(valueRaster, "polygonLayer", (outputLoc + selectVal), "", 
                                               "", "ClippingGeometry", "")

##  move workspace to the output geodatabase of tables
arcpy.env.workspace = outputLoc

print "Merging tables..."
##  create empty list of tables names for merging
mergeList = []
##  iterate through the tables in the workspace...
for table in arcpy.ListTables():
    ##  if that table is not already in mergeList...
    if table not in mergeList:
        ##  add it to mergeList
        mergeList.append(table)

##  merge the tables into a new table
arcpy.Merge_management(mergeList,"CoverTablegfc2000")