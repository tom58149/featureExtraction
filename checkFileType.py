#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
from shutil import move

"""
Checks file's header signature to confirm it is a MZ dos file type
@author: Thomas
"""

path = "/"  #Downloaded Malware location
dest = "/"  #Destination of PE files only
exe_files = [] #Will hold verfied exe

#Get all individual files from a given directory by traversing though all folders to read files. 
#The full file path is then added to array.
#TODO break up nested loop.
file_list_malware = []
for folder, subfolder, files in os.walk(path):
    for f in files:
        full_path = os.path.join(folder, f)
        file_list_malware.append(full_path)
            
#Checks the files singature for the true file type.
#If the signature is MZ (.EXE) add to array. 
for file in file_list_malware:
    #output = magic.from_file(file)
    with open(file) as fd:
        file_head = fd.read(2)
        if file_head == "MZ":
            print(file)
            exe_files.append(file)
            
#Move all verfied PE files to final dest
try:
    for file in exe_files:
        move(file, dest)
except Exception as e:
    print(e)
            
  
   
