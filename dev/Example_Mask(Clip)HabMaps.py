# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 15:08:11 2016

@author: nmtarr

Script to create a collection of hab maps clipped to smaller extents that can
be used for tests and troubleshooting and developing code.  This code extracts
the species habitat maps from within polygons for various sizes.  "Tiny" is 45 
cells, "Small" is 1 huc in SC, and "Medium" is an area of the northern Rockies.

If this code is rerun, be sure to run check_model and check_prop on each 
directory until there are no problem rasters.  This script may not handle all
problems on the first run through.
"""
import arcpy
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")
import sys
sys.path.append("T:/Gap/Data")
sys.path.append('T:/Scripts/GAPage')
import gapage as gp

fromLoc = "D:/Work/Output/"
arcpy.env.workspace = fromLoc
big_maps = arcpy.ListRasters()

#######################################################################  SMALL
print(("#")*70)
toLoc = "D:/Work/Output/Small/"
arcpy.env.workspace = toLoc
smallMask = "a_SC_HUC.shp"

for bm in big_maps:
    print "\n" + bm
    try:
        m = arcpy.Raster(fromLoc + bm)
        e = arcpy.sa.ExtractByMask(m, smallMask)
        try:
            rows = arcpy.SearchCursor(e)
            for row in rows:
                print row.getValue("VALUE"), row.getValue("Count")
            e.save(bm)
            print("Copied " + bm)
        except:
            print("Skipped " + bm)
            e = None  
    except Exception as e:
        print("Couldn't copy {0}".format(m))
        print ("\t {0}".format(e))

arcpy.management.BuildPyramidsandStatistics(toLoc, skip_existing=True)
newRas = arcpy.ListRasters()
check_model = gp.gaprasters.CheckModelTable(newRas)
check_prop = gp.gaprasters.CheckRasterProperties(newRas)

for new in check_model["CursorProblem"]:
    arcpy.management.Delete(new)
    print(new)
    
######################################################################## TINY
print(("#")*70)
toLoc = "D:/Work/Output/Tiny/"
arcpy.env.workspace = toLoc
smallMask = "tiny_extent.shp"

for bm in big_maps:
    print "\n" + bm
    try:
        m = arcpy.Raster(fromLoc + bm)
        e = arcpy.sa.ExtractByMask(m, smallMask)
        try:
            rows = arcpy.SearchCursor(e)
            for row in rows:
                print row.getValue("VALUE"), row.getValue("Count")
            e.save(bm)
            print("Copied " + bm)
        except:
            print("Skipped " + bm)
            e = None  
    except Exception as e:
        print("Couldn't copy {0}".format(m))
        print ("\t {0}".format(e))

arcpy.management.BuildPyramidsandStatistics(toLoc, skip_existing=True)
newRas = arcpy.ListRasters()
check_model = gp.gaprasters.CheckModelTable(newRas)
check_prop = gp.gaprasters.CheckRasterProperties(newRas)

for new in check_model["CursorProblem"]:
    arcpy.management.Delete(new)
    print(new)
    
####################################################################  MEDIUM
print(("#")*70)
toLoc = "D:/Work/Output/Medium/"
arcpy.env.workspace = toLoc
smallMask = "medium_extent.shp"

for bm in big_maps:
    print "\n" + bm
    try:
        m = arcpy.Raster(fromLoc + bm)
        e = arcpy.sa.ExtractByMask(m, smallMask)
        try:
            rows = arcpy.SearchCursor(e)
            for row in rows:
                print row.getValue("VALUE"), row.getValue("Count")
            e.save(bm)
            print("Copied " + bm)
        except:
            print("Skipped " + bm)
            e = None  
    except Exception as e:
        print("Couldn't copy {0}".format(m))
        print ("\t {0}".format(e))

arcpy.management.BuildPyramidsandStatistics(toLoc, skip_existing=True)
newRas = arcpy.ListRasters()
check_model = gp.gaprasters.CheckModelTable(newRas)
check_prop = gp.gaprasters.CheckRasterProperties(newRas)
for new in check_model["CursorProblem"]:
    print(new)
    null = arcpy.sa.SetNull(new, new, "VALUE = 255")
    print("Nulled")
    null.save(new)
    print("Saved")
    
newRas = arcpy.ListRasters()
check_model = gp.gaprasters.CheckModelTable(newRas)
check_prop = gp.gaprasters.CheckRasterProperties(newRas)
for new in check_model["CursorProblem"]:
    arcpy.management.Delete(new)
    print(new)
