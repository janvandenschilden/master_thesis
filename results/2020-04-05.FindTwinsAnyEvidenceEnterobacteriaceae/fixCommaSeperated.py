#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 18:37:29 2020

@author: jan
"""

import pandas as pd

def fixCommaSeperated(file):
    def extractCols():
        with open(file) as f:
            col1,col2 = f.readline().strip().split("\t")
        return col1, col2
    col1,col2 = extractCols()
    df = pd.read_csv(file, sep="\t")
    newDf = pd.DataFrame(df[col2].str.split(",").tolist(),index=df[col1]).stack()
    newDf = newDf.reset_index([0, col1])
    newDf.columns = [col1, col2]  
    newDf.to_csv(file, sep="\t", index=None)