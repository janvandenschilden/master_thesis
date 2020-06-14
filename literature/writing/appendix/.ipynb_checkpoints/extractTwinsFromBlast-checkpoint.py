import os
import pandas as pd
from tqdm.auto import tqdm

def getTwins(inputBlastDir,outputListDir):
    def parse(x):
        try:
            return x.split("|")[1]
        except:
            return x
        
    def blast2Twin(inputBlast,outputList):
        BlastResults = pd.read_csv(inputBlast, sep="\t",header=None)
        Twins = pd.DataFrame()
        Twins["cytoplasm"]=BlastResults[0].apply(parse)
        Twins["periplasm"]=BlastResults[1].apply(parse)
        Twins.to_csv(outputList, sep="\t", index=None)
    for inputBlast in tqdm([d for d in os.listdir(inputBlastDir) if d!=".ipynb_checkpoints"]):
        try:
            inputBlastPath = "{0}/{1}".format(inputBlastDir,inputBlast)
            outputPath="{0}/{1}".format(outputListDir,inputBlast.replace(".blast",".tab"))
            blast2Twin(inputBlastPath,outputPath)
        except:
            pass