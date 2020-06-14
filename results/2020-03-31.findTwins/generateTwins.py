#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import argparse

def generateTwins(input,output):
    def parse(x):
        try:
            return x.split("|")[1]
        except:
            return x
        
    BlastResults = pd.read_csv(input, sep="\t",header=None)
    
    Twins = pd.DataFrame()
    Twins["cytoplasm"]=BlastResults[0].apply(parse)
    Twins["periplasm"]=BlastResults[1].apply(parse)
    
    Twins.to_csv(output, sep="\t", index=None)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    
    INPUT=args.input
    OUTPUT=args.output
    
    generateTwins(INPUT,OUTPUT)