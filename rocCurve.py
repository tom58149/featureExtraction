#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
@Author: Thomas
Description: Create a visual ROC graph for fp / tp from a trained model (currently set at extra tree)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# roc curve and auc score
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

from sklearn.ensemble import ExtraTreesClassifier



def plot_roc_curve(fpr, tpr, colour, key):
    plt.plot(fpr, tpr, color=colour, label=key)
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.show()

def setRocSettings(data, colour, key):
        
    X = data.iloc[:, :-1] #for whatever reason adding .values makes x object arrays "not supported"
    Y = data.iloc[:, 16].values
    X_train, X_test, y_train, y_test = train_test_split(X, Y ,test_size=0.2)
    
    clf = ExtraTreesClassifier()
    clf = clf.fit(X_train, y_train)
    
    probs = clf.predict_proba(X_test)
    probs = probs[:, 1]
    
    auc = roc_auc_score(y_test, probs)
    print('AUC: %.2f' % auc)
    
    fpr, tpr, thresholds = roc_curve(y_test, probs)
    plot_roc_curve(fpr, tpr, colour, key)
    
        


data = pd.read_csv('.csv') #CSV of extracted features from windows pe files (Malware / Benign)
setRocSettings(data, 'blue', 'Windows')
#data = pd.read_csv('.csv') 
#setRocSettings(data, 'green', 'Other')


