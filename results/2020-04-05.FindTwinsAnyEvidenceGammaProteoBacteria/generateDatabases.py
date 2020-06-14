#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 17:26:52 2020

@author: jan
"""
import os
from tqdm.auto import tqdm

def generateDatabases(fastaDir,outputDir):
    def generateDatabase(fasta,output):
        cmd = "makeblastdb -in {0} -dbtype 'prot' -out {1}".format(fasta,output)
        os.system(cmd)
    for fasta in tqdm(os.listdir(fastaDir)):
        fastaPath="{0}/{1}".format(fastaDir,fasta)
        output="{0}/{1}".format(outputDir,fasta.replace(".fasta",""))
        generateDatabase(fastaPath,output)