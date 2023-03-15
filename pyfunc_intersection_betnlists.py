#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 12:36:55 2021

@author: kameshwari
"""
def pyfunc_intersection_betnlists(list1, list2):
    list1 = list(list1); list2 = list(list2)
    list3 = [value for value in list1 if value in list2]
    return list3


# [val for val in xx if val in yy]