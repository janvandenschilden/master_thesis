#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 12:18:22 2020

@author: jan
"""

import pandas as pd
import os
from mapping import mapping
from tqdm.auto import tqdm

def mapUniref2Uniprot(inputDir,outputDir):
    def mapResults2QueryFile(mapResultsFile):
        mapResults=pd.read_csv(mapResultsFile, 
                               sep="\t")
        query=mapResults["Cluster ID"]
        FileName=mapResultsFile.split("/")[-1]
        List="{0}/{1}".format(outputDir,FileName.replace(".tab",".list"))
        query.to_csv(List, 
                     sep="\t", 
                     index=None,
                     header=False)
        return List
    params={
        "from":"NF50",
        "to":"ACC",
        "format":"tab",
        "columns":"id"
        }
    for mapResults in tqdm([d for d in os.listdir(inputDir) \
                       if d!=".ipynb_checkpoints"]):
        mapResultsFile = "{0}/{1}".format(inputDir,mapResults)
        List=mapResults2QueryFile(mapResultsFile)
        output=List.replace(".list",".tab")\
        .replace("uniprot2Uniref","uniref2Uniprot")
        mapping(List,output,params)