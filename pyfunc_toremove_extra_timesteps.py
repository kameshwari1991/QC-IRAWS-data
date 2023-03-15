#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 11:22:47 2021

@author: kameshwari
"""

from datetime import datetime as dt
import numpy as np


def pyfunc_toremove_extra_timesteps(timeaxiss, data, intrvl):
    
    rr = len(data.Date)
    data_dates = [dt(data.Date[ii].year, data.Date[ii].month, data.Date[ii].day,\
                     data.Time[ii].hour, data.Time[ii].minute, data.Time[ii].second) \
                  for ii in range(rr)]
    indd = []    
    for ii in range(len(timeaxiss)):
        print(ii)
        rr = len(data.Date)
       
        temp = np.repeat([timeaxiss[ii]],rr)
        diff = np.subtract(temp,data_dates)
        # diff = [timeaxiss[ii] - data_dates[jj] for jj in range(rr)]#(data_datenums)]
        diff_sec = [diff[jj].total_seconds() for jj in range(rr)]
        ind1 = [jj for jj in range(rr) if np.abs(diff_sec[jj]) < 3600]
        ind2 = [jj for jj in ind1 if timeaxiss[ii].hour == data_dates[jj].hour]
        if intrvl == 10:
            if (len(ind2) > 6): 
                data = data.drop(index = ind2[6:]);
                for jj in sorted(ind2[6:], reverse=True): del data_dates[jj] 
                indd.append(ind2[6:])
                data = data.reset_index(drop = True, inplace = False)
        elif intrvl == 60:
            if (len(ind2) > 1): 
                data = data.drop(index = ind2[1:]); 
                for jj in sorted(ind2[1:], reverse=True): del data_dates[jj]
                indd.append(ind2[1:])
                data = data.reset_index(drop = True, inplace = False)
    return data, indd

#%%
#data = pyfunc_toremove_extra_timesteps(timeaxiss, data0, intrvl)    



