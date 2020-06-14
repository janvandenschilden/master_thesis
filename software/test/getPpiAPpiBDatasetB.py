#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#   Import Libraries
#------------------------------------------------------------------------------
import shutil
import sys
sys.path.insert(0, '../')

from uniprotRetrieve import uniprotRetrieve
from intersectProteinSets import intersectProteinSets
from cdhit import cdhit
from clustalOmega import clustalOmega


#------------------------------------------------------------------------------
#   Use Uniprot to get ppiA and ppiB proteins in tab format that agree with
#   the following characteristics
#   ppiA:
#       in gene name: ppiA
#       no signal peptide
#       of taxonomic group: gammaproteobacteria
#   ppiB:
#       in gene name: ppiB
#       signal peptide
#       of taxonomic group: gammaproteobacteria         
#------------------------------------------------------------------------------
print("1. Downloading by query from uniprot")
ppiA = uniprotRetrieve(query="gene:ppia annotation:(type:signal) taxonomy:gammaproteobacteria length:[175 TO 205]",
                form = "tab",
                columns = "id,organism",
                output="ppiA.tab")
ppiB = uniprotRetrieve(query="gene:ppib taxonomy:gammaproteobacteria NOT annotation:(type:signal) length:[149 TO 179]",
                form = "tab",
                columns = "id,organism",
                output="ppiB.tab")


#------------------------------------------------------------------------------
#   Intersect protein sets ppiA.tab
#   
#   Only keep those proteins where ppiA and ppiB occur in the same organism
#------------------------------------------------------------------------------
print("2. Make intersection")
generatedFiles = intersectProteinSets(ppiA, ppiB)
ppiAMerged=generatedFiles[1]
ppiBMerged=generatedFiles[2]


#------------------------------------------------------------------------------
#   Get fasta file for ppiA_merged.list and ppiB_merged.list
#------------------------------------------------------------------------------
print("3. Get fasta file from uniprot")
ppiAMergedFasta = uniprotRetrieve(proteinList=ppiAMerged,
                                  form="fasta",
                                  output="ppiA_merged.fasta")
ppiBMergedFasta = uniprotRetrieve(proteinList=ppiBMerged,
                                  form="fasta",
                                  output="ppiB_merged.fasta")


#------------------------------------------------------------------------------
#   Run CDHIT0.90 on fasta files to reduce bias towards overrepresented seqs
#------------------------------------------------------------------------------
print("4. CDHIT90")
ppiACdhitFasta, ppiACdhitClstr = cdhit(ppiAMergedFasta,cutoff="0.9")
ppiBCdhitFasta, ppiBCdhitClstr = cdhit(ppiBMergedFasta,cutoff="0.9")


#------------------------------------------------------------------------------
#   Generate Multiple Sequence Alignment for ppiA and ppiB
#------------------------------------------------------------------------------
print("5. CLustalOmega")
ppiAFinalFasta, ppiAFinalPim = clustalOmega(ppiACdhitFasta)
ppiBFinalFasta, ppiBFinalPim = clustalOmega(ppiBCdhitFasta)


#------------------------------------------------------------------------------
#   Try to remove generated __pycache__
#------------------------------------------------------------------------------
try:
    shutil.rmtree("./__pycache__")
except:
    pass
