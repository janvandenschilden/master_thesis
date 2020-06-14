#!/usr/bin/env python
# coding: utf-8

# In[2]:


from b2bTools.singleSeq.EFoldMine.Predictor import EFoldMine

def readFasta(file):
    f=open(file)
    fastaDic=dict()
    for line in f:
        if line.startswith(">"):
            Id=line.strip().replace(">","")
            fastaDic[Id]=""
        else:
            fastaDic[Id]+=line.strip()
    return fastaDic

def getPredictions(msaDic):
    efoldMineInput = [(Id,seq.replace("-","")) for Id,seq in msaDic.items()]
    efm = EFoldMine()
    efm.predictSeqs(efoldMineInput)
    return efm.allPredictions

def mapPredictions(msaDic,predictionDic):
    Ids = msaDic.keys()
    mappedPredictions=dict()
    for Id in Ids:
        mappedPredictions[Id]=dict()
        seq=msaDic[Id]
        seqLength=len(seq)
        mappedPredictions[Id]["sequence"]=seq
        for predictionKey,predictionSequence in predictionDic[Id].items():
            mappedPredictions[Id][predictionKey]=list()
            posInPrediction=0
            for msaRes in seq:
                if msaRes=="-":
                    mappedPredictions[Id][predictionKey].append("-")
                else:
                    predictionResidue=predictionSequence[posInPrediction][0]
                    predictionValue=predictionSequence[posInPrediction][1]
                    if msaRes==predictionResidue:
                        mappedPredictions[Id][predictionKey].append(predictionValue)
                        posInPrediction+=1
                    else:
                        print("something went wrong")
    return mappedPredictions

def mappedPredictions2File(mappedPredictions, fileName):
    f = open(fileName,"w")
    for Id in mappedPredictions.keys():
        f.write(">{}\n".format(Id))
        for feature, sequence in mappedPredictions[Id].items():
            sequenceList=map(str,list(sequence))
            sequenceString=" ".join(sequenceList)
            f.write("{}\t{}\n".format(feature,sequenceString))
    f.close()

if __name__ == "__main__":
    MSA_FILE="msa.fasta"
    MSA_DIC=readFasta(MSA_FILE)
    MSA_PREDICTIONS= getPredictions(MSA_DIC)
    MSA_MAPPED_PREDICTIONS=mapPredictions(MSA_DIC,MSA_PREDICTIONS)
    mappedPredictions2File(MSA_MAPPED_PREDICTIONS,"mapped_msa.pred")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




