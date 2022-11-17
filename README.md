# featureExtraction
This is a set of files for static Malware analysis with Python machine learning Libraries.


Data preparation steps:


Checkfiletype
This file has two uses. First to traversing folders and sub-folders and extracting only files and as  the displayed extension can not be trusted, due to it being malware, the header signature is therefore read to confirm the type.

staticFeatureExtraction
Program will take a collection of verified malware and benign files to extract static features using the pefile Python library. The results will be written to a CSV file.
This program will also traversing folders and sub-folders but will not check files signature.

Model Training & Evaluation:


selectionGraphs
This is the training of the machine learning model with the program taking a csv of static features and training on a few algorithms with pre-set depths (these are all configurable to the data). The out put will compare the algorithms to determin which has the least FP

rocCurve
This program will train a model and then evaulate the false postive rate and display as a graph.
Currenlty set to evaluate ExtraTreesClassifier but this can be changed to depending on algorithm.

Other:


VirusTotalSorter
Simply prints out all files with 1 or more VT detections. 
