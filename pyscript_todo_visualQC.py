#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:52:10 2021

@author: kameshwari
"""

import matplotlib.pyplot as mplt
import os
import glob
import pandas as pd
import statistics
import numpy as np


inpath1 = '/media/kameshwari/Partition_E/work/marine-met/iraws/iraws_qc_reports/AWSDATA/AWSQC/06032023/'
inpath2 = '/media/kameshwari/Partition_E/work/marine-met/iraws/iraws_qc_reports/AWSDATA/AWSQC/06032023/';

#inpath1 = '/home/kameshwari/kanthi/incois/work/iraws/25052021/AWSDATA/'
#inpath2 = '/home/kameshwari/kanthi/incois/work/iraws/25052021/AWSDATA/JAN-FEB-MAR-2021/DATA10MIN/';
#ff = open(inpath2 + 'qcflags0.txt',"w+")
os.chdir(inpath2)
files = glob.glob('*SARVEKSHAK*.xlsx')

qc_varname=['slp','dbt','rh','sst','ws','wdir','rain','lwr','swr'];
variables = ['air_pressure','air_temperature','humidity','sst','wind_speed','wind_direction','rain_guage','long_wave_radiation','short_wave_radiation'];
qcflags = pd.read_csv(inpath2 + 'qcflags_values_t.csv')
# to plot

# for filename in files :

#     # getting height of the ship from Height_of_AWS.xlsx file
#     shipname = filename[0:len(filename)-5]
#     Data = pd.read_excel(io = inpath2 + filename)

for filename in files[:] :
    # reading data file..
    Data0 = pd.read_csv(inpath2 + filename)
    Data0.ship_name = [str1.upper() for str1 in Data0.ship_name]
    Data0.ship_name = [str1.replace(' ','') for str1 in Data0.ship_name]
    Data0.ship_name = [str1.replace('MASTYA','MATSYA') for str1 in Data0.ship_name]
    shipnames = Data0.ship_name.unique()
    
    for shipname in shipnames :
    # getting height of the ship from Height_of_AWS.xlsx file
        # shipname = filename[0:len(filename)-5]
        Data = Data0[Data0.ship_name == shipname]

        data = Data.drop_duplicates(subset = None, inplace = False)
        data.reset_index(inplace = True)
    
        # data.columns = data.columns.str.replace(" ","")
        rr = len(data.observation_time)
        for ii in range(len(variables)):
            var = list(data.eval(variables[ii]))
            qcfl = list(qcflags[str(shipname) + '_' + qc_varname[ii]])
            
            keyy = str(str(shipname) + '_' + qc_varname[ii])
            ll = len(qcflags[keyy])
            numer = [ii for ii in range(ll) if qcflags[keyy][ii] == 8]
            percnt = 100 - ((len(numer)/ll)*100)
            
            
            xaxiss = list(range(len(var)))
            # xaxiss = str(data.Time)
            fig,ax = mplt.subplots()
            std = 4*statistics.stdev(var)
            mm = statistics.mean(var)
            ind = [ii  for ii in range(len(var)) if ((var[ii]-mm < -1*std) | (var[ii]-mm > std))]
            if len(ind) > 0 : 
                for item in ind:
                    var[item] = np.nan

            ax.plot(xaxiss[0:],var[0:], color="red", marker="o")
            ax.set_xlabel("number",fontsize=14)
            ax.set_ylabel("var",color="red",fontsize=14)
            
    #        xaxiss = list(range(len(qcfl)))
            ax2=ax.twinx()
            
            ax2.plot(xaxiss[:],qcfl[0:len(xaxiss)],color="cyan",alpha = 0.3,marker=".")
            ax2.set_ylabel("qcflag",color="cyan",fontsize=14)
            mplt.title(str(shipname) + '_' + qc_varname[ii] + '   Percent=' + str(percnt))
            mplt.show()
    
    
            
            # len(var)
