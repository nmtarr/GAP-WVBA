# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:41:17 2020

@author: nmtarr

Test of region xwalk script.  
"""
import repo_functions as fun

help(fun.regional_xwalk)

a, b, c, d = fun.regional_xwalk(sp_name="Acadian Flycatcher", cutoff_lc=1.0, 
                                min_detections=1, min_link=0.49, 
                                support_bins=[0, 0.49, 0.80, 1],
                                print_tables=False)

print(a)
print(b)
print(c)
print(d)

