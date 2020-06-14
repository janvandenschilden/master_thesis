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
