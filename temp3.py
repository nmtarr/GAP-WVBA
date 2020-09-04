# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 13:39:25 2020

@author: nmtarr

exploratory test of crosswalk support metric.
"""

import pandas as pd
import numpy as np

x = list(range(1,20,1))
y = x
df = pd.DataFrame({"x":x, "y":y})
df['z'] = df['x']/2.
df.set_index(['x']).plot()
