# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 12:28:41 2020

@author: Jessica

WV Cross walk types were removed from consideration if they 
meet all of the following criteria:
    1. They match WV systems that were not reported
    2. The WV ststem was not used in West Virginia's final analysis
    3. SE GAP systems that would have crosswalked to those systems could be 
        crosswalked to other WV reported ecological systems
        
This applied to the following records:
3207	North-Central Appalachian Circumneutral Cliff and Talus	  26	Cliff
3207	North-Central Appalachian Circumneutral Cliff and Talus	  27	Talus
3208	North-Central Appalachian Acidic Cliff and Talus	      26	Cliff
3208	North-Central Appalachian Acidic Cliff and Talus	      27	Talus
3208	North-Central Appalachian Acidic Cliff and Talus	      28	Boulder field forest
4119	Southern Appalachian Northern Hardwood Forest	          28	Boulder field forest

The following matches meet all criteria except 3 and are recommended to revisit
3205	Central Interior Calcareous Cliff and Talus	26	Cliff
3205	Central Interior Calcareous Cliff and Talus	27	Talus
3219	Southern Interior Acid Cliff	            26	Cliff
3220	Southern Appalachian Montane Cliff	        26	Cliff
       
The following matches meet all criteria except criteria 1:
3207	North-Central Appalachian Circumneutral Cliff and Talus	25	Rock outcrop
3208	North-Central Appalachian Acidic Cliff and Talus	    25	Rock outcrop

"""
import pandas as pd
import repo_functions as fun
pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 15)

cross = pd.read_csv(fun.dataDir + "LandCover/land_cover_crosswalk.csv",
                    header=0, dtype={'GAP_code': str})
# Get indexes where name column has value john and 
# value column equals to 0.0
d1 = cross[ (cross['GAP_code'] == '3207') & (cross['wv_code_fine'] == '26')].index
cross.drop(d1, inplace=True) 
d2 = cross[ (cross['GAP_code'] == '3207') & (cross['wv_code_fine'] == '27')].index
cross.drop(d2, inplace=True)
d3 = cross[ (cross['GAP_code'] == '3208') & (cross['wv_code_fine'] == '26')].index
cross.drop(d3, inplace=True)
d4 = cross[ (cross['GAP_code'] == '3208') & (cross['wv_code_fine'] == '27')].index
cross.drop(d4, inplace=True)
d5 = cross[ (cross['GAP_code'] == '3208') & (cross['wv_code_fine'] == '28')].index
cross.drop(d5, inplace=True)
d6 = cross[ (cross['GAP_code'] == '4119') & (cross['wv_code_fine'] == '28')].index
cross.drop(d6, inplace=True)
cross.to_csv(fun.dataDir + "LandCover/land_cover_crosswalk2.csv")