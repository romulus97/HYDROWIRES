# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 19:25:54 2019

@author: Joy Hill
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 12:03:41 2018

@author: Joy Hill
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:14:07 2017

@author: YSu
"""

from pyomo.opt import SolverFactory
from PNW_dispatch import model as m1
from PNW_dispatchLP import model as m2
from pyomo.core import Var
from pyomo.core import Constraint
from pyomo.core import Param
from operator import itemgetter
import pandas as pd
import numpy as np
from datetime import datetime
import pyomo.environ as pyo

def sim(days):
    
    instance = m1.create_instance('data.dat')
    instance2 = m2.create_instance('data.dat')
    
    instance2.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    opt = SolverFactory("cplex")
       
    
    H = instance.HorizonHours
    D = int(H/24)
    K=range(1,H+1)   
    
    #Space to store results
    mwh_1=[]
    mwh_2=[]
    mwh_3=[]
    on=[]
    switch=[]
    srsv=[]
    nrsv=[]
    solar=[]
    wind=[]
    flow=[]
    Generator=[]
    Duals=[]
    
    df_generators = pd.read_csv('generators.csv',header=0)
    
    # forecast days
    forecast_days = []
    for f in range(1,D+1):
        a = 'fd%d' % f
        forecast_days.append(a)
        
    instance.ini_on["COLUMBIA_2"] = 1
    instance.ini_mwh_1["COLUMBIA_2"] = 300
        
    #max here can be (1,365)
    for day in range(1,days+1):
        
        pnwH_first = []
        p66_first = []
        p65_first = []
        p3_first = []
        p8_first = []
        p14_first = []
        
         #load time series data
        for z in instance.zones:
            
            instance.GasPrice[z] = instance.SimGasPrice[z,day]
            instance2.GasPrice[z] = instance.SimGasPrice[z,day]
            
            for i in K:
              
                instance.HorizonDemand[z,i] = instance.SimDemand[z,(day-1)*24+i]
                instance.HorizonWind[z,i] = instance.SimWind[z,(day-1)*24+i]
                instance.HorizonSolar[z,i] = instance.SimSolar[z,(day-1)*24+i]
                instance.HorizonMustRun[z,i] = instance.SimMustRun[z,(day-1)*24+i]
    
                instance2.HorizonDemand[z,i] = instance2.SimDemand[z,(day-1)*24+i]
                instance2.HorizonWind[z,i] = instance2.SimWind[z,(day-1)*24+i]
                instance2.HorizonSolar[z,i] = instance2.SimSolar[z,(day-1)*24+i]
                instance2.HorizonMustRun[z,i] = instance2.SimMustRun[z,(day-1)*24+i]
        
        pnw = 0
        p66 = 0
        p65 = 0
        p3 = 0
        p8 = 0
        p14 = 0
        
        pnw_deficit = 0
        p66_deficit = 0
        p65_deficit = 0
        p3_deficit = 0
        p8_deficit = 0
        p14_deficit = 0      
        
        for d in range(1,D+1):
            
            fd = forecast_days[d-1]
            
            pnw = pnw + instance.SimPNW_hydro[fd,day]
            p66 = p66 + instance.SimPath66_imports[fd,day]
            p65 = p65 + instance.SimPath65_imports[fd,day]
            p3 = p3 + instance.SimPath3_imports[fd,day]
            p8 = p8 + instance.SimPath8_imports[fd,day]
            p14 = p14 + instance.SimPath14_imports[fd,day]
            
        
        if day < 2:
            
            instance.HorizonPNW_hydro = pnw
            instance.HorizonPath66_imports = p66
            instance.HorizonPath65_imports = p65
            instance.HorizonPath3_imports = p3
            instance.HorizonPath8_imports = p8
            instance.HorizonPath14_imports = p14
    
            instance2.HorizonPNW_hydro = pnw
            instance2.HorizonPath66_imports = p66
            instance2.HorizonPath65_imports = p65
            instance2.HorizonPath3_imports = p3
            instance2.HorizonPath8_imports = p8
            instance2.HorizonPath14_imports = p14        
        
        else:
            
            pnw_deficit = pnw_deficit - np.min((0,pnw- np.sum(pnwH_first) + instance.SimPNW_hydro['fd1',day-1]))
            p66_deficit = p66_deficit - np.min((0,p66- np.sum(p66_first) + instance.SimPath66_imports['fd1',day-1]))
            p65_deficit = p65_deficit - np.min((0,p65- np.sum(p65_first) + instance.SimPath65_imports['fd1',day-1]))
            p3_deficit = p3_deficit - np.min((0,p3- np.sum(p3_first) + instance.SimPath3_imports['fd1',day-1]))
            p8_deficit = p8_deficit - np.min((0,p8- np.sum(p8_first) + instance.SimPath8_imports['fd1',day-1]))
            p14_deficit = p14_deficit - np.min((0,p14- np.sum(p14_first) + instance.SimPath14_imports['fd1',day-1]))
        
            instance.HorizonPNW_hydro = np.max((0,pnw - np.sum(pnwH_first) + instance.SimPNW_hydro['fd1',day-1] - pnw_deficit))   
            instance.HorizonPath66_imports = np.max((0,p66 - np.sum(p66_first) + instance.SimPath66_imports['fd1',day-1] - p66_deficit))
            instance.HorizonPath65_imports = np.max((0,p65 - np.sum(p65_first) + instance.SimPath65_imports['fd1',day-1] - p65_deficit))
            instance.HorizonPath3_imports = np.max((0,p3 - np.sum(p3_first) + instance.SimPath3_imports['fd1',day-1] - p3_deficit))
            instance.HorizonPath8_imports = np.max((0,p8 - np.sum(p8_first) + instance.SimPath8_imports['fd1',day-1] - p8_deficit))
            instance.HorizonPath14_imports = np.max((0,p14 - np.sum(p14_first) + instance.SimPath14_imports['fd1',day-1] - p14_deficit))
        
            instance2.HorizonPNW_hydro = np.max((0,pnw - np.sum(pnwH_first) + instance2.SimPNW_hydro['fd1',day-1] - pnw_deficit))   
            instance2.HorizonPath66_imports = np.max((0,p66 - np.sum(p66_first) + instance2.SimPath66_imports['fd1',day-1] - p66_deficit))
            instance2.HorizonPath65_imports = np.max((0,p65 - np.sum(p65_first) + instance2.SimPath65_imports['fd1',day-1] - p65_deficit))
            instance2.HorizonPath3_imports = np.max((0,p3 - np.sum(p3_first) + instance2.SimPath3_imports['fd1',day-1] - p3_deficit))
            instance2.HorizonPath8_imports = np.max((0,p8 - np.sum(p8_first) + instance2.SimPath8_imports['fd1',day-1] - p8_deficit))
            instance2.HorizonPath14_imports = np.max((0,p14 - np.sum(p14_first) + instance2.SimPath14_imports['fd1',day-1] - p14_deficit))
    
            pnw_deficit = np.max((0,pnw_deficit - pnw - np.sum(pnwH_first) + instance.SimPNW_hydro['fd1',day-1]))
            p66_deficit = np.max((0,p66_deficit - p66 - np.sum(p66_first) + instance.SimPath66_imports['fd1',day-1]))
            p65_deficit = np.max((0,p65_deficit - p65 - np.sum(p65_first) + instance.SimPath65_imports['fd1',day-1]))
            p3_deficit = np.max((0,p3_deficit - p3 - np.sum(p3_first) + instance.SimPath3_imports['fd1',day-1]))
            p8_deficit = np.max((0,p8_deficit - p8 - np.sum(p8_first) + instance.SimPath8_imports['fd1',day-1]))
            p14_deficit = np.max((0,p14_deficit - p14 - np.sum(p14_first) + instance.SimPath14_imports['fd1',day-1]))
       
        for i in K:
            instance.HorizonReserves[i] = instance.SimReserves[(day-1)*24+i] 
            instance2.HorizonReserves[i] = instance2.SimReserves[(day-1)*24+i] 
           
        for d in range(1,D+1):
            
            fd = forecast_days[d-1]
            
            for j in range(1,25):
                
                instance.HorizonPath3_exports[(d-1)*24+j] = instance.SimPath3_exports[fd,(day-1)*24+j]
                instance.HorizonPath8_exports[(d-1)*24+j] = instance.SimPath8_exports[fd,(day-1)*24+j]
                instance.HorizonPath14_exports[(d-1)*24+j] = instance.SimPath14_exports[fd,(day-1)*24+j]
                instance.HorizonPath66_exports[(d-1)*24+j] = instance.SimPath66_exports[fd,(day-1)*24+j]    
                instance.HorizonPath65_exports[(d-1)*24+j] = instance.SimPath65_exports[fd,(day-1)*24+j]    
                instance.HorizonPNW_hydro_minflow[(d-1)*24+j] = instance.SimPNW_hydro_minflow[fd,(day-1)*24+j]
                instance.HorizonPath3_minflow[(d-1)*24+j] = instance.SimPath3_imports_minflow[fd,(day-1)*24+j]
                instance.HorizonPath8_minflow[(d-1)*24+j] = instance.SimPath8_imports_minflow[fd,(day-1)*24+j]
                instance.HorizonPath14_minflow[(d-1)*24+j] = instance.SimPath14_imports_minflow[fd,(day-1)*24+j]
                instance.HorizonPath65_minflow[(d-1)*24+j] = instance.SimPath65_imports_minflow[fd,(day-1)*24+j]
                instance.HorizonPath66_minflow[(d-1)*24+j] = instance.SimPath66_imports_minflow[fd,(day-1)*24+j]
    
                instance2.HorizonPath3_exports[(d-1)*24+j] = instance2.SimPath3_exports[fd,(day-1)*24+j]
                instance2.HorizonPath8_exports[(d-1)*24+j] = instance2.SimPath8_exports[fd,(day-1)*24+j]
                instance2.HorizonPath14_exports[(d-1)*24+j] = instance2.SimPath14_exports[fd,(day-1)*24+j]
                instance2.HorizonPath66_exports[(d-1)*24+j] = instance2.SimPath66_exports[fd,(day-1)*24+j]    
                instance2.HorizonPath65_exports[(d-1)*24+j] = instance2.SimPath65_exports[fd,(day-1)*24+j]    
                instance2.HorizonPNW_hydro_minflow[(d-1)*24+j] = instance2.SimPNW_hydro_minflow[fd,(day-1)*24+j]
                instance2.HorizonPath3_minflow[(d-1)*24+j] = instance2.SimPath3_imports_minflow[fd,(day-1)*24+j]
                instance2.HorizonPath8_minflow[(d-1)*24+j] = instance2.SimPath8_imports_minflow[fd,(day-1)*24+j]
                instance2.HorizonPath14_minflow[(d-1)*24+j] = instance2.SimPath14_imports_minflow[fd,(day-1)*24+j]
                instance2.HorizonPath65_minflow[(d-1)*24+j] = instance2.SimPath65_imports_minflow[fd,(day-1)*24+j]
                instance2.HorizonPath66_minflow[(d-1)*24+j] = instance2.SimPath66_imports_minflow[fd,(day-1)*24+j]
    #            
#        PNW_result = opt.solve(instance,tee=True,symbolic_solver_labels=True)
        PNW_result = opt.solve(instance)
        instance.solutions.load_from(PNW_result)   
        
        for j in instance.Generators:
            for t in K:
                if instance.on[j,t] == 1:
                    instance2.on[j,t] = 1
                    instance2.on[j,t].fixed = True
                else:
                    instance.on[j,t] = 0
                    instance2.on[j,t] = 0
                    instance2.on[j,t].fixed = True
    
                if instance.switch[j,t] == 1:
                    instance2.switch[j,t] = 1
                    instance2.switch[j,t].fixed = True
                else:
                    instance2.switch[j,t] = 0
                    instance2.switch[j,t] = 0
                    instance2.switch[j,t].fixed = True
                    
#        results = opt.solve(instance2,tee=True,symbolic_solver_labels=True)
        results = opt.solve(instance2,tee=True,symbolic_solver_labels=True)
        instance2.solutions.load_from(results)
        
        
        print ("Duals")
        
        for c in instance2.component_objects(Constraint, active=True):
    #        print ("   Constraint",c)
            cobject = getattr(instance2, str(c))
            if str(c) == 'Bal5Constraint':
                for index in cobject:
                     if int(index>0 and index<25):
    #                print ("   Constraint",c)
                         Duals.append((str(c),index+((day-1)*24), instance2.dual[cobject[index]]))
    
    #            print ("      ", index, instance2.dual[cobject[index]])
    
     
        #The following section is for storing and sorting results
        for v in instance.component_objects(Var, active=True):
            varobject = getattr(instance, str(v))
            a=str(v)
            if a=='mwh_1':
             
             for index in varobject:
                 
               name = index[0]     
               g = df_generators[df_generators['name']==name]
               seg1 = g['seg1'].values
               seg1 = seg1[0]  
                 
                 
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                    
                    gas_price = instance.GasPrice['PNW'].value
                    
                    
                    if index[0] in instance.Gas:
                        marginal_cost = seg1*gas_price
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Gas',marginal_cost))                  
                    elif index[0] in instance.Coal:
                        marginal_cost = seg1*2
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg1*20
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Oil',marginal_cost))
                    elif index[0] in instance.Nuclear:
                        marginal_cost = 10
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Nuclear',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Slack',marginal_cost))               
                    elif index[0] in instance.Hydro:
                        marginal_cost = 0
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Hydro',marginal_cost))                
                        pnwH_first.append(varobject[index].value)
                
        
                elif index[0] in instance.WECCImports:
                    mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'WECC','imports',0))
                    if index[0] == 'P66I':
                        p66_first.append(varobject[index].value)
                    elif index[0] == 'P65I':
                        p65_first.append(varobject[index].value)
                    elif index[0] == 'P3I':
                        p3_first.append(varobject[index].value)      
                    elif index[0] == 'P8I':
                        p8_first.append(varobject[index].value)  
                    elif index[0] == 'P14I':
                        p14_first.append(varobject[index].value)  
                        
            if a=='mwh_2':
           
             for index in varobject:
                 
               name = index[0]     
               g = df_generators[df_generators['name']==name]
               seg2 = g['seg2'].values
               seg2 = seg2[0]  
    
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                    
                    gas_price = instance.GasPrice['PNW'].value
                    
                    if index[0] in instance.Gas:
                        marginal_cost = seg2*gas_price
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Gas',marginal_cost))                  
                    elif index[0] in instance.Coal:
                        marginal_cost = seg2*2
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg2*20
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Oil',marginal_cost))
                    elif index[0] in instance.Nuclear:
                        marginal_cost = 10
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Nuclear',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Slack',marginal_cost))               
                    elif index[0] in instance.Hydro:
                        marginal_cost = 0
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Hydro',marginal_cost))         
                        pnwH_first.append(varobject[index].value)
                        
                elif index[0] in instance.WECCImports:
                    mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'WECC','imports',0))
                    if index[0] == 'P66I':
                        p66_first.append(varobject[index].value)
                    elif index[0] == 'P65I':
                        p65_first.append(varobject[index].value)
                    elif index[0] == 'P3I':
                        p3_first.append(varobject[index].value)      
                    elif index[0] == 'P8I':
                        p8_first.append(varobject[index].value)  
                    elif index[0] == 'P14I':
                        p14_first.append(varobject[index].value)  
            
            if a=='mwh_3':
               
             for index in varobject:
                 
               name = index[0]     
               g = df_generators[df_generators['name']==name]
               seg3 = g['seg3'].values
               seg3 = seg3[0]  
                 
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                    
                    gas_price = instance.GasPrice['PNW'].value
                    
                    if index[0] in instance.Gas:
                        marginal_cost = seg3*gas_price
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Gas',marginal_cost))                  
                    elif index[0] in instance.Coal:
                        marginal_cost = seg3*2
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg3*20
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Oil',marginal_cost))
                    elif index[0] in instance.Nuclear:
                        marginal_cost = 10
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Nuclear',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Slack',marginal_cost))               
                    elif index[0] in instance.Hydro:
                        marginal_cost = 0
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Hydro',marginal_cost))         
                
                elif index[0] in instance.WECCImports:
                    mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'WECC','imports',0))
                    pnwH_first.append(varobject[index].value)
                    if index[0] == 'P66I':
                        p66_first.append(varobject[index].value)
                    elif index[0] == 'P65I':
                        p65_first.append(varobject[index].value)
                    elif index[0] == 'P3I':
                        p3_first.append(varobject[index].value)      
                    elif index[0] == 'P8I':
                        p8_first.append(varobject[index].value)  
                    elif index[0] == 'P14I':
                        p14_first.append(varobject[index].value) 
                        
            if a=='on':
                
             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                 on.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW'))
                 
          
             
            if a=='switch':
            
             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                 switch.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW'))
               
        
             
            if a=='srsv':
            
             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                 srsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW'))
              
        
             
            if a=='nrsv':
           
             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                 nrsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW'))
               
             
             
            if a=='solar':
               
             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                solar.append((index[0],index[1]+((day-1)*24),varobject[index].value))   
             
              
            if a=='wind':
               
             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                wind.append((index[0],index[1]+((day-1)*24),varobject[index].value))  
                   
            for j in instance.Generators:
                if instance.on[j,24] == 1:
                    instance.on[j,0] = 1
                else: 
                    instance.on[j,0] = 0
                instance.on[j,0].fixed = True
                           
                if instance.mwh_1[j,24].value <=0 and instance.mwh_1[j,24].value>= -0.0001:
                    newval_1=0
                else:
                    newval_1=instance.mwh_1[j,24].value
                instance.mwh_1[j,0] = newval_1
                instance.mwh_1[j,0].fixed = True
                              
                if instance.mwh_2[j,24].value <=0 and instance.mwh_2[j,24].value>= -0.0001:
                    newval=0
                else:
                    newval=instance.mwh_2[j,24].value
                                         
                if instance.mwh_3[j,24].value <=0 and instance.mwh_3[j,24].value>= -0.0001:
                    newval2=0
                else:
                    newval2=instance.mwh_3[j,24].value
                                          
                                          
                instance.mwh_2[j,0] = newval
                instance.mwh_2[j,0].fixed = True
                instance.mwh_3[j,0] = newval2
                instance.mwh_3[j,0].fixed = True 
                if instance.switch[j,24] == 1:
                    instance.switch[j,0] = 1
                else:
                    instance.switch[j,0] = 0
                instance.switch[j,0].fixed = True
              
                if instance.srsv[j,24].value <=0 and instance.srsv[j,24].value>= -0.0001:
                    newval_srsv=0
                else:
                    newval_srsv=instance.srsv[j,24].value
                instance.srsv[j,0] = newval_srsv 
                instance.srsv[j,0].fixed = True        
        
                if instance.nrsv[j,24].value <=0 and instance.nrsv[j,24].value>= -0.0001:
                    newval_nrsv=0
                else:
                    newval_nrsv=instance.nrsv[j,24].value
                instance.nrsv[j,0] = newval_nrsv 
                instance.nrsv[j,0].fixed = True        
                   
        print(day)
    
    mwh_1_pd=pd.DataFrame(mwh_1,columns=('Generator','Time','Value','Zones','Type','$/MWh'))
    mwh_2_pd=pd.DataFrame(mwh_2,columns=('Generator','Time','Value','Zones','Type','$/MWh'))
    mwh_3_pd=pd.DataFrame(mwh_3,columns=('Generator','Time','Value','Zones','Type','$/MWh'))
    on_pd=pd.DataFrame(on,columns=('Generator','Time','Value','Zones'))
    switch_pd=pd.DataFrame(switch,columns=('Generator','Time','Value','Zones'))
    srsv_pd=pd.DataFrame(srsv,columns=('Generator','Time','Value','Zones'))
    nrsv_pd=pd.DataFrame(nrsv,columns=('Generator','Time','Value','Zones'))
    solar_pd=pd.DataFrame(solar,columns=('Zone','Time','Value'))
    wind_pd=pd.DataFrame(wind,columns=('Zone','Time','Value'))
    shadow_price=pd.DataFrame(Duals,columns=('Constraint','Time','Value'))
        
    mwh_1_pd.to_csv('mwh_1.csv')
    mwh_2_pd.to_csv('mwh_2.csv')
    mwh_3_pd.to_csv('mwh_3.csv')
    on_pd.to_csv('on.csv')
    switch_pd.to_csv('switch.csv')
    srsv_pd.to_csv('srsv.csv')
    nrsv_pd.to_csv('nrsv.csv')
    solar_pd.to_csv('solar_out.csv')
    wind_pd.to_csv('wind_out.csv')
    shadow_price.to_csv('shadow_price.csv')
    
    return None
