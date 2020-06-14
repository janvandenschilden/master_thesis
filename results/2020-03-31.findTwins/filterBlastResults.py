#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import argparse

def filterBlastResults(file,**filters):
    columns= ["cytoplasm", 
          "periplasm", 
          "identity", 
          "alignmentLength", 
          "mismatches", 
          "gapOpens", 
          "cytoplasm.start", 
          "cytoplasm.end", 
          "periplasm.start", 
          "periplasm.end", 
          "evalue", 
          "bit score"]
    blastResults = pd.read_csv(file, sep="\t", names=columns)
    temp=blastResults
    for filter, value in filters.items():
        min=value[0]
        max=value[1]
        temp=temp[(temp[filter]>min) & (temp[filter]<max)]
    newResults=temp
    return newResults

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--identityMin", default=25.0)
    parser.add_argument("--identityMax", default=100.0)
    parser.add_argument("--evalueMin", default=0.0)
    parser.add_argument("--evalueMax", default=1e-10)
    args = parser.parse_args()
    
    INPUT=args.input
    OUTPUT=args.output
    identityMin=float(args.identityMin)
    identityMax=float(args.identityMax)
    evalueMin=float(args.evalueMin)
    evalueMax=float(args.evalueMax)

    newResults = filterBlastResults(INPUT,
                                   identity=(identityMin,identityMax),
                                   evalue=(evalueMin,evalueMax))
    newResults.to_csv(OUTPUT,
                      sep="\t", 
                      index=None, 
                      header=None)