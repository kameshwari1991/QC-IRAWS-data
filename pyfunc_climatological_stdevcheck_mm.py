#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:05:13 2021

@author: kameshwari
"""

import netCDF4 as nc
import numpy as np
from pyfunc_latlondistance import pyfunc_latlondistance
from pyfunc_intersection_betnlists import pyfunc_intersection_betnlists
from cdo import Cdo
import pandas as pd

inpath1 = '/home/kameshwari/Documents/py_scripts/'
# cdo = Cdo()
def pyfunc_climatological_stdevcheck_mm(inpathclim,variablelist,data):
   
    ncfile = 'icoads_global_slp_mean_mm.nc'
    clim = nc.Dataset(inpathclim + ncfile)
    climlat = clim.variables['lat'][:]
    climlon = clim.variables['lon'][:]
    time = clim.variables['time']
    climtime = nc.num2date(time[:],time.units)
    ntimes = np.shape(climtime)[0] # num of timesteps in the climatology dataset
    [longrid,latgrid] = np.meshgrid(climlon,climlat)
    ngrids = np.shape(longrid)[0]*np.shape(longrid)[1] # totag num of grid points in the climatology dataset
    climlatlon = np.array(np.reshape(latgrid,(ngrids,1),'F'))
    climlatlon = np.append(climlatlon, np.reshape(longrid,(ngrids,1),'F'),axis = 1)
    
    indtime_clim = []; indlatlon_clim = []
    for ii in range(len(data.year4)) :
        print(ii)
        indtime_clim.append([jj for jj in range(ntimes) if climtime[jj].month == data.month4[ii]])
        temp_lat_ind_clim = np.logical_and(climlatlon[:,0] > data.lat4[ii]-1.5, climlatlon[:,0] < data.lat4[ii]+1.5)
        temp_lon_ind_clim = np.logical_and(climlatlon[:,1] > data.lon4[ii]-1.5, climlatlon[:,1] < data.lon4[ii]+1.5)
        indlatlon_clim.append(pyfunc_intersection_betnlists(np.where(temp_lat_ind_clim)[0], np.where(temp_lon_ind_clim)[0]))

    qcf = pd.DataFrame(columns = variablelist,index=range(len(data.index)))
    for varname in variablelist :  
        print('starting stdev check:',varname)
        if (varname == 'sea_level_pressure') | (varname == 'air_pressure') | (varname == 'pressure') | (varname == 'airp4_hPa') | (varname == 'slp'): var = 'slp'
        if (varname == 'dry_bulb_temperature') | (varname == 'air_temperature') | (varname == 'dbt') | (varname == 'dbt4_degC') : var = 'air'
        if (varname == 'relative_humidity') | (varname == 'humidity') | (varname == 'rhum'): var = 'rhum'
        if (varname == 'specific_humidity') | (varname == 'shum4_kgperkg') : var = 'shum'
        if (varname == 'uwnd4_mpers') | (varname == 'uwnd'): var = 'uwnd'
        if (varname == 'vwnd4_mpers') | (varname == 'vwnd'): var = 'vwnd'
        if (varname == 'sea_surface_temperature') | (varname == 'water_temperature') | (varname == 'sst4_degC') | (varname == 'sst'): var = 'sst'
        if (varname == 'cloudiness') | (varname == 'cloud_amount') | (varname == 'cloud_okta') | (varname == 'cla4_okta') : var = 'cldc'
        # if (varname == 'short_wave_radiation') | (varname == 'short_wave') : var = 'slp'
    
        print('variable being checked is : ',var)
        meanfile = 'icoads_global_' + var + '_mean_mm.nc'
        stdevfile = 'icoads_global_' + var + '_stddev_mm.nc'
    
        clim1 = nc.Dataset(inpathclim + meanfile)
        clim2 = nc.Dataset(inpathclim + stdevfile)
        climstdev = clim2.variables[var][:];
        climmean = clim1.variables[var][:];
        climmean1 = np.reshape(climmean,(ntimes,ngrids,1),'F')
        climstdev1 = np.reshape(climstdev,(ntimes,ngrids,1),'F')

        for ii in range(len(data.index)) :
           # print(ii)
            if len(indlatlon_clim[ii]) > 0 :
                mean = np.nanmean([climmean1[indtime_clim[ii],value] if climmean1[indtime_clim[ii],value].mask == False else np.nan for value in indlatlon_clim[ii]])
                stdev = np.nanmean([climstdev1[indtime_clim[ii],value] if climstdev1[indtime_clim[ii],value].mask == False else np.nan for value in indlatlon_clim[ii]])
                if (np.isnan(mean) | np.isnan(stdev)) :
                    qcf.eval(varname)[ii] = 4
                elif (data.eval(varname)[ii] - mean >= -5.0*stdev) & (data.eval(varname)[ii] - mean <= 5.0*stdev) : 
                    qcf.eval(varname)[ii] = 1
                else : 
                    qcf.eval(varname)[ii] = 8
        del(var)
    return qcf










    # if region == 'asiansector' :
    #     lat1 = -80.0; lon1 = -15.0; lat2 = 80; lon2 = +180.0
    #     cdo.sellonlatbox(lon1,lon2,lat1,lat2,input = inpathclim + meanfile,output = 'temp1.nc')
    #     clim1 = nc.Dataset('temp1.nc')
    #     cdo.sellonlatbox(lon1,lon2,lat1,lat2,input = inpathclim + stdevfile,output = 'temp1.nc')
    #     clim2 = nc.Dataset('temp1.nc')
    # elif region = tio






