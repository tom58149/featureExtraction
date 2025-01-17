#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 2020
Author Thomas

Simple script to print out all files that have been detected as malware.
"""
import pandas as pd

col_names = ['Search Term', 'Requested', 'Response', 'Scan Date', 'Detections', 'Total', 'Permalink', 'AVs', 'CVEs']
data = pd.read_csv('/', sep=';') #Location to csv with virus total results.

df = data[data['Detections'] != 0]

print(df['Search Term'])
