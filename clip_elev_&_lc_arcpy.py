# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 11:42:47 2020

@author: Jessica Page Jordan
"""
#execfile("C:/Users/Jessica/GAP-WVBA/AppendSysPaths3.py").read()
#use the following to import arcpy when using command propt
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

# Paths

#seElev = gapDataDir + "Elev/elev_se"
#neElev = gapDataDir + "Elev/elev_ne"
#seLC = gapDataDir + "LandCover/lcgap_se"
#neLC = gapDataDir + "LandCover/lcgap_ne"
neMask = fromLoc + "maskclp_ne"
seMask = fromLoc + "maskclp_se"
seElev = fromLoc + "elev_se"
neElev = fromLoc + "elev_ne"
seLC = fromLoc + "lcgap_se"
neLC = fromLoc + "lcgap_ne"

#Mask regional data to exclude buffer
#Mask neElev   
outExtractByMask = arcpy.sa.ExtractByMask(neElev, neMask)
neEl_clip = toLoc + 'neElclip'
outExtractByMask.save(neEl_clip)
print("neElev clipped succesfully")
#Mask seElev    
outExtractByMask = arcpy.sa.ExtractByMask(seElev, seMask)
seEl_clip = toLoc + 'seElclip'
outExtractByMask.save(seEl_clip)
print("seElev clipped succesfully")
#Mask neLC    
outExtractByMask = arcpy.sa.ExtractByMask(neLC, neMask)
neLC_clip = toLoc + 'neLCclip'
outExtractByMask.save(neLC_clip)
print("neLC clipped succesfully")
#Mask seLC   
outExtractByMask = arcpy.sa.ExtractByMask(seLC, seMask)
seLC_clip = toLoc + 'seLCclip'
outExtractByMask.save(seLC_clip)
print("neLC clipped succesfully")

#Mosaic together NE and SE regions
ElRast = arcpy.ListRasters("*" + "Elclip")
eElev= toLoc + "elev"
arcpy.MosaicToNewRaster_management(ElRast, toLoc, "elev", "", "", "", 1,) 
print("Elevation mosaic successful") 

LCRast = arcpy.ListRasters("*" + "LCclip")
eLC= fromLoc + "lcgap"
arcpy.MosaicToNewRaster_management(LCRast, toLoc, "lcgap", "", "", "", 1,)  
print("Land Cover mosaic successful")

#Clip mosaiced rasters to W.Virginia
wvBoundary = toLoc + 'wv_bound.shp'
outExtractByMask = arcpy.sa.ExtractByMask(eElev, wvBoundary)
wvElev = toLoc + 'wvElev'
outExtractByMask.save(wvElev)
print("neLC clipped succesfully")

outExtractByMask = arcpy.sa.ExtractByMask(eLC, wvBoundary)
wvLC = toLoc + 'wvLC'
outExtractByMask.save(wvLC)
print("neLC clipped succesfully")


"""
arcpy.management.BuildPyramidsandStatistics(toLoc, skip_existing=True)
newRas = arcpy.ListRasters()
check_model = gp.gaprasters.CheckModelTable(newRas)
check_prop = gp.gaprasters.CheckRasterProperties(newRas)

for new in check_model["CursorProblem"]:
    arcpy.management.Delete(new)
    print(new)
"""

