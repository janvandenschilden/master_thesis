#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 14:39:47 2020

@author: jan
"""

import os
import pandas as pd
from tqdm.auto import tqdm

def extractFastas(idSeqDir,outputDir,uniprot2UnirefDir, uniref2UniprotDir):
    def generateMapper(mapFile):
        mapper=dict()
        with open(mapFile) as f:
            f.readline()
            for line in f.readlines():
                To, From =line.strip().split("\t")
                mapper[To]=From
        return mapper
    def combineMappers(mapper1,mapper2):
        """
        Keys of mapper1 will be linked to values mapper2
        """
        mapperCombined=dict()
        for key1,key2 in mapper1.items():
            value=mapper2[key2]
            mapperCombined[key1]=value
        return mapperCombined
    def writeFastas(idSeqFile,mapper):
        def writeRow(row):
            proteinId=row["Entry"]
            originalId=mapper[proteinId]
            sequence=row["Sequence"]
            outputFile="{}/{}.fasta".format(outputDir,originalId)
            with open(outputFile,"a") as f:
                firstLine=">{}\n".format(proteinId)
                f.write(firstLine)
                secondLine="{}\n".format(sequence)
                f.write(secondLine)
        idSeqDf=pd.read_csv(idSeqFile, sep="\t")
        for i, row in idSeqDf.iterrows():
            writeRow(row)
            
    for idSeq in tqdm([d for d in os.listdir(idSeqDir) \
                       if d!=".ipynb_checkpoints" and d.endswith(".tab")]):
        idSeqFile="{}/{}".format(idSeqDir,idSeq)
        uniprot2UnirefFile="{}/{}".format(uniprot2UnirefDir,idSeq.replace("_","_uniprot2Uniref_"))
        uniref2UniprotFile="{}/{}".format(uniref2UniprotDir,idSeq.replace("_","_uniref2Uniprot_"))
        
        mapperProtein2Uniref = generateMapper(uniref2UniprotFile)
        mapperUniref2Original = generateMapper(uniprot2UnirefFile)
        mapper=combineMappers(mapperProtein2Uniref,mapperUniref2Original)
                    
        writeFastas(idSeqFile,mapper)