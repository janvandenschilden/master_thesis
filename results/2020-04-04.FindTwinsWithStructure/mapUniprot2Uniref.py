#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 11:32:41 2020

@author: jan
"""

from mapping import mapping
import os
from tqdm.auto import tqdm

def mapUniprot2Uniref(inputListDir, outputMappingDir):
    params={
        "from":"ACC",
        "to":"NF50",
        "format":"tab",
        "columns":"id"
        }
    for List in tqdm([d for d in os.listdir(inputListDir) if d!=".ipynb_checkpoints"]):
        queryFile="{0}/{1}".format(inputListDir,List)
        baseName=List.replace("toMap2Uniref","uniprot2Uniref").replace(".list",".tab")
        output="{0}/{1}".format(outputMappingDir,baseName)  
        mapping(queryFile,output,params)