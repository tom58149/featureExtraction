#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 23:33:21 2019

@author: laptop
"""
import pandas as pd

col_names = ['Search Term', 'Requested', 'Response', 'Scan Date', 'Detections', 'Total', 'Permalink', 'AVs', 'CVEs']
data = pd.read_csv('/home/laptop/Documents/virustotal-search-20191214-193919.csv', sep=';') #Line will be missed

df = data[data['Detections'] != 0]

print(df['Search Term'])