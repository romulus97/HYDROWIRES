# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 10:25:49 2020

@author: jkern
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

per_means = []
pf_means = []
per_std = []
pf_std = []

# PRICES

for i in range(0,11):
    
    PER_filename = 'PERSISTENCE/PERSISTENCE_RESULTS/CA%d_shadow_price.csv' % i
    df_PER = pd.read_csv(PER_filename)
    per_means.append(np.mean(df_PER.loc[:,'Value']))
    per_std.append(np.std(df_PER.loc[:,'Value']))
    
    PF_filename = 'PERFECT_FORESIGHT/PERFECT_FORESIGHT_RESULTS/CA%d_shadow_price.csv' % i
    df_PF = pd.read_csv(PF_filename)
    pf_means.append(np.mean(df_PF.loc[:,'Value']))
    pf_std.append(np.std(df_PF.loc[:,'Value']))    
    
plt.figure()
plt.plot(per_means,'b')
plt.plot(pf_means,'r')
plt.title('PRICES Mean Values $/MWh')

plt.figure()
plt.plot(per_std,'b')
plt.plot(pf_std,'r')
plt.title('PRICES Std. Deviation $/MWh')

# OBJECTIVE FUNCTION 

per_means = []
pf_means = []

for i in range(0,11):
    
    PER_filename = 'PERSISTENCE/PERSISTENCE_RESULTS/CA%d_obj_function.csv' % i
    df_PER = pd.read_csv(PER_filename)
    per_means.append(np.mean(df_PER.loc[:,'0']))
    per_std.append(np.std(df_PER.loc[:,'0']))
    
    PF_filename = 'PERFECT_FORESIGHT/PERFECT_FORESIGHT_RESULTS/CA%d_obj_function.csv' % i
    df_PF = pd.read_csv(PF_filename)
    pf_means.append(np.mean(df_PF.loc[:,'0']))
    pf_std.append(np.std(df_PF.loc[:,'0']))    
    
plt.figure()
plt.plot(per_means,'b')
plt.plot(pf_means,'r')
plt.title('SYSTEM COST Mean Values $')


# EMISSIONS

#per_means = []
#pf_means = []
#
#for i in years:
#    
#    PER_filename = 'PERSISTANCE_RESULTS/CA%d_obj_function.csv' % i
#    df_PER = pd.read_csv(PER_filename)
#    per_means.append(np.mean(df_PER.loc[:,'0']))
#    per_std.append(np.std(df_PER.loc[:,'0']))
#    
#    PF_filename = 'PERFECT_FORESIGHT_RESULTS/CA%d_obj_function.csv' % i
#    df_PF = pd.read_csv(PF_filename)
#    pf_means.append(np.mean(df_PF.loc[:,'0']))
#    pf_std.append(np.std(df_PF.loc[:,'0']))    
#    
#plt.figure()
#plt.plot(per_means,'b')
#plt.plot(pf_means,'r')

    