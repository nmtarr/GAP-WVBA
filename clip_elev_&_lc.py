# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 17:09:58 2020

@author: nmtarr

Description: Similar to clip_habmaps but clip the elevation and land cover
rasters to WV.  Save in "/Data"
"""
# Paths
gapDataDir = "P:/Proj3/USGap/Vert/Model/Data/"
seElev = gapDataDir + "Elev/Elev_se"
neElev = gapDataDir + "Elev/Elev_ne"
seLC = gapDataDir + "LandCover/lcgap_se"
neLC = gapDataDir + "LandCover/lcgap_ne"
wvBoundary = "P:/Proj6/GAP-WVBA/Data/wv_boundary.shp" # This needs to be created.

