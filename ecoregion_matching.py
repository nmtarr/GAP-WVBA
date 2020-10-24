# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:13:37 2020

@author: Jessie Jordan

Description: Clip and summarizes GAP_types to L3 ecoregions in WV
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


in_class_data = fun.dataDir + "LandCover/WVworkspace/wvlc"
in_zone_data = fun.dataDir + "LandCover/WVworkspace/wv_eco.shp"
##  new output database for tables, or gdb to be overwritten
out_table = fun.dataDir + "LandCover/WVworkspace/ecoclip/wvlc_L3.dbf"
out_table2 = fun.dataDir + "LandCover/WVworkspace/ecoclip/wvlc_ne.dbf"
out_table3 = fun.dataDir + "LandCover/WVworkspace/ecoclip/wvlc_se.dbf"
##  set input value raster as snap raster
arcpy.env.snapRaster = in_class_data

arcpy.sa.TabulateArea(in_class_data, "VALUE", 
             in_zone_data, "US_L3CODE", out_table, 30)
arcpy.TableToTable_conversion(out_table, 
                              fun.dataDir + "LandCover/WVworkspace/ecoclip/", 
                              "wvlc_L3.csv")

arcpy.sa.TabulateArea(in_class_data, "VALUE", 
             in_zone_data, "US_L4CODE", out_table2, 30)
arcpy.TableToTable_conversion(out_table2, 
                              fun.dataDir + "LandCover/WVworkspace/ecoclip/", 
                              "wvlc_L4.csv")


in_class_datane = fun.dataDir + "LandCover/WVworkspace/nelcclip"
in_class_datase = fun.dataDir + "LandCover/WVworkspace/selcclip"
in_zone_data2 = fun.dataDir + "LandCover/WVworkspace/wv_eco.shp"
##  new output database for tables, or gdb to be overwritten
arcpy.sa.TabulateArea(in_class_datane, "VALUE", 
             in_zone_data2, "STATE_NAME", out_table2, 30)
arcpy.TableToTable_conversion(out_table2, 
                              fun.dataDir + "LandCover/WVworkspace/ecoclip/", 
                              "wvlc_ne.csv")
arcpy.sa.TabulateArea(in_class_datase, "VALUE", 
             in_zone_data2, "STATE_NAME", out_table3, 30)
arcpy.TableToTable_conversion(out_table3, 
                              fun.dataDir + "LandCover/WVworkspace/ecoclip/", 
                              "wvlc_se.csv")