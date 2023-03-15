# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# this script is written to process the data which Arun has asked on
# purpose for some payment...whether they should pay the vendors or
# not...27112019

# using this code again for the same above purpose_19/02/2020

# using this code "mscript_toprocess_irawsdata3.m" again for the same above purpose_13/05/2020

# using this code "mscript_toprocess_irawsdata4.m" again for the same above purpose_04/08/2020
# %%
import pandas as pd
import numpy as np
import os
# os.chdir('/media/kameshwari/Partition_E/work/scripts/py_scripts/')
os.chdir('/media/kameshwari/Partition_E/work/marine-met/iraws/iraws_qc_reports/qc_generic/')
from pyfunc_climatological_stdevcheck_mm import *
import qc_timesequence as tscheck1
import glob
import math as math
from pyfunc_spiketest_qcflags import *
from pyfunc_stuckvaluetest_qcflags import *
from pyfunc_rainfalltest_qcflags import *
from pyfunc_toextract_missing_timesteps import *
from pyfunc_toremove_extra_timesteps import *
import datetime as dt
import itertools
import csv
#from 

inpath0 = '/media/kameshwari/Partition_E/work/marine-met/iraws/iraws_qc_reports/qc_generic/'
# inpath1 = '/media/kameshwari/Partition_E/work/marine-met/iraws/iraws_qc_reports/AWSDATA/AWSQC/DATA_QC 2021/'
# inpath2 = '/media/kameshwari/Partition_E/work/marine-met/iraws/iraws_qc_reports/AWSDATA/AWSQC/DATA_QC 2021/30MIN-AMJ-2021/';
inpath1 = '/media/kameshwari/Partition_E/work/marine-met/iraws/iraws_qc_reports/AWSDATA/AWSQC/06032023/'
inpath2 = '/media/kameshwari/Partition_E/work/marine-met/iraws/iraws_qc_reports/AWSDATA/AWSQC/06032023/';
## some inputs to be given in the beginning...check them thoroughly
speciall = 15 # 6-amj 15-jfm 8-ond  # more for winter season as more num of night timesteps...
startt = '2023-02-01 00:00:00'
endd = '2023-02-28 23:00:00'
timeaxiss = pd.date_range(start = startt, end = endd, freq = 'H')
## beginning
ff = open(inpath2 + 'qcflags_statistics_60min_t.txt',"w+")
os.chdir(inpath2)
files = glob.glob('*.csv')
heights =  pd.read_excel(io = inpath0 + 'Height_of_AWS.xlsx', engine='openpyxl')  
qcflags = {}
qc_varname = ['slp','dbt','rh','sst','ws','wdir','rain','lwr','swr'];
# files = glob.glob('*DARSHAK*.xlsx')


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
        ind1 = list(heights.Ship_Name).index(shipname.replace(' ',''))
        zz = heights.height[ind1]
        Data = Data0[Data0.ship_name == shipname]
    # the first step of QC is to remove the duplicates in the data...whole record being repeated...
        data0 = Data.drop_duplicates(subset = None, inplace = False)
        data0 = data0.reset_index(inplace = False, drop = True)
        data0.columns = data0.columns.str.replace(" ","") # removing any spaces in the column names in the dataframe
    # send the data to a routine, to remove extra timesteps..
        # data, indd = pyfunc_toremove_extra_timesteps(timeaxiss, data0, intrvl)    
        data = data0 ; rr = len(data.ship_name)
        
        data['observation_time'] = [dt.datetime.strptime(data.observation_time[ii],'%Y-%m-%d %H:%M:%S') for ii in range(rr)]
        temp1 = data.observation_time[0]
        temp2 = data.observation_time[1]
        diff = (temp2 - temp1).total_seconds()/60  
        intrvl = 60
    # extracting year,month and all to input to timesequence check
    # %
        year0 = pd.DatetimeIndex(data.observation_time).year
        month0 = pd.DatetimeIndex(data.observation_time).month
        date0 = pd.DatetimeIndex(data.observation_time).day
        kk = 0; hour0 = []; minute0 = []
        for kk in range(rr):
            hour0.append(data.observation_time[kk].hour)
            minute0.append(data.observation_time[kk].minute)
        latitude0 = list(data.latitude)
        longitude0 = list(data.longitude)
        second0 = np.repeat([0],rr)
        ll = 0  #dummy variable
    # %%
        qc_temp = tscheck1.mqc_of_imma_csv(year0,month0,date0,hour0,minute0,second0,latitude0,longitude0,ll,rr)
        qcflags[str(shipname) + '_timesequence'] = qc_temp
    # %%
        
    # position lat-lon check
        indlat = data[(data['latitude'] >= -90) & (data['latitude'] <= 90)].index.tolist()
        for ii in range(rr):
            if data['longitude'][ii] < 0.0 : data['longitude'][ii] = data['longitude'][ii] + 360.0 
        indlon = data[(data['longitude'] >= 0) & (data['longitude'] <= 360)].index.tolist()
        ind1 = list(set.intersection(set(indlat), set(indlon))) 
    #   ind2=find(data1(:,7)==0 & data1(:,8)==0); # if compass value has to be checked
        qcflags[str(shipname) + '_location']=np.repeat([8],rr); qcflags[str(shipname) + '_location'][ind1] = 1 
            
    #___________________________________range check_______________________________
            
        temp = [(year0 >= 2019)&(year0 <= 2023)]; ind_yy = np.where(temp)[1]
        temp = [(month0 >= 1)&(month0 <= 12)]; ind_mm = np.where(temp)[1]
        temp = [(date0 >= 1)&(date0 <= 31)]; ind_dd = np.where(temp)[1]
        temp = [(np.array(hour0) >= 0)&(np.array(hour0) <= 24)]; ind_hh = np.where(temp)[1]
        temp = [(np.array(minute0) >= 0)&(np.array(minute0) <= 60)]; ind_min = np.where(temp)[1]
        temp = [(second0 >= 0)&(second0 <= 60)]; ind_sec = np.where(temp)[1]
        
        ind_time = list(set.intersection(set(ind_yy),set(ind_mm),set(ind_dd),set(ind_hh),set(ind_min),set(ind_sec)));
        qcflags[str(shipname) + '_time'] = np.repeat([8],rr); qcflags[str(shipname) + '_time'][ind_time] = 1
        
    #______________________________climate variables____________________  
        # data['sst'] = -999
    #    % latitude variation cause to dbt range
        temp = [(np.array(latitude0)>30) | (np.array(latitude0)<-30)]; ind_ns_lat = np.where(temp)[1]
        temp = [(np.array(latitude0)<=30) | (np.array(latitude0)>=-30)]; ind_trop_lat = np.where(temp)[1]
        
    #    % recomputing air pressure to sea level
        a = []; a = list(np.repeat(0.0342*zz,rr))
        b = []; b = list(data.air_temperature + 273.15)
        temp = []; temp = list(data.air_pressure)
        temp1= []; temp1 = temp * np.exp([i / j for i,j in zip(a,b)])
        data.air_pressure = np.round(temp1,2);
        del(temp); del(temp1)
        
    #    %  range qc for variables
        ind_slp = data[(data['air_pressure'] >= 970) & (data['air_pressure'] <= 1040)].index.tolist()
        temp = (data.air_temperature[ind_trop_lat] >= 10) & (data.air_temperature[ind_trop_lat] <= 50)
        if len(temp) == 0:
            ind_dbt1 = []        
        elif len(temp) == 1:
            ind_dbt1 = [0]
        else:
            ind_dbt1 = list(temp)
        temp = (data.air_temperature[ind_ns_lat] >= -40) & (data.air_temperature[ind_ns_lat] <= 50) if ind_ns_lat.size != 0 else []
        if len(temp) == 0:
            ind_dbt2 = []        
        elif len(temp) == 1:
            ind_dbt2 = [0]
        else:
            ind_dbt2 = list(temp)
        ind_dbt = np.append(ind_trop_lat[ind_dbt1] , ind_ns_lat[ind_dbt2]);
        ind_rh = data[(data.humidity >= 55) & (data.humidity <= 100)].index.tolist();
        temp = (data.sst[ind_trop_lat] >= 7) & (data.sst[ind_trop_lat] <= 40)
        if len(temp) == 0:
            ind_sst1 = []        
        elif len(temp) == 1:
            ind_sst1 = [0]
        else:
            ind_sst1 = list(temp)
        temp = (data.sst[ind_ns_lat] >= -10) & (data.sst[ind_ns_lat] <= 50) if ind_ns_lat.size != 0 else []
        if len(temp) == 0:
            ind_sst2 = []        
        elif len(temp) == 1:
            ind_sst2 = [0]
        else:
            ind_sst2 = list(temp)
        ind_sst = np.append(ind_trop_lat[ind_sst1] , ind_ns_lat[ind_sst2]);
        ind_ws = data[(data.wind_speed >= 0.5) & (data.wind_speed <= 40)].index.tolist();
        ind_wdir = data[(data.wind_direction >= 0) & ( data.wind_direction <= 360)].index.tolist();
        ind_rain = data[(data.rain_guage >= 0) & (data.rain_guage <= 50)].index.tolist();
        ind_lwr = data[(data.long_wave_radiation >= 0) & (data.long_wave_radiation <= 700)].index.tolist();
        ind_swr = data[(data.short_wave_radiation >= 0) & (data.short_wave_radiation <= 1380)].index.tolist();
        
        
        qcflags[str(shipname) + '_slp'] = np.repeat([8],rr); qcflags[str(shipname) + '_slp'][ind_slp] = 1;
        qcflags[str(shipname) + '_dbt'] = np.repeat([8],rr); qcflags[str(shipname) + '_dbt'][ind_dbt] = 1;
        qcflags[str(shipname) + '_rh'] = np.repeat([8],rr); qcflags[str(shipname) + '_rh'][ind_rh] = 1;
        qcflags[str(shipname) + '_sst'] = np.repeat([8],rr); qcflags[str(shipname) + '_sst'][ind_sst] = 1;
        qcflags[str(shipname) + '_ws'] = np.repeat([8],rr); qcflags[str(shipname) + '_ws'][ind_ws] = 1;
        qcflags[str(shipname) + '_wdir'] = np.repeat([8],rr); qcflags[str(shipname) + '_wdir'][ind_wdir] = 1;
        qcflags[str(shipname) + '_rain'] = np.repeat([8],rr); qcflags[str(shipname) + '_rain'][ind_rain] = 1;
        qcflags[str(shipname) + '_lwr'] = np.repeat([8],rr); qcflags[str(shipname) + '_lwr'][ind_lwr] = 1;
        qcflags[str(shipname) + '_swr'] = np.repeat([8],rr); qcflags[str(shipname) + '_swr'][ind_swr] = 1;
        
        del( ind_slp, ind_dbt , ind_rh , ind_sst, a ,b, ind_dbt1, ind_dbt2, ind_sst1, ind_sst2)
        del(ind_ws, ind_rain,  ind_lwr, ind_swr )
        
        # ind1 = qcflags[str(shipname) + '_location'][qcflags[str(shipname) + '_location'] == 8]
        # ind2 = qcflags[str(shipname) + '_timesequence'][qcflags[str(shipname) + '_timesequence'] == 8]
        # ind3 = qcflags[str(shipname) + '_time'][qcflags[str(shipname) + '_time'] == 8]
        
        ind1 = np.where(qcflags[str(shipname) + '_location'] == 8)
        ind2 = np.where(qcflags[str(shipname) + '_timesequence'] == 8)
        ind3 = np.where(qcflags[str(shipname) + '_time'] == 8)

    
        ind = np.append(np.append(ind1,ind2),ind3); 
        
        if ind.size != 0:
            temp = set(ind); ind = list(temp)
            for jj in range(9) :
                qcflags[str(shipname) + '_' + qc_varname[jj]][np.array(ind)] = 8;
    
    #    %%%%%%%%%%%%%%%%%%%%spike test%%%%%%%%%%%%%%%%%%%%%%%%%
        variables = ['air_pressure','air_temperature','humidity','sst','wind_speed','wind_direction','rain_guage','long_wave_radiation','short_wave_radiation'];
        qcvarind = [0,1,2,3,4,7]
        for ii in qcvarind:
            var = list(data.eval(variables[ii]));
            spikes = pyfunc_spiketest_qcflags(rr,var,year0,month0,date0,hour0,minute0,second0,3);
            if len(spikes) != 0 :
                qcflags[str(shipname) + '_' +  qc_varname[ii]][spikes] = 8;
            del(var,spikes)
           
    #   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%stuck value test%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        variables = ['air_pressure','air_temperature','humidity','sst','wind_speed','wind_direction','rain_guage','long_wave_radiation','short_wave_radiation'];
        qcvarind = [0,1,2,3,4,5,7,8]
        diff = intrvl
        if diff == 10:
            rpnum1 = 80; rpnum2 = 6;
        elif diff == 30: 
            rpnum1 = 30; rpnum2 = 4;
        else:
            rpnum1=speciall; rpnum2 = 3;
        
            
        for jj in qcvarind:
            print(jj,qc_varname[jj],variables[jj])
            rpnum=rpnum2;
            if jj == 8 : rpnum = rpnum1;
            var = list(data.eval(variables[jj]))
            bad = pyfunc_stuckvaluetest_qcflags(var,rpnum);
            stuck = [j for i in bad for j in i]
            if len(stuck) != 0:
                qcflags[str(shipname) + '_' + qc_varname[jj]][stuck] = 8;
            
            del(var,stuck)
            
           
    #....%%%%%%%%%%%%%%%%%%%%%%%%%%%%%special test for rain data%%%%%%%%%%%%%
    
        print('started checking rain')
        var = list(data.rain_guage)
        badd = pyfunc_rainfalltest_qcflags(var,hour0);
        qcflags[str(shipname) + '_rain'][badd] = 8;
        print('done rain QC')
    
    
    #      %%%%%%%%%%%%%%%%%%%%%%%%%%%%% stdev within test %%%%%%%%%%%%%%%%%%%
    
    
            # variables = ['air_pressure','air_temperature','humidity','sst','wind_speed','wind_direction','rain_guage','long_wave_radiation','short_wave_radiation'];
            # qcvarind = [0,1,2,3,4,5,6,7,8]
            
            # for ii in qcvarind:
            #     var = list(data.eval(variables[jj]))
            #     mean1 = st.mean(var)
            #     std1 = st.stdev(var)
            #     deviation1 = var - np.repeat(mean1,rr)
            #     ind = [ii for ii in range(rr) if abs(deviation1[ii]) > 3*std1]
    
    #______________________________________climatological stdev check__________________________
    
        inpathclim = '/media/kameshwari/Partition_E/work/marine-met/icoads/noaa_gridded/mm/'
        variablelist = ['slp', 'dbt', 'rhum', 'sst', 'uwnd','vwnd']
        data00 = pd.DataFrame(columns = ['year4','month4','date4','hour4','minute4','lon4','lat4',\
                                         'slp','dbt','rhum','sst','uwnd','vwnd'], index=range(len(data.index)))
        data00.year4 = pd.DatetimeIndex(data.observation_time).year
        data00.month4 = pd.DatetimeIndex(data.observation_time).month
        data00.date4 = pd.DatetimeIndex(data.observation_time).day
        hour0 = []; minute0 = []
        for kk in range(rr):
            hour0.append(data.observation_time[kk].hour)
            minute0.append(data.observation_time[kk].minute)
        data00.hour4 = hour0
        data00.minute4 = minute0
        data00.lat4 = data.latitude; data00.lon4 = data.longitude;
        for item1,item2 in zip(['slp','dbt','rhum','sst'], ['air_pressure','air_temperature','humidity','sst']):
            data00[item1] = data[item2]
        uwnd = []; vwnd = []
        for ii in range(len(data.index)) :  
            uwnd.append(-1.0 * data['wind_speed'][ii] * np.sin((3.142/180.0) * data['wind_direction'][ii]) if (data['wind_speed'][ii] != -999.9) & (data['wind_direction'][ii] != '-999.9') else -999.9)
            vwnd.append(-1.0 * data['wind_speed'][ii] * np.cos((3.142/180.0) * data['wind_direction'][ii]) if (data['wind_speed'][ii] != -999.9) & (data['wind_direction'][ii] != '-999.9') else -999.9)   
        data00['uwnd'] = uwnd; data00['vwnd'] = vwnd
        qcf1 = pyfunc_climatological_stdevcheck_mm(inpathclim,variablelist,data00) 
        ind1 = np.logical_or(qcf1.uwnd == 8, qcf1.vwnd == 8)
        qcflags[shipname + '_ws'][ind1 == True] = 8; qcflags[shipname + '_wdir'][ind1 == True] = 8;    
        qcflags[shipname + '_slp'][qcf1.slp == 8] = 8
        qcflags[shipname + '_dbt'][qcf1.dbt == 8] = 8
        qcflags[shipname + '_rh'][qcf1.rhum == 8] = 8
        qcflags[shipname + '_sst'][qcf1.sst == 8] = 8
        
        
    #____________________________________ missing timesteps_______________________________________
    
        missing, indd = pyfunc_toextract_missing_timesteps(timeaxiss,data,intrvl)
    
    #________________________ special test for SWR night timesteps__________________________________
    
    # nightts = [['19:00:00','06:00:00'],['19:00:00','06:00:00'],['19:00:00','05:15:00'],\
    #            ['19:00:00','05:15:00'],['19:00:00','05:15:00'],['19:00:00','05:15:00'],\
    #            ['19:00:00','05:30:00'],['19:00:00','05:30:00'],['19:00:00','05:30:00'],]
        
        for ii in range(rr):
            print(ii)
            timegap_hrs = data0.longitude[ii] / 15    
            localtime = (data0.observation_time[ii] + dt.timedelta(hours = timegap_hrs)).time()
            if ((localtime.hour >= 19) & (localtime.hour <= 23)) | ((localtime.hour >= 0) & (localtime.hour <= 6.0)):
                if data0.short_wave_radiation[ii] > 100.0 : qcflags[str(shipname) + '_swr'][ii] = 8
    
    
        
    #__________________________________________________________________________________________
        
        if intrvl == 10 : actual_data = len(timeaxiss) * 6 
        if intrvl == 60 : actual_data = len(timeaxiss) * 1
        if intrvl == 30 : actual_data = len(timeaxiss) * 2
        for var in qc_varname:
            keyy = str(str(shipname) + '_' + var)
            ll = len(qcflags[keyy])
            numer = [ii for ii in range(ll) if qcflags[keyy][ii]  == 8]
            bad_data = len(numer); available_data = ll; qw = rr;  
            ff.writelines(keyy + '  : actual_data : ' + str(actual_data) + \
                          ', available_data : ' + str(available_data) + ', bad_data :'\
                          + str(bad_data) + ', Missing_data : ' + str(missing))
            ff.write('\n')
        
        ff.write('\n \n \n')

ff.close(); print('have written qc percentages');

with open(inpath2 + "qcflags_values_t.csv", "w") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(qcflags.keys())
    writer.writerows(itertools.zip_longest(*qcflags.values()))


print('have written qcflags');

#%%   
