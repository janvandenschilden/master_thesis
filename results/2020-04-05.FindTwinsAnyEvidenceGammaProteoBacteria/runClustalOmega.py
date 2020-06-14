#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 16:06:49 2020

@author: jan
"""

import os
from tqdm.auto import tqdm

def runClustalOmega(inputCdhitDir, outputClustaloDir):
    def clustalo(inputFasta,outputFasta):
        cmd="clustalo -i {} -o {}".format(inputFasta,outputFasta)
        os.system(cmd)
    for cdhit in tqdm([d for d in os.listdir(inputCdhitDir) \
                       if d!=".ipynb_checkpoints" \
                       and d.endswith(".fasta")]):
        cdhitFile="{}/{}".format(inputCdhitDir,cdhit)
        outputMsaFile="{}/{}".format(outputClustaloDir,cdhit.replace(".fasta",".MSA.fasta"))
        clustalo(cdhitFile, outputMsaFile)