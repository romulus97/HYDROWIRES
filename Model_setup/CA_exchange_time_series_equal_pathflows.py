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
    
    df_data = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/Load_Path_Sim.csv',header=0)
    c = ['Path66_sim','Path46_sim','Path61_sim','Path42_sim','Path24_sim','Path45_sim']
    df_data = df_data[c]
    paths = ['Path66','Path46','Path61','Path42','Path24','Path45']
    df_data.columns = paths
    df_data = df_data.loc[year*365:year*365+364,:]
    
    # select dispatchable imports (positve flow days)
    imports = df_data
    imports = imports.reset_index()
    
    for p in paths:
        for i in range(0,len(imports)):     
            
            if p == 'Path42':
                if imports.loc[i,p] >= 0:
                    imports.loc[i,p] = 0
                else:
                    imports.loc[i,p] = -imports.loc[i,p]
            
            elif p == 'Path46':
                if imports.loc[i,p] < 0:
                    imports.loc[i,p] = 0
                else:
                    imports.loc[i,p] = imports.loc[i,p]*.404 + 424
            
            else:
                if imports.loc[i,p] < 0:
                    imports.loc[i,p] = 0
                    
                    
    imports.rename(columns={'Path46':'Path46_SCE'}, inplace=True)
    imports.to_csv('Path_setup/CA_imports.csv')
    
    # convert to minimum flow time series and dispatchable (daily)
    df_mins = pd.read_excel('Path_setup/CA_imports_minflow_profiles.xlsx',header=0)
    lines = ['Path66','Path46_SCE','Path61','Path42']
    
    for i in range(0,len(df_data)):
        for L in lines:
            
            if df_mins.loc[i,L] >= imports.loc[i,L]:
                df_mins.loc[i,L] = imports.loc[i,L]
                imports.loc[i,L] = 0
            
            else:
                imports.loc[i,L] = np.max((0,imports.loc[i,L]-df_mins.loc[i,L]))
    
    dispatchable_imports = imports*24
    dispatchable_imports.to_csv('Path_setup/CA_dispatchable_imports.csv')
    
    df_data = pd.read_csv('Path_setup/CA_imports.csv',header=0)
    
    # hourly minimum flow for paths
    hourly = np.zeros((8760,len(lines)))
    
    for i in range(0,365):
        for L in lines:
            index = lines.index(L)
            
            hourly[i*24:i*24+24,index] = np.min((df_mins.loc[i,L], df_data.loc[i,L]))
            
    H = pd.DataFrame(hourly)
    H.columns = ['Path66','Path46_SCE','Path61','Path42']
    H.to_csv('Path_setup/CA_path_mins.csv')
    
    # hourly exports
    df_data = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/Load_Path_Sim.csv',header=0)
    c = ['Path66_sim','Path46_sim','Path61_sim','Path42_sim','Path24_sim','Path45_sim']
    df_data = df_data[c]
    df_data.columns = [paths]
    
    df_data = df_data.loc[year*365:year*365+364,:]
    df_data = df_data.reset_index()
    
    e = np.zeros((8760,4))
    
    #Path 42
    path_profiles = pd.read_excel('Path_setup/CA_path_export_profiles.xlsx',sheet_name='Path42',header=None)
    pp = path_profiles.values
    
    for i in range(0,len(df_data)):
        if df_data.loc[i,'Path42'].values > 0:
            e[i*24:i*24+24,0] = pp[i,:]*df_data.loc[i,'Path42'].values
    
    #Path 24
    path_profiles = pd.read_excel('Path_setup/CA_path_export_profiles.xlsx',sheet_name='Path24',header=None)
    pp = path_profiles.values
    
    for i in range(0,len(df_data)):
        if df_data.loc[i,'Path24'].values < 0:
            e[i*24:i*24+24,1] = pp[i,:]*df_data.loc[i,'Path24'].values*-1
    
    #Path 45
    path_profiles = pd.read_excel('Path_setup/CA_path_export_profiles.xlsx',sheet_name='Path45',header=None)
    pp = path_profiles.values
    
    for i in range(0,len(df_data)):
        if df_data.loc[i,'Path45'].values < 0:
            e[i*24:i*24+24,2] = pp[i,:]*df_data.loc[i,'Path45'].values*-1  
            
    #Path 66
    path_profiles = pd.read_excel('Path_setup/CA_path_export_profiles.xlsx',sheet_name='Path66',header=None)
    pp = path_profiles.values
    
    for i in range(0,len(df_data)):
        if df_data.loc[i,'Path66'].values < 0:
            e[i*24:i*24+24,2] = pp[i,:]*df_data.loc[i,'Path66'].values*-1  
    
    e = e*24
    
    exports = pd.DataFrame(e) 
    exports.columns = ['Path42','Path24','Path45','Path66']
    exports.to_csv('Path_setup/CA_exports.csv')
   
    
    # HYDRO    
    
    forecast_days = ['fd1','fd2','fd3','fd4','fd5','fd6','fd7']
    
    # convert to minimum flow time series and dispatchable (daily)
    
    df_PGE= pd.read_csv('../Stochastic_engine/CA_hydropower/PGE_valley_hydro.csv',header=0,index_col=0)
    df_SCE= pd.read_csv('../Stochastic_engine/CA_hydropower/SCE_hydro.csv',header=0,index_col=0)
    PGE_hydro = df_PGE.loc[year*365:year*365+364,:]
    SCE_hydro = df_SCE.loc[year*365:year*365+364,:]
    PGE_hydro = PGE_hydro.reset_index(drop=True)
    SCE_hydro = SCE_hydro.reset_index(drop=True)
    PGE_hydro=PGE_hydro.values*(1/.837)
    SCE_hydro=SCE_hydro.values*(1/.8016)
    
    df_mins = pd.read_excel('Hydro_setup/Minimum_hydro_profiles.xlsx',header=0)
    
    for i in range(0,len(PGE_hydro)):
        for fd in forecast_days:
            fd_index = forecast_days.index(fd)
            
            if df_mins.loc[i,'PGE_valley']*24 >= PGE_hydro[i,fd_index]:
                df_mins.loc[i,'PGE_valley'] = PGE_hydro[i,fd_index]/24
                PGE_hydro[i,fd_index] = 0            
            else:
                PGE_hydro[i,fd_index] = np.max((0,PGE_hydro[i,fd_index]-df_mins.loc[i,'PGE_valley']*24))
    
            if df_mins.loc[i,'SCE']*24 >= SCE_hydro[i,fd_index]:
                df_mins.loc[i,'SCE'] = SCE_hydro[i,fd_index]/24
                SCE_hydro[i,fd_index] = 0            
            else:
                SCE_hydro[i,fd_index] = np.max((0,SCE_hydro[i,fd_index]-df_mins.loc[i,'SCE']*24))
    
    dispatchable_PGE = pd.DataFrame(PGE_hydro)
    dispatchable_PGE.columns = forecast_days
    dispatchable_PGE.to_csv('Hydro_setup/CA_dispatchable_PGE.csv')
    
    dispatchable_SCE = pd.DataFrame(SCE_hydro)
    dispatchable_SCE.columns = forecast_days
    dispatchable_SCE.to_csv('Hydro_setup/CA_dispatchable_SCE.csv')
      
    # hourly minimum flow for hydro
    hourly_PGE = np.zeros((8760,len(forecast_days)))
    hourly_SCE = np.zeros((8760,len(forecast_days)))
    
    
    df_PGE= pd.read_csv('../Stochastic_engine/CA_hydropower/PGE_valley_hydro.csv',header=0,index_col=0)
    df_SCE= pd.read_csv('../Stochastic_engine/CA_hydropower/SCE_hydro.csv',header=0,index_col=0)
    PGE_hydro = df_PGE.loc[year*365:year*365+364,:]
    SCE_hydro = df_SCE.loc[year*365:year*365+364,:]
    PGE_hydro = PGE_hydro.reset_index(drop=True)
    SCE_hydro = SCE_hydro.reset_index(drop=True)
    PGE_hydro=PGE_hydro.values*(1/.837)
    SCE_hydro=SCE_hydro.values*(1/.8016) 
    
    for i in range(0,365):
        for fd in forecast_days:
            
            fd_index = forecast_days.index(fd)
                        
            hourly_PGE[i*24:i*24+24,fd_index] = np.min((df_mins.loc[i,'PGE_valley'],PGE_hydro[i,fd_index]))
            hourly_SCE[i*24:i*24+24,fd_index] = np.min((df_mins.loc[i,'SCE'],SCE_hydro[i,fd_index]))
            
    H_PGE = pd.DataFrame(hourly_PGE)
    H_PGE.columns = forecast_days
    H_PGE.to_csv('Hydro_setup/PGE_mins.csv')
    
    H_SCE = pd.DataFrame(hourly_SCE)
    H_SCE.columns = forecast_days
    H_SCE.to_csv('Hydro_setup/SCE_mins.csv')
    
    return None
