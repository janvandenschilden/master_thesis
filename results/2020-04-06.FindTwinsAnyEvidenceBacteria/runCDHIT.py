#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 15:33:37 2020

@author: jan
"""

import os
from tqdm.auto import tqdm

def runCDHIT(inputFastaDir,outputCdhitDir, identity=0.9):
    def CDHIT(inputFasta,outputFasta):
        cmd="cd-hit -i {0} -o {1} -c {2}".format(inputFasta,outputFasta,identity)
        os.system(cmd)
    for fasta in tqdm([d for d in os.listdir(inputFastaDir) \
                       if d!=".ipynb_checkpoints"]):
        fastaFile = "{}/{}".format(inputFastaDir,fasta)
        outputFile = "{}/{}".format(outputCdhitDir,fasta)
        CDHIT(fastaFile,outputFile)