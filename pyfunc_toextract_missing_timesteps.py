#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 08:28:35 2021

@author: kameshwari
"""


from datetime import datetime as dt
import numpy as np

data_datenums = []
timeaxiss_datenums = []

def pyfunc_toextract_missing_timesteps(timeaxiss, data, intrvl):
    
    indd = []                                                                                                                                                                                                                                    
    missing = 0
    rr = len(data.observation_time)
    data_dates = [dt(data.observation_time[ii].year, data.observation_time[ii].month, data.observation_time[ii].day,\
                     data.observation_time[ii].hour, data.observation_time[ii].minute, data.observation_time[ii].second) \
                  for ii in range(rr)]
        
    for ii in range(len(timeaxiss)):
        print(ii)
        diff = [timeaxiss[ii] - data_dates[jj] for jj in range(rr)]#(data_datenums)]
        diff_sec = [diff[jj].total_seconds() for jj in range(rr)]
        ind1 = [jj for jj in range(rr) if np.abs(diff_sec[jj]) < 3600]
        ind2 = [jj for jj in ind1 if timeaxiss[ii].hour == data_dates[jj].hour]
        if intrvl == 10:
            if (len(ind2) == 0): missing = missing + 6 
            if (len(ind2) < 6) & (len(ind2) > 0): missing = missing + (6 - len(ind2))
        elif intrvl == 30:
            if (len(ind2) == 0): 
                missing = missing + 3 
                indd.append(timeaxiss[ii])    
        elif intrvl == 60:
            if (len(ind2) == 0): 
                missing = missing + 1 
                indd.append(timeaxiss[ii])

    return missing, indd    

# pyfunc_toextract_missing_timesteps(timeaxiss,data,intrvl)            
            


#%%            
    # for ii in range(rr):
    #     print(ii)
    #     diff = [timeaxiss[jj] - data_dates[ii] for jj in range(len(timeaxiss))]#(data_datenums)]
    #     diff_sec = [diff[jj].total_seconds() for jj in range(len(timeaxiss))]
    #     ind1 = [jj for jj in range(len(timeaxiss)) if np.abs(diff_sec[jj]) < 3600]
    #     if  any(np.abs(diff_sec) < 3600 ) == 0:
    #         missing = missing + 1        
    
    # data_dates_datenums = [dt.toordinal(data_dates[ii]) + 366 for ii in range(rr)]
    # temp1 = [data_dates[ii] - dt.fromordinal(data_dates[ii].toordinal()) for ii in range(rr)]
    # data_hourminsec_datenums = [temp1[ii].total_seconds()/(24*60*60) for ii in range(rr)]
    # data_datenums = [data_dates_datenums[ii] + data_hourminsec_datenums[ii]for ii in range(rr)]
    
    # timeaxiss_dates_datenums = [dt.toordinal(timeaxiss[ii]) + 366 for ii in range(len(timeaxiss))]
    # temp1 = [timeaxiss[ii] - dt.fromordinal(timeaxiss[ii].toordinal()) for ii in range(len(timeaxiss))]
    # timeaxiss_hourminsec_datenums = [temp1[ii].total_seconds()/(24*60*60) for ii in range(len(timeaxiss))]
    # timeaxiss_datenums = [timeaxiss_dates_datenums[ii] + timeaxiss_hourminsec_datenums[ii]for ii in range(len(timeaxiss))]


    # for ii in range(len(timeaxiss_datenums)):
    #     diff = [timeaxiss_datenums[ii] - data_datenums[jj] for jj in range(rr)]#(data_datenums)]
    #     if  any(np.abs(diff) < 0.0416666667) != 1:
    #         missing = missing + 1
    
    
    
    
