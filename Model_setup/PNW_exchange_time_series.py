# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:29:16 2018
@author: jdkern
"""
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def exchange(year):

    year=0
    
    df_Path66 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path66.csv',header=0,index_col=0)
    df_Path3 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path3.csv',header=0,index_col=0)
    df_Path8 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path8.csv',header=0,index_col=0)
    df_Path14 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path14.csv',header=0,index_col=0)
    df_Path65 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path65.csv',header=0,index_col=0)    
       
    df_Path66 = df_Path66.loc[year*365:year*365+364,:]
    df_Path3 = df_Path3.loc[year*365:year*365+364,:]
    df_Path8 = df_Path8.loc[year*365:year*365+364,:]
    df_Path14 = df_Path14.loc[year*365:year*365+364,:]
    df_Path65 = df_Path65.loc[year*365:year*365+364,:]
       
    df_Path66 = df_Path66.reset_index(drop=True)
    df_Path3 = df_Path3.reset_index(drop=True)
    df_Path8 = df_Path8.reset_index(drop=True)
    df_Path14 = df_Path14.reset_index(drop=True)
    df_Path65 = df_Path65.reset_index(drop=True)
    
    # select dispatchable imports (positve flow days)
    
    forecast_days = ['fd1','fd2','fd3','fd4','fd5','fd6','fd7']
    
    for i in range(0,len(df_Path66)):     
        
        for fd in forecast_days:
            
            if df_Path3.loc[i,fd] >= 0:
                df_Path3.loc[i,fd] = 0
            else:
                df_Path3.loc[i,fd] = -df_Path3.loc[i,fd]
    
            if df_Path65.loc[i,fd] >= 0:
                df_Path65.loc[i,fd] = 0
            else:
                df_Path65.loc[i,fd] = -df_Path65.loc[i,fd]
                
            if df_Path66.loc[i,fd] >= 0:
                df_Path66.loc[i,fd] = 0
            else:
                df_Path66.loc[i,fd] = -df_Path66.loc[i,fd]
                
            if df_Path14.loc[i,fd] < 0:
                df_Path14.loc[i,fd] = 0
    
            if df_Path8.loc[i,fd] < 0:
                df_Path8.loc[i,fd] = 0
    
    # convert to minimum flow time series and dispatchable (daily)
    df_mins = pd.read_excel('Path_setup/PNW_imports_minflow_profiles.xlsx',header=0)
    
    for i in range(0,len(df_Path66)):
        
        for fd in forecast_days:
        
            m= 'Path66'
             
            if df_mins.loc[i,m] >= df_Path66.loc[i,fd]:
                df_mins.loc[i,m] = df_Path66.loc[i,fd]
                df_Path66.loc[i,fd] = 0
            
            else:
                df_Path66.loc[i,fd] = np.max((0,df_Path66.loc[i,fd]-df_mins.loc[i,m]))
                
            m= 'Path65'
             
            if df_mins.loc[i,m] >= df_Path65.loc[i,fd]:
                df_mins.loc[i,m] = df_Path65.loc[i,fd]
                df_Path65.loc[i,fd] = 0
            
            else:
                df_Path65.loc[i,fd] = np.max((0,df_Path65.loc[i,fd]-df_mins.loc[i,m]))
                
            m= 'Path3'
             
            if df_mins.loc[i,m] >= df_Path3.loc[i,fd]:
                df_mins.loc[i,m] = df_Path3.loc[i,fd]
                df_Path3.loc[i,fd] = 0
            
            else:
                df_Path3.loc[i,fd] = np.max((0,df_Path3.loc[i,fd]-df_mins.loc[i,m]))
                
            
            m= 'Path8'
             
            if df_mins.loc[i,m] >= df_Path8.loc[i,fd]:
                df_mins.loc[i,m] = df_Path8.loc[i,fd]
                df_Path8.loc[i,fd] = 0
            
            else:
                df_Path8.loc[i,fd] = np.max((0,df_Path8.loc[i,fd]-df_mins.loc[i,m]))
    
            m= 'Path14'
             
            if df_mins.loc[i,m] >= df_Path14.loc[i,fd]:
                df_mins.loc[i,m] = df_Path14.loc[i,fd]
                df_Path14.loc[i,fd] = 0
            
            else:
                df_Path14.loc[i,fd] = np.max((0,df_Path14.loc[i,fd]-df_mins.loc[i,m]))
    
    dispatchable_66 = df_Path66*24
    dispatchable_65 = df_Path65*24
    dispatchable_3 = df_Path3*24
    dispatchable_8 = df_Path8*24
    dispatchable_14 = df_Path14*24
    
    dispatchable_66.to_csv('Path_setup/PNW_dispatchable_66.csv')
    dispatchable_65.to_csv('Path_setup/PNW_dispatchable_65.csv')
    dispatchable_3.to_csv('Path_setup/PNW_dispatchable_3.csv')
    dispatchable_8.to_csv('Path_setup/PNW_dispatchable_8.csv')
    dispatchable_14.to_csv('Path_setup/PNW_dispatchable_14.csv')
           
    # hourly minimum flow for paths
    hourly66 = np.zeros((8760,len(forecast_days)))
    hourly65 = np.zeros((8760,len(forecast_days)))
    hourly3 = np.zeros((8760,len(forecast_days)))
    hourly8 = np.zeros((8760,len(forecast_days)))
    hourly14 = np.zeros((8760,len(forecast_days)))
    
    for i in range(0,365):
        
        for fd in forecast_days:
            
            fd_index = forecast_days.index(fd)
        
            m = 'Path66'
            hourly66[i*24:i*24+24,fd_index] = np.min((df_mins.loc[i,m], df_Path66.loc[i,fd]))
                   
            m = 'Path65'
            hourly65[i*24:i*24+24,fd_index] = np.min((df_mins.loc[i,m], df_Path65.loc[i,fd]))
                
            m = 'Path3'
            hourly3[i*24:i*24+24,fd_index] = np.min((df_mins.loc[i,m], df_Path3.loc[i,fd]))
        
            m = 'Path8'
            hourly8[i*24:i*24+24,fd_index] = np.min((df_mins.loc[i,m], df_Path8.loc[i,fd]))   
    
            m = 'Path14'
            hourly14[i*24:i*24+24,fd_index] = np.min((df_mins.loc[i,m], df_Path14.loc[i,fd]))   
    
    H66 = pd.DataFrame(hourly66)
    H66.columns = forecast_days
    H66.to_csv('Path_setup/PNW_path_mins66.csv')
    
    H65 = pd.DataFrame(hourly65)
    H65.columns = forecast_days
    H65.to_csv('Path_setup/PNW_path_mins65.csv')
    
    H3 = pd.DataFrame(hourly3)
    H3.columns = forecast_days
    H3.to_csv('Path_setup/PNW_path_mins3.csv')
    
    H8 = pd.DataFrame(hourly8)
    H8.columns = forecast_days
    H8.to_csv('Path_setup/PNW_path_mins8.csv')
    
    H14 = pd.DataFrame(hourly14)
    H14.columns = forecast_days
    H14.to_csv('Path_setup/PNW_path_mins14.csv')
    
    # hourly exports
    
    df_Path66 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path66.csv',header=0,index_col=0)
    df_Path3 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path3.csv',header=0,index_col=0)
    df_Path8 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path8.csv',header=0,index_col=0)
    df_Path14 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path14.csv',header=0,index_col=0)
    df_Path65 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path65.csv',header=0,index_col=0)    
       
    df_Path66 = df_Path66.loc[year*365:year*365+364,:]
    df_Path3 = df_Path3.loc[year*365:year*365+364,:]
    df_Path8 = df_Path8.loc[year*365:year*365+364,:]
    df_Path14 = df_Path14.loc[year*365:year*365+364,:]
    df_Path65 = df_Path65.loc[year*365:year*365+364,:]
       
    df_Path66 = df_Path66.reset_index(drop=True)
    df_Path3 = df_Path3.reset_index(drop=True)
    df_Path8 = df_Path8.reset_index(drop=True)
    df_Path14 = df_Path14.reset_index(drop=True)
    df_Path65 = df_Path65.reset_index(drop=True)
    
    e65 = np.zeros((8760,len(forecast_days)))
    e66 = np.zeros((8760,len(forecast_days)))
    e3 = np.zeros((8760,len(forecast_days)))
    e8 = np.zeros((8760,len(forecast_days)))
    e14 = np.zeros((8760,len(forecast_days)))
    
    #Path 65
    path_profiles65 = pd.read_excel('Path_setup/PNW_path_export_profiles.xlsx',sheet_name='Path65',header=None)
    pp65 = path_profiles65.values*-1
    
    #Path 14
    path_profiles14 = pd.read_excel('Path_setup/PNW_path_export_profiles.xlsx',sheet_name='Path14',header=None)
    pp14 = path_profiles14.values
    
    #Path 3
    path_profiles3 = pd.read_excel('Path_setup/PNW_path_export_profiles.xlsx',sheet_name='Path3',header=None)
    pp3 = path_profiles3.values*-1
    
    #Path 66
    path_profiles66 = pd.read_excel('Path_setup/PNW_path_export_profiles.xlsx',sheet_name='Path66',header=None)
    pp66 = path_profiles66.values*-1
    
    #Path 8
    path_profiles8 = pd.read_excel('Path_setup/PNW_path_export_profiles.xlsx',sheet_name='Path8',header=None)
    pp8 = path_profiles8.values    
    
    for i in range(0,len(df_Path65)):
    
        for fd in forecast_days:
            
            fd_index = forecast_days.index(fd)
            
            if df_Path66.loc[i,fd] < 0:
                e66[i*24:i*24+24,fd_index] = pp66[i,:]*df_Path66.loc[i,fd]*-1
    
            if df_Path65.loc[i,fd] < 0:
                e65[i*24:i*24+24,fd_index] = pp65[i,:]*df_Path65.loc[i,fd]*-1
    
            if df_Path3.loc[i,fd] < 0:
                e3[i*24:i*24+24,fd_index] = pp3[i,:]*df_Path3.loc[i,fd]*-1
    
            if df_Path8.loc[i,fd] < 0:
                e8[i*24:i*24+24,fd_index] = pp8[i,:]*df_Path8.loc[i,fd]*-1   
    
            if df_Path14.loc[i,fd] < 0:
                e14[i*24:i*24+24,fd_index] = pp14[i,:]*df_Path14.loc[i,fd]*-1  
       
    e66 = e66*24
    e65 = e65*24
    e3 = e3*24
    e14 = e14*24
    e8=e8*24
    
    for i in range(0,len(e14)):
        for fd in forecast_days:
            fd_index = forecast_days.index(fd)
            
            if e14[i,fd_index] > 3800:
                e14[i,fd_index] = 3800
                
    exports66 = pd.DataFrame(e66) 
    exports66.columns = forecast_days
    exports66.to_csv('Path_setup/PNW_exports66.csv')
    
    exports65 = pd.DataFrame(e65) 
    exports65.columns = forecast_days
    exports65.to_csv('Path_setup/PNW_exports65.csv')
    
    exports14 = pd.DataFrame(e14) 
    exports14.columns = forecast_days
    exports14.to_csv('Path_setup/PNW_exports14.csv')
    
    exports3 = pd.DataFrame(e3) 
    exports3.columns = forecast_days
    exports3.to_csv('Path_setup/PNW_exports3.csv')        
    
    exports8 = pd.DataFrame(e8) 
    exports8.columns = forecast_days
    exports8.to_csv('Path_setup/PNW_exports8.csv')      
    
    ##########################
    ##########################
    
    # HYDRO
    
    # convert to minimum flow time series and dispatchable (daily)
    
    df_data = pd.read_csv('../Stochastic_engine/PNW_hydro/PNW_hydro_daily.csv',header=0)
    hydro = df_data.loc[year*365:year*365+364,:]
    hydro = hydro.reset_index()
    df_mins = pd.read_excel('Hydro_setup/Minimum_hydro_profiles.xlsx',header=0)
       
    for i in range(0,len(hydro)):
        for fd in forecast_days:
          
            if df_mins.loc[i,'PNW']*24 >= hydro.loc[i,fd]:
                df_mins.loc[i,'PNW'] = hydro.loc[i,fd]/24
                hydro.loc[i,fd] = 0
            
            else:
                hydro.loc[i,fd] = np.max((0,hydro.loc[i,fd]-df_mins.loc[i,'PNW']*24))
        
    dispatchable_hydro = hydro
    dispatchable_hydro.to_csv('Hydro_setup/PNW_dispatchable_hydro.csv')
    
    # hourly minimum flow for hydro
    hourly = np.zeros((8760,len(forecast_days)))
    
    df_data = pd.read_csv('../Stochastic_engine/PNW_hydro/PNW_hydro_daily.csv',header=0)
    hydro = df_data.loc[year*365:year*365+364,:]
    hydro = hydro.reset_index()
        
    for i in range(0,365):
        for fd in forecast_days:
            fd_index = forecast_days.index(fd)
            
            hourly[i*24:i*24+24,fd_index] = np.min((df_mins.loc[i,'PNW'],hydro.loc[i,fd]))
            
    H = pd.DataFrame(hourly)
    H.columns = forecast_days
    H.to_csv('Hydro_setup/PNW_hydro_mins.csv')

    return None
