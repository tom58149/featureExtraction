#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
from shutil import move

"""
Program checks file's header is a MZ dos file type

@author: tom
"""

path = "/home/laptop/Downloads/collectionOfMalware"
dest = "/home/laptop/Downloads/peFiles"
exe_files = []

file_list_malware = []
for folder, subfolder, files in os.walk(path):
    for f in files:
        full_path = os.path.join(folder, f)
        file_list_malware.append(full_path)
            
for file in file_list_malware:
    #output = magic.from_file(file)
    with open(file) as fd:
        file_head = fd.read(2)
        if file_head == "MZ":
            print(file)
            exe_files.append(file)
            
try:
    for file in exe_files:
        move(file, dest)
except Exception as e:
    print(e)
            
  
   