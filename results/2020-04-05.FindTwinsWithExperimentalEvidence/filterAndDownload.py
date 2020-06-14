#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 12:45:56 2020

@author: jan
"""

import os
from uniprotRetrieve import uniprotRetrieve
from tqdm.auto import tqdm

def filterAndDownload(mapInputDir, outputFastaDir,
                      queryCytoplasm="NOT annotation:(type:signal)", 
                      queryPeriplasm="annotation:(type:signal)"):
    def retrieveYourList(mapInputFile):
        with open(mapInputFile) as f:
            LINE = f.read().strip()
        yourlist=LINE.split("\t")[1].split("\n")[0]
        return yourlist
    for mapResults in tqdm([d for d in os.listdir(mapInputDir) \
                       if d!=".ipynb_checkpoints" and d.endswith(".tab")]):
        mapResultsFile="{0}/{1}".format(mapInputDir,mapResults)
        yourlist=retrieveYourList(mapResultsFile)
        
        output="{}/{}".format(outputFastaDir,
                mapResults.replace("uniref2Uniprot_",""))
        format="tab"
        columns="id,sequence"
        if mapResults.endswith("cytoplasm.tab"):
            queryFinal="{} {} {}".format(yourlist,"active:yes",queryCytoplasm)
        elif mapResults.endswith("periplasm.tab"):
            queryFinal="{} {} {}".format(yourlist,"active:yes",queryPeriplasm)
        else:
            print("Not cytoplasmic or periplasmic protein")
            queryFinal="{} {}".format(yourlist,"active:yes")
        uniprotRetrieve(output, format=format, query=queryFinal, columns=columns)
        
