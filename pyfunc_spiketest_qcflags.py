#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 12:00:11 2021

@author: kameshwari
"""
from datetime import datetime as dt
import statistics as st

# year = [2000,2000,2000,2000,2000,2000,2000,2000,2000,2000]
# month = [1,1,1,1,1,1,1,1,1,1]
# date = [1,1,1,2,2,2,2,2,2,2]
# hour = [21,22,23,0,1,2,3,4,5,6]
# mins = [10,10,10,10,10,10,10,10,10,10]
# sec = [0,0,0,0,0,0,0,0,0,0]
# var = [20,20.3,20.4,20.6,20.5,20.8,20.3,28,20.6,20.3]


def pyfunc_spiketest_qcflags(rr,var,year,month,date,hour,mins,sec,k):
    spikes = []
    sss=1; # k is no of values around each number to be considered
    for ii in range(rr):
        print(ii)
        datenum = []
        if ((ii>=k) & (ii<=rr-k-1)):
            dd = 0
            for tt in range(ii-k,ii+k+1):
                D = dt(year[tt],month[tt],date[tt],hour[tt],mins[tt],sec[tt]) #converting normal nummbers of year, month, adte....into DATETIME timestamp
                temp1 = 366 + dt.toordinal(D)  #converting the DATETIME into equivalent matlab datenum (but without considering the values of hh,mm,ss)
                temp2 = D - dt.fromordinal(D.toordinal()) # calculating the time difference of the DATETIME with and without hh,mm,ss (so basically we will get hh,mm,ss separately from D in some strict format read by datetime mudule)
                temp3 = temp2.total_seconds()/(24*60*60) # converting that hh.mm,ss fixed format into seconds
                datenum.append(temp1 + temp3) # now adding datenums of both yyyy.mm.dd and hh.mm.ss
                dd=dd+1;
            diff1 = [x - datenum[i - 1] for i, x in enumerate(datenum)][1:]
            if all(x >= -0.5 for x in diff1) & all(x < 0.5 for x in diff1): #if the observations are made within 12 hours
                m = st.mean(var[ii-k:ii+k+1]);
                s = st.stdev(var[ii-k:ii+k+1]);
                if (abs(var[ii]-m) >= 1.6*s):
                    print('i am a spike');
                    spikes.append(ii);
                    sss = sss+1;
        if (sss == 1) & (ii == rr):
            spikes.append([]);
    return spikes

