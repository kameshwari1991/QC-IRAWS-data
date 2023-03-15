#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 10:39:31 2021

@author: kameshwari
"""
import math as math

def pyfunc_latlondistance(lat1,lon1,lat2,lon2) :

    R = 6373.0
    # radius of the Earth
    
    
    lat1 = math.radians(lat1)
    # coordinates
    
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    dlon = lon2 - lon1
    # change in coordinates
    
    dlat = lat2 - lat1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    # Haversine formula
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance