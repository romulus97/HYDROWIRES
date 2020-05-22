# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 14:14:33 2020

@author: jkern
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df_data = pd.read_csv('CA_hydropower/SCE_hydro.csv',header=0,index_col=0)
data = df_data.values

pf = []
per = []
track = []
#    sample = total
sample = data
for j in range(0,len(data)-7):
    a = np.sum(sample[j:j+7,0])
    b = np.sum(sample[j,:])
    pf = np.append(pf,a)
    per = np.append(per,b)

difference = pf - per
for j in range(0,len(pf)):
    if j < 1:
        track.append(difference[j])
    else:
        track.append(difference[j] + track[j-1])
   
plt.figure()
plt.plot(difference)
plt.title('SCE')

plt.figure()
plt.plot(track)
plt.title('SCE')

plt.figure()
plt.plot(pf,'r')
plt.plot(per,'b')
plt.title('SCE')

pct = 100*track[-1]/sum(pf)
result = 'The error is ' + str(pct) + '%'
print(result)