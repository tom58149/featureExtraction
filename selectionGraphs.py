#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Thomas
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
from multiprocessing import Pool
##Algorithms
from sklearn.ensemble import ExtraTreesClassifier
import sklearn.ensemble as ske
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.svm import SVR
from sklearn.feature_selection import RFE
from sklearn.datasets import make_friedman1
from sklearn.linear_model import LassoCV


data = pd.read_csv('.csv') #CSV of extracted features.

X = data.iloc[:, :-1] #for whatever reason adding .values makes x object arrays "not supported"
Y = data.iloc[:, 16].values




def recursiveFeatureElimination():
    estimator = SVR(kernel="linear")
    selector = RFE(estimator, 5, step=1)
    selector = selector.fit(X, Y)
    

    selector.ranking_


def selectKBest(X,Y):
    clf = SelectKBest(score_func=chi2, k=8)    
    clf = clf.fit(X,Y)   
    featureScores = np.array(clf.scores_)
    #Graph
    graph = pd.Series(featureScores, index=X.columns)
    graph.nlargest(10).plot(kind='barh')
    return clf.transform(X)
    

##Extra tree classifier to show feature importance, with select from model
def extraTreeFeatureImportance(X, Y):
    clf = ExtraTreesClassifier()
    clf = clf.fit(X, Y)
    importance = np.array(clf.feature_importances_)
    
    feat_importances = pd.Series(importance, index=X.columns)
    feat_importances.nlargest(10).plot(kind='barh')
    model = SelectFromModel(clf, prefit=True)
    return model.transform(X)
    
##Extra tree classifier to show feature importance with variability
def extraTreeWithVariability(X, Y):
    clf = ExtraTreesClassifier(n_estimators=30, random_state=0)
    clf = clf.fit(X, Y)
    importances = clf.feature_importances_
    
    
    std = np.std([tree.feature_importances_ for tree in clf.estimators_],
             axis=0)
    indices = np.argsort(importances)[::-1]
        
        
    for f in range(X.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
    
    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.barh(range(X.shape[1]), importances[indices],
           color="r", xerr=std[indices], align="center")
    plt.yticks(range(X.shape[1]), X.columns)
    plt.ylim([-1, X.shape[1]])
    plt.show()


def lassoSelectFromGraph(X,Y):
    clf = LassoCV()
    sfm = SelectFromModel(clf, threshold=0.25)
    sfm.fit(X, Y)
    n_features = sfm.transform(X).shape[::-1]
    
    while n_features > 2:
        sfm.threshold += 0.1
        X_transform = sfm.transform(X)
        n_features = X_transform.shape[::-1]
        
    # Plot the selected two features from X.
    plt.title(
        "Features selected from Boston using SelectFromModel with "
        "threshold %0.3f." % sfm.threshold)
    feature1 = X_transform[:, 0]
    feature2 = X_transform[:, 1]
    plt.plot(feature1, feature2, 'r.')
    plt.xlabel("Feature number 1")
    plt.ylabel("Feature number 2")
    plt.ylim([np.min(feature2), np.max(feature2)])
    plt.show()


##Heatmap showing the correction of all features to all others
def heatMap(X,Y):
    corrmat = data.corr()
    top_corr_features = corrmat.index
    sns.heatmap(data[top_corr_features].corr(),annot=True,cmap="RdYlGn")
    
    
    
##Call methods
p = Pool(5)
print(p.map(recursiveFeatureElimination()))
X_new = selectKBest(X,Y)
X_new = extraTreeFeatureImportance(X,Y)


X_train, X_test, y_train, y_test = train_test_split(X_new, Y ,test_size=0.2)


#Algorithm comparison
algorithms = {
        "DecisionTree": tree.DecisionTreeClassifier(max_depth=10, random_state=0),
        "RandomForest": ske.RandomForestClassifier(n_estimators=30, random_state=50),
        "GradientBoosting": ske.GradientBoostingClassifier(n_estimators=50, random_state=0),
        "AdaBoost": ske.AdaBoostClassifier(n_estimators=100,random_state=0),
        "GNB": GaussianNB()
    }

results = {}
print("\nNow testing algorithms")
for algo in algorithms:
    clf = algorithms[algo]
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    print("%s : %f %%" % (algo, score*100))
    results[algo] = score

winner = max(results, key=results.get)
print('\nWinner algorithm is %s with a %f %% success' % (winner, results[winner]*100))


