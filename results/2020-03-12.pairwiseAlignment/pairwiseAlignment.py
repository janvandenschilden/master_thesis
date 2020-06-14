#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 18:19:24 2020

@author: jan
"""
#------------------------------------------------------------------------------
#   Import different modules
#------------------------------------------------------------------------------
from Bio import pairwise2    # For pairwise sequence alignment
from Bio import SeqIO        # For parsing fasta files
from tqdm import tqdm


#------------------------------------------------------------------------------
#   Declare different variabels (will be replaced by command line args)
#------------------------------------------------------------------------------
pathProteinsSP = "./E_coli_K_12_proteins_SP.fasta"
pathProteinsNoSP = "./E_coli_K_12_proteins_NO_SP.fasta"


#------------------------------------------------------------------------------
#   parseFasta files
#------------------------------------------------------------------------------
proteinsSP = list(SeqIO.parse(pathProteinsSP, "fasta"))
proteinsNoSP = list(SeqIO.parse(pathProteinsNoSP, "fasta"))

print(len(proteinsNoSP))
print(len(proteinsSP))


#------------------------------------------------------------------------------
#   Do pairwise sequence alignment between all proteins with and without signal
#   peptide
#------------------------------------------------------------------------------
i=0
for protNoSP in tqdm(proteinsNoSP):
    for protSP in proteinsSP:    
        idProtSP = protSP.id
        seqProtSP = protSP.seq
        idProtNoSP = protNoSP.id
        seqProtNoSP = protNoSP.seq
        alignment[0] = pairwise2.align.globalxx(seqProtSP,seqProtNoSP)
        i+=1
print(i)    


#------------------------------------------------------------------------------
#   Test Code
#------------------------------------------------------------------------------
#for protein in proteinsSP:
#    print(protein.id)