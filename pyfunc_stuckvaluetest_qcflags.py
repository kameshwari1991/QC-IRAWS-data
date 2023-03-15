#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 19:11:33 2021

@author: kameshwari
"""
def  pyfunc_stuckvaluetest_qcflags(var,rpnum):
    
    bad = []
    rp = 0
    ss=0
    for ii in range(len(var)-1):
        print(ii)
        diff = var[ii+1]-var[ii]
        if diff == 0.0:
            rp = rp + 1
        elif (diff != 0) & (rp >= rpnum-1):
            bad.append([*range(ii-rp,ii+1)])
            rp = 0
        else:
            rp = 0
        
    if (ii == len(var)-2) & (rp >= rpnum-1):
        bad.append([*range(ii-rp,ii+1)])
        
    return bad
#    return bad
    

# %%
    
#bad = pyfunc_stuckvaluetest_qcflags(var,rpnum)
    
# for ii in range(1040,len(var)-1):
#     print(ii)
# print('after loop')
# print(ii)    
        