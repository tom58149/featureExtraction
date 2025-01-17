#!/usr/bin/env python2
"""
@Author: Thomas
Description: Program takes a collection of malware and benign PE (Portable executable) files and extracts static features to be used to train a ML model.
"""
import pefile
import os
import hashlib
import array
import math
import sys,os
import csv
#extract resources from given pe file
def pe_resources(pe):
    resources = []
    if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
	try:
            for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                if hasattr(resource_type, 'directory'):
                    for resource_id in resource_type.directory.entries:
                        if hasattr(resource_id, 'directory'):
                            for resource_lang in resource_id.directory.entries:
                                data = pe.get_data(resource_lang.data.struct.OffsetToData, resource_lang.data.struct.Size)
                                size = resource_lang.data.struct.Size
                                resources_entropy = pe_entropy(data)

                                resources.append([resources_entropy, size])
        except Exception as e:
            return resources
            print("error getting directory entry resourcesS") + e
    return resources

#find entroy of section by using the data struture off set and size of the pe
def pe_entropy(data):
    if len(data) == 0:
        return 0.0
    count = array.array('L', [0]*256)
    for x in data:
  	count[x if isinstance(x, int) else ord(x)] += 1
      
    
    entropy = 0
    for x in count:
	if x:
	    p_x = float(x) / len(data)
	    entropy -= p_x*math.log(p_x, 2)

    return entropy

def entropy_iterator(pe, file):
    entropy = []
    try:
        entropy = map(lambda x:x[0], pe.sections)
    except Exception:
        print("EE") + file
        
        
    return entropy

    

    
def write_features(malware_id):
    
    pe = pefile.PE(file)
 
    #Get sha256 //delete once finshed
    fh = open(file, "rb")
    data = fh.read()
    fh.close()
    sha256 = hashlib.sha256(data).hexdigest()
                
    
        #Get import table hash// delete?
        #ihash = pe.get_imphash() 
        #get file warninga // to be counted##
        #warnings = pe.get_warnings()
        
       
       
     
            #get mean entropy for pe    
    entropy = map(lambda x:x.get_entropy(), pe.sections)
    max_entropy = max(entropy)
            
   

        
        # If these are 0 they do not need to be treated as missing values
        #number of imported API call names
    try:
        importedApi = 0
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            for API in entry.imports:
                importedApi +=1
         
                  
            #number od dll inported
        importedDll = 0
        for x in pe.DIRECTORY_ENTRY_IMPORT:
            importedDll += 1
                            
    except AttributeError:
        importedApi = 0
        importedDll = 0
            
     
        #image size
    imageSize = pe.OPTIONAL_HEADER.SizeOfImage
        
            
        #if these values are missing they will be treated as missing using the mean method
            
            #pe virtual sizeentropyyy
    virtual_sizes = map(lambda x:x.Misc_VirtualSize, pe.sections)
    if virtual_sizes > 0:
        virtual_sizes = sum(virtual_sizes)/float(len(virtual_sizes))
    else:
        virtual_sizes = 0
            
                                
                #size of pe data 
    raw_sizes = map(lambda x:x.SizeOfRawData, pe.sections)
    if raw_sizes > 0:
        raw_sizes = sum(raw_sizes)/float(len(raw_sizes))
    else:
        raw_sizes = 0

        
            
    
    
     #resource //to be counted
    resources = pe_resources(pe)
            #resource size
    if len(resources) > 0:
        entropy = map(lambda x:x[0], resources)
        max_resource_entropy = max(entropy)
                
        # max resource size
        sizes = map(lambda x:x[1], resources)
        max_resource_size = max(sizes)
    else:
        max_resource_entropy = 0
        max_resource_size = 0
       
            

        #pe hoptian header entry point
    entry_point = pe.OPTIONAL_HEADER.AddressOfEntryPoint
            

        #  file Characteristics
    chars = pe.FILE_HEADER.Characteristics
        
               
    machine = pe.FILE_HEADER.Machine
    sub_system = pe.OPTIONAL_HEADER.Subsystem
    major_sub_system = pe.OPTIONAL_HEADER.MajorSubsystemVersion
    optinal_head_size = pe.FILE_HEADER.SizeOfOptionalHeader
    sections_len = len(pe.sections)
    char_dll = pe.OPTIONAL_HEADER.DllCharacteristics
    
   
        
        
    #Write hashes to doc
    worksheet.writerow([max_entropy, importedApi, importedDll, imageSize, virtual_sizes, raw_sizes, max_resource_entropy, max_resource_size, entry_point, chars, machine, sub_system, major_sub_system, optinal_head_size, sections_len, char_dll, malware_id])
    
    
    

#ToDo create for loop to run through dir of files instead of one
if __name__ == "__main__":

    
    dir_path_malware = "" # Collection of folder and sub folders of malware files
    dir_path_benign = "" # Collection of folders and sub folders of benign files



    #Create a list of files with full path for malware
    file_list_malware = []
    for folder, subfolder, files in os.walk(dir_path_malware):
        for f in files:
            full_path = os.path.join(folder, f)
            file_list_malware.append(full_path)
            
            
    #Create a list of files with full path for benign
    file_list_benign = []
    for folder, subfolder, files in os.walk(dir_path_benign):
        for f in files:
            full_path = os.path.join(folder, f)
            file_list_benign.append(full_path)
    
    with open('csv for results', 'wb') as csvfile:
	worksheet = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    
        worksheet.writerow(["Max entropy", "API", "DLL","image Size", "virtual_sizes", "raw_sizes", "max_resource_entropy","resource_sizes", "entry_point", "Characteristics", "Machine", "sub system", "major sub system", "optinal header size", "sections length", "DLL Characteristics", "malware?"])
        
        
        
        for file in file_list_malware:
                try:
                    write_features(1)    
                except Exception as e: 
                    print(e)
                    print(file)
                    
        for file in file_list_benign:
                try:
                    write_features(0)    
                except Exception as e: 
                    print(e)
                    print(file)
