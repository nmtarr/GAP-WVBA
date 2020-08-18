# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 17:35:46 2020

@author: nmtarr
"""
spp = 'xACFLx'

WV_types = (WV
            [lambda x: x['species'] == spp[1:5]]
            .T
            .rename(columns={1: 'detections'})
            .iloc[1:]
            [lambda x: x['detections'] > 0])
'''
Integrate this into the other script with the end in mind being
having the number of detections in the final table.
'''