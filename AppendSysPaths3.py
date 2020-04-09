# -*- coding: utf-8 -*-
"""
Description: append statements that need to be run upfront in top-level
scripts in order to be able to import packages not instalable with conda
or pip.
execute with "execfile("AppendSysPaths27.py")"
N. Tarr, 7/20/2018
"""
import sys
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.4/bin64')
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.4/ArcPy')
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.4/ArcToolBox/Scripts')
#sys.path.append('T:/GAP/Data/')