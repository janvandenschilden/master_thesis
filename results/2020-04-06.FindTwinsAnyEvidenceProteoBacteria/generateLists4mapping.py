#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 10:42:37 2020

@author: jan
"""

import os
import pandas as pd
from tqdm.auto import tqdm

def generateLists4mapping(twinDir,outputListDir,maxLength=2):
    def readTwins(path):
        twinsDf = pd.read_csv(path, sep="\t")
        return twinsDf
    def writeTwins(twinsDf):
        def getNumber():
            path, dirs, files = next(os.walk(outputListDir))
            numberOfFiles=len(files)
            return int(numberOfFiles/2)
        n = getNumber()
        # Write cytoplasm proteins to file
        cytoplasmProteins = twinsDf["cytoplasm"]
        outputPathCytoplasm = "{0}/{1}_toMap2Uniref_cytoplasm.list".format(outputListDir,n)
        cytoplasmProteins.to_csv(outputPathCytoplasm,
                                 sep="\t",
                                 index=None, 
                                 header=False)
        
        # Write Periplasm proteins to file
        periplasmProteins = twinsDf["periplasm"]
        outputPathPeriplasm = "{0}/{1}_toMap2Uniref_periplasm.list".format(outputListDir,n)
        periplasmProteins.to_csv(outputPathPeriplasm, 
                                 sep="\t", 
                                 index=None,
                                 header=False)
        
    def AddOrWriteTwins(twinsConcatted, twinsToConcat):
        if len(twinsConcatted)+len(twinsToConcat)<=maxLength:
            return twinsConcatted.append(twinsToConcat, ignore_index=True)
        else:
            writeTwins(twinsConcatted)
            return twinsToConcat
        
    twinsToWrite=pd.DataFrame(columns=["cytoplasm","periplasm"])
    for twins in tqdm([d for d in os.listdir(twinDir) \
                       if d!=".ipynb_checkpoints"]):
        twinsPath="{0}/{1}".format(twinDir,twins)
        twinsDf = readTwins(twinsPath)
        twinsToWrite=AddOrWriteTwins(twinsToWrite,twinsDf)
    writeTwins(twinsToWrite)
    
        