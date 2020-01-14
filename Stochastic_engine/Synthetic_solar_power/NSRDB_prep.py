# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 23:32:13 2020

@author: jkern
"""

from __future__ import division
import pandas as pd 
import numpy as np

#years = ['1998','1999']
#hourly_clearsky1 = []
#hourly_GHI1 = []
#
##SITE 1
#for y in years:
#    filename = '154650_40.49_-121.9_' + y + '.csv'
#    df = pd.read_csv(filename,header=2)
#    for i in range(0,len(df),2):
#        hourly_clearsky1.append(np.mean(df.loc[i:i+1,'GHI']))
#        hourly_GHI1.append(np.mean(df.loc[i:i+1,'Clearsky GHI']))
#
##SITE 7
#hourly_clearsky7 = []
#hourly_GHI7 = []
#    
#for y in years:
#    filename = '71308_32.65_-114.18_' + y + '.csv'
#    df = pd.read_csv(filename,header=2)
#    for i in range(0,len(df),2):
#        hourly_clearsky7.append(np.mean(df.loc[i:i+1,'GHI']))
#        hourly_GHI7.append(np.mean(df.loc[i:i+1,'Clearsky GHI']))
#
#
##SITE 6
#hourly_clearsky6 = []
#hourly_GHI6 = []
#    
#for y in years:
#    filename = '80533_33.73_-115.82_' + y + '.csv'
#    df = pd.read_csv(filename,header=2)
#    for i in range(0,len(df),2):
#        hourly_clearsky6.append(np.mean(df.loc[i:i+1,'GHI']))
#        hourly_GHI6.append(np.mean(df.loc[i:i+1,'Clearsky GHI']))
#
##SITE 5
#hourly_clearsky5 = []
#hourly_GHI5 = []
#    
#for y in years:
#    filename = '83553_34.05_-118.38_' + y + '.csv'
#    df = pd.read_csv(filename,header=2)
#    for i in range(0,len(df),2):
#        hourly_clearsky5.append(np.mean(df.loc[i:i+1,'GHI']))
#        hourly_GHI5.append(np.mean(df.loc[i:i+1,'Clearsky GHI']))
#
#
##SITE 4
#hourly_clearsky4 = []
#hourly_GHI4 = []
#    
#for y in years:
#    filename = '93470_35.05_-117.34_' + y + '.csv'
#    df = pd.read_csv(filename,header=2)
#    for i in range(0,len(df),2):
#        hourly_clearsky4.append(np.mean(df.loc[i:i+1,'GHI']))
#        hourly_GHI4.append(np.mean(df.loc[i:i+1,'Clearsky GHI']))
#
#
##SITE 3
#hourly_clearsky3 = []
#hourly_GHI3 = []
#    
#for y in years:
#    filename = '110594_36.69_-119.54_' + y + '.csv'
#    df = pd.read_csv(filename,header=2)
#    for i in range(0,len(df),2):
#        hourly_clearsky3.append(np.mean(df.loc[i:i+1,'GHI']))
#        hourly_GHI3.append(np.mean(df.loc[i:i+1,'Clearsky GHI']))
#
#
#
##SITE 2
#hourly_clearsky2 = []
#hourly_GHI2 = []
#    
#for y in years:
#    filename = '131631_38.57_-121.7_' + y + '.csv'
#    df = pd.read_csv(filename,header=2)
#    for i in range(0,len(df),2):
#        hourly_clearsky2.append(np.mean(df.loc[i:i+1,'GHI']))
#        hourly_GHI2.append(np.mean(df.loc[i:i+1,'Clearsky GHI']))
#
#hourly = np.column_stack((hourly_GHI1,hourly_clearsky1,hourly_GHI2,hourly_clearsky2,hourly_GHI3,hourly_GHI3,hourly_clearsky3,hourly_GHI4,hourly_clearsky4,hourly_GHI5,hourly_clearsky5,hourly_GHI6,hourly_clearsky6,hourly_GHI7,hourly_clearsky7))
#
#df_hourly = pd.DataFrame(hourly)
#df_hourly.columns = ['s1','s1_clear','s2','s2_clear','s3','s3_clear','s4','s4_clear','s5','s5_clear','s6','s6_clear','s7','s7_clear']
#df_hourly.to_csv('more_hist.csv')


df_data = pd.read_csv('more_hist.csv')
days = int(len(df_data)/24)
daily = np.zeros((days,7))

for i in range(0,days):
    for j in range(0,7):
        field = 's' + str(j+1)
        daily[i,j] = np.sum(df_data.loc[i*24:i*24+24,field])
        
df_daily = pd.DataFrame(daily)
df_daily.columns = ['Site1','Site2','Site3','Site4','Site5','Site6','Site7']
df_daily.to_csv('syn_irr.csv')