# -*- coding: utf-8 -*-
"""
Created on Fri May  8 12:24:01 2020

@author: Jessica
"""


import os
import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 10)

projDir = "P:/Proj6/GAP-WVBA/"
resultsCSV = projDir + "Results/bbaHab_summary.csv"
recordsBBA = projDir + "Data/bba_spprecords.csv"
from datetime import datetime

timestamp = str(datetime.now(tz=None).strftime("%d%B%Y_%I%M%p"))
archiveCSV = projDir + "/Results/Archive/elevation_" + timestamp + ".csv"
df = pd.read_csv(recordsBBA,  dtype={'species': 'string', 
                                     'habitat': 'string',	
                                     'new hab': 'string',}) 

df.drop(['observer', 'start time',	'end time',	'month', 'day',	'year',	
              'block-point number', 'latitude', 'longitude'], 
             axis='columns', index=None, 
             columns=None, level=None, inplace=True, errors='raise')

fillCols = {'0-<50m:0-3 min' : '0', '0-<50m:>3-5 min': '0', 
            '0-<50m:>5-10min': '0', 
             '50-100m:0-3min': '0', '50-100m:>3-5min': '0', 
             '50-100m:>5-10min': '0', 
             '?100m or flyover:0-3min': '0', '?100m or flyover:>3-5min': '0', 
             '?100m or flyover:>5-10min': '0'}
pointList = df[{'0-<50m:0-3 min','0-<50m:>3-5 min', '0-<50m:>5-10min',
         '50-100m:0-3min','50-100m:>3-5min','50-100m:>5-10min',	
         '?100m or flyover:0-3min', '?100m or flyover:>3-5min',	
         '?100m or flyover:>5-10min'}]
pointList.fillna(fillCols, inplace=True)
pointList = pointList.astype(int)
df['point_sum'] = pointList.sum(axis=1)
df.drop(['0-<50m:0-3 min','0-<50m:>3-5 min', '0-<50m:>5-10min',
         '50-100m:0-3min','50-100m:>3-5min','50-100m:>5-10min',	
         '?100m or flyover:0-3min', '?100m or flyover:>3-5min',	
         '?100m or flyover:>5-10min'], axis='columns', index=None, 
             columns=None, level=None, inplace=True, errors='raise')
groupdf = df.groupby(['species', 'habitat']).agg({'point_sum': ['sum']})
unstackdf = groupdf.unstack(level=-1)
unstackdf.to_csv(archiveCSV)
unstackdf.to_csv(resultsCSV)

