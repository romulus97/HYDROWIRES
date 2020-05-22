# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 14:57:08 2020

@author: jkern
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#perfect foresight
df_pf_1 = pd.read_csv('PERFECT_FORESIGHT_RESULTS/mwh_1.csv')
df_pf_2 = pd.read_csv('PERFECT_FORESIGHT_RESULTS/mwh_2.csv')
df_pf_3 = pd.read_csv('PERFECT_FORESIGHT_RESULTS/mwh_3.csv')

#perfect foresight
df_p_1 = pd.read_csv('PERSISTANCE_RESULTS/mwh_1.csv')
df_p_2 = pd.read_csv('PERSISTANCE_RESULTS/mwh_2.csv')
df_p_3 = pd.read_csv('PERSISTANCE_RESULTS/mwh_3.csv')

pf = df_pf_1.loc[df_pf_1['Generator'] == 'PGEV_hydro','Value'] + df_pf_2.loc[df_pf_2['Generator'] == 'PGEV_hydro','Value'] + df_pf_3.loc[df_pf_3['Generator'] == 'PGEV_hydro','Value']
pf = pf.reset_index(drop=True)

p = df_p_1.loc[df_p_1['Generator'] == 'PGEV_hydro','Value'] + df_p_2.loc[df_p_2['Generator'] == 'PGEV_hydro','Value'] + df_p_3.loc[df_p_3['Generator'] == 'PGEV_hydro','Value']
p = p.reset_index(drop=True)

hourly_diff = []
pfv = pf.values
pv = p.values

for i in range(0,len(p)):
    diff = pfv[i] - pv[i]
    if i < 1:
        hourly_diff.append(diff)
    else:
        hourly_diff.append(diff + hourly_diff[i-1])
        

plt.figure()
plt.plot(hourly_diff)