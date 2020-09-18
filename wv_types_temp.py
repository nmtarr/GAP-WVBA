import repo_functions as fun
import pandas as pd
import numpy as np
species = "Cerulean Warbler"

#def WVBBA_detected_in(species):
'''
Returns list of cover types WVBBA found species in.
'''
WV = pd.read_csv(fun.resultsDir + "WV_spp_lc_detections.csv", header=0)
WV.rename({'3A' : '3', '4A' : '4', '8A' : '8', '7C' : '7', '13A' : '13', 
           '16D' : '16', '18D' : '18','1"': '1', '1LA' : '1',
           '1"U': '1', '10A' : '10'}, axis=1, inplace=True)
WV = WV.groupby(WV.columns, axis=1).sum()
WV.replace(0,np.nan, inplace=True)


spp = fun.GAP_spp_code(species)
WV_types = (WV
            [lambda x: x['species'] == spp[1:5]]
            .T)

WV_types = (WV_types.rename(columns={WV_types.columns[0]: 'detections'})
           .iloc[:-1]
            [lambda x: x['detections'] > 0])
#return WV_types

