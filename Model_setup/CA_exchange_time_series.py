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
    
    df_Path66 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path66.csv',header=0,index_col=0)
    df_Path46 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path46.csv',header=0,index_col=0)
    df_Path61 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path61.csv',header=0,index_col=0)
    df_Path42 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path42.csv',header=0,index_col=0)
    df_Path24 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path24.csv',header=0,index_col=0)
    df_Path45 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path45.csv',header=0,index_col=0)    
    
    df_Path66 = df_Path66.loc[year*365:year*365+364,:]
    df_Path46 = df_Path46.loc[year*365:year*365+364,:]
    df_Path61 = df_Path61.loc[year*365:year*365+364,:]
    df_Path42 = df_Path42.loc[year*365:year*365+364,:]
    df_Path24 = df_Path24.loc[year*365:year*365+364,:]
    df_Path45 = df_Path45.loc[year*365:year*365+364,:]    
    
    df_Path66 = df_Path66.reset_index(drop=True)
    df_Path46 = df_Path46.reset_index(drop=True)
    df_Path61 = df_Path61.reset_index(drop=True)
    df_Path42 = df_Path42.reset_index(drop=True)
    df_Path24 = df_Path24.reset_index(drop=True)
    df_Path45 = df_Path45.reset_index(drop=True)
    
    # select dispatchable imports (positve flow days)
    
    forecast_days = ['fd1','fd2','fd3','fd4','fd5','fd6','fd7']
    
    for i in range(0,len(df_Path66)):     
        
        for fd in forecast_days:
            
            if df_Path42.loc[i,fd] >= 0:
                df_Path42.loc[i,fd] = 0
            else:
                df_Path42.loc[i,fd] = -df_Path42.loc[i,fd]
        
            if df_Path46.loc[i,fd] < 0:
                df_Path46.loc[i,fd] = 0
            else:
                df_Path46.loc[i,fd] = df_Path46.loc[i,fd]*.404 + 424       
    
            if df_Path66.loc[i,fd] < 0:
                df_Path66.loc[i,fd] = 0
    
            if df_Path61.loc[i,fd] < 0:
                df_Path61.loc[i,fd] = 0
    
            if df_Path24.loc[i,fd] < 0:
                df_Path24.loc[i,fd] = 0
    
            if df_Path45.loc[i,fd] < 0:
                df_Path45.loc[i,fd] = 0                    

    # convert to minimum flow time series and dispatchable (daily)
    df_mins = pd.read_excel('Path_setup/CA_imports_minflow_profiles.xlsx',header=0)
     
    for i in range(0,len(df_Path66)):
        
        for fd in forecast_days:
        
            m= 'Path66'
             
            if df_mins.loc[i,m] >= df_Path66.loc[i,fd]:
                df_mins.loc[i,m] = df_Path66.loc[i,fd]
                df_Path66.loc[i,fd] = 0
            
            else:
                df_Path66.loc[i,fd] = np.max((0,df_Path66.loc[i,fd]-df_mins.loc[i,m]))
                
            m= 'Path46_SCE'
             
            if df_mins.loc[i,m] >= df_Path46.loc[i,fd]:
                df_mins.loc[i,m] = df_Path46.loc[i,fd]
                df_Path46.loc[i,fd] = 0
            
            else:
                df_Path46.loc[i,fd] = np.max((0,df_Path46.loc[i,fd]-df_mins.loc[i,m]))
                
            m= 'Path61'
             
            if df_mins.loc[i,m] >= df_Path61.loc[i,fd]:
                df_mins.loc[i,m] = df_Path61.loc[i,fd]
                df_Path61.loc[i,fd] = 0
            
            else:
                df_Path61.loc[i,fd] = np.max((0,df_Path61.loc[i,fd]-df_mins.loc[i,m]))
                
            
            m= 'Path42'
             
            if df_mins.loc[i,m] >= df_Path42.loc[i,fd]:
                df_mins.loc[i,m] = df_Path42.loc[i,fd]
                df_Path42.loc[i,fd] = 0
            
            else:
                df_Path42.loc[i,fd] = np.max((0,df_Path42.loc[i,fd]-df_mins.loc[i,m]))
    
    dispatchable_66 = df_Path66*24
    dispatchable_46 = df_Path46*24
    dispatchable_61 = df_Path61*24
    dispatchable_42 = df_Path42*24
    dispatchable_24 = df_Path24*24
    dispatchable_45 = df_Path45*24
    
    dispatchable_66.columns = forecast_days
    dispatchable_46.columns = forecast_days
    dispatchable_61.columns = forecast_days
    dispatchable_42.columns = forecast_days
    dispatchable_24.columns = forecast_days
    dispatchable_45.columns = forecast_days
    
    dispatchable_66.to_csv('Path_setup/CA_dispatchable_66.csv')
    dispatchable_46.to_csv('Path_setup/CA_dispatchable_46.csv')
    dispatchable_61.to_csv('Path_setup/CA_dispatchable_61.csv')
    dispatchable_42.to_csv('Path_setup/CA_dispatchable_42.csv')
    dispatchable_24.to_csv('Path_setup/CA_dispatchable_24.csv')
    dispatchable_45.to_csv('Path_setup/CA_dispatchable_45.csv')
    
    #    df_data = pd.read_csv('Path_setup/CA_imports.csv',header=0)
    
    # hourly minimum flow for paths
    hourly66 = np.zeros((8760,len(forecast_days)))
    hourly46 = np.zeros((8760,len(forecast_days)))
    hourly61 = np.zeros((8760,len(forecast_days)))
    hourly42 = np.zeros((8760,len(forecast_days)))
    
    for i in range(0,365):
        
        for fd in forecast_days:
            
            fd_index = forecast_days.index(fd)
        
            m = 'Path66'
            hourly66[i*24:i*24+24,fd_index] = np.min((df_mins.loc[i,m], df_Path66.loc[i,fd]))
                   
            m = 'Path46_SCE'
            hourly46[i*24:i*24+24,fd_index] = np.min((df_mins.loc[i,m], df_Path46.loc[i,fd]))
                
            m = 'Path61'
            hourly61[i*24:i*24+24,fd_index] = np.min((df_mins.loc[i,m], df_Path61.loc[i,fd]))
        
            m = 'Path42'
            hourly42[i*24:i*24+24,fd_index] = np.min((df_mins.loc[i,m], df_Path42.loc[i,fd]))   
    
    H66 = pd.DataFrame(hourly66)
    H66.columns = forecast_days
    H66.to_csv('Path_setup/CA_path_mins66.csv')
    
    H46 = pd.DataFrame(hourly46)
    H46.columns = forecast_days
    H46.to_csv('Path_setup/CA_path_mins46.csv')
    
    H61 = pd.DataFrame(hourly61)
    H61.columns = forecast_days
    H61.to_csv('Path_setup/CA_path_mins61.csv')
    
    H42 = pd.DataFrame(hourly42)
    H42.columns = forecast_days
    H42.to_csv('Path_setup/CA_path_mins42.csv')
    
    
    # exports
    
    df_Path66 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path66.csv',header=0,index_col=0)
    df_Path46 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path46.csv',header=0,index_col=0)
    df_Path61 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path61.csv',header=0,index_col=0)
    df_Path42 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path42.csv',header=0,index_col=0)
    df_Path24 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path24.csv',header=0,index_col=0)
    df_Path45 = pd.read_csv('../Stochastic_engine/Synthetic_demand_pathflows/syn_Path45.csv',header=0,index_col=0)    
    
    df_Path66 = df_Path66.loc[year*365:year*365+364,:]
    df_Path46 = df_Path46.loc[year*365:year*365+364,:]
    df_Path61 = df_Path61.loc[year*365:year*365+364,:]
    df_Path42 = df_Path42.loc[year*365:year*365+364,:]
    df_Path24 = df_Path24.loc[year*365:year*365+364,:]
    df_Path45 = df_Path45.loc[year*365:year*365+364,:]    
    
    df_Path66 = df_Path66.reset_index(drop=True)
    df_Path46 = df_Path46.reset_index(drop=True)
    df_Path61 = df_Path61.reset_index(drop=True)
    df_Path42 = df_Path42.reset_index(drop=True)
    df_Path24 = df_Path24.reset_index(drop=True)
    df_Path45 = df_Path45.reset_index(drop=True)
    
    e42 = np.zeros((8760,len(forecast_days)))
    e24 = np.zeros((8760,len(forecast_days)))
    e45 = np.zeros((8760,len(forecast_days)))
    e66 = np.zeros((8760,len(forecast_days)))
      
    #Path 42
    path_profiles42 = pd.read_excel('Path_setup/CA_path_export_profiles.xlsx',sheet_name='Path42',header=None)
    pp42 = path_profiles42.values
    
    #Path 24
    path_profiles24 = pd.read_excel('Path_setup/CA_path_export_profiles.xlsx',sheet_name='Path24',header=None)
    pp24 = path_profiles24.values
    
    #Path 45
    path_profiles45 = pd.read_excel('Path_setup/CA_path_export_profiles.xlsx',sheet_name='Path45',header=None)
    pp45 = path_profiles45.values
    
    #Path 66
    path_profiles66 = pd.read_excel('Path_setup/CA_path_export_profiles.xlsx',sheet_name='Path66',header=None)
    pp66 = path_profiles66.values
    
    for i in range(0,len(df_Path42)):
        
        for fd in forecast_days:
            
            fd_index = forecast_days.index(fd)
            
            if df_Path42.loc[i,fd] > 0:
                e42[i*24:i*24+24,fd_index] = pp42[i,:]*df_Path42.loc[i,fd]
    
            if df_Path24.loc[i,fd] < 0:
                e24[i*24:i*24+24,fd_index] = pp24[i,:]*df_Path24.loc[i,fd]*-1
    
            if df_Path45.loc[i,fd] < 0:
                e45[i*24:i*24+24,fd_index] = pp45[i,:]*df_Path45.loc[i,fd]*-1
    
            if df_Path66.loc[i,fd] < 0:
                e66[i*24:i*24+24,fd_index] = pp66[i,:]*df_Path66.loc[i,fd]*-1
      
    e66 = e66*24
    e45 = e45*24
    e24 = e24*24
    e42 = e42*24
    
    exports66 = pd.DataFrame(e66) 
    exports66.columns = forecast_days
    exports66.to_csv('Path_setup/CA_exports66.csv')
    
    exports45 = pd.DataFrame(e45) 
    exports45.columns = forecast_days
    exports45.to_csv('Path_setup/CA_exports45.csv')
    
    exports24 = pd.DataFrame(e24) 
    exports24.columns = forecast_days
    exports24.to_csv('Path_setup/CA_exports24.csv')
    
    exports42 = pd.DataFrame(e42) 
    exports42.columns = forecast_days
    exports42.to_csv('Path_setup/CA_exports42.csv')    
    
    ##########################3
    ##########################
    
    # HYDRO    
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
