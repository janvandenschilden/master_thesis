#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import 
import shutil
import os
import datetime

# define general functions
def makeDir(name):
    try:
        shutil.rmtree(name)
    except:
        pass
    os.makedirs(name)
    return name

def makeBackup(name):
    moment=str(datetime.datetime.now()).replace(":",".")
    backup=name+".bu."+moment
    try:
        shutil.copytree(name,backup)
    except:
        pass
    return backup


# # 1 Download periplasmic and cytoplasmic proteins

# First we have to download all the periplasmic and cytoplasmic proteins from Uniprot that potentially have a twin.

# In[2]:


print("1 Download periplasmic and cytoplasmic proteins")

# Import
from uniprotRetrieve import uniprotRetrieve

# Make dir for results
DIR1=makeDir("1.downloadProteins")

# Download proteins Cytoplasm
# Enterobacteriaceae
# Enterobacterales
# Gammaproteobacteria
# Proteobacteria
# Bacteria
QUERY="taxonomy:Enterobacteriaceae (locations:(location:cytoplasm) OR locations:(location:cytosol)) NOT annotation:(type:signal)"
FORMAT="tab"
COLUMNS="id,organism,ec,sequence"
FILENAME="proteinsCytoplasmic.tab"
OUTPUT="{0}/{1}" .format(DIR1,FILENAME)
uniprotRetrieve(OUTPUT, format=FORMAT, query=QUERY, columns=COLUMNS)

# Download proteins Periplasm
QUERY="taxonomy:Enterobacteriaceae locations:(location:periplasm) annotation:(type:signal)"
FORMAT="tab"
COLUMNS="id,organism,ec,sequence"
FILENAME="proteinsPeriplasmic.tab"
OUTPUT="{0}/{1}" .format(DIR1,FILENAME)
uniprotRetrieve(OUTPUT, format=FORMAT, query=QUERY, columns=COLUMNS)

# Make backup
BACKUP=makeBackup(DIR1)


# # 2 Extract common organisms and generate FASTA's

# We want to check for structural Twins (one in the periplasm and one in the cytoplasm) in the same organism.
# Therefore the script will look at all the avaible proteins and check for which organisms there are both cytoplasmic and periplasmic proteins available.
# Only for those, fasta files are generated.

# In[3]:


print("2 Extract common organisms and generate FASTA's")

# Import
import generateFastas

# Generate dirs for resuts
CYTODIR=makeDir("2.exctractCommonOrganismCytoplasm")
PERIDIR=makeDir("2.exctractCommonOrganismPeriplasm")

# Read in Tab files
CYTOPLASM_PROTEINS_FILE="1.downloadProteins/proteinsCytoplasmic.tab"
PERIPLASM_PROTEINS_FILE="1.downloadProteins/proteinsPeriplasmic.tab"

# Generate Fasta files
generateFastas.generateFastas(CYTOPLASM_PROTEINS_FILE, CYTODIR,
                              PERIPLASM_PROTEINS_FILE, PERIDIR)

#make backup
CYTODIR_BACKUP=makeBackup(CYTODIR)
PERIDIR_BACKUP=makeBackup(PERIDIR)


# # 3 Use Blast to search for Twins

# In[ ]:


print("3 Use Blast to search for Twins")


# ## 3.1 Generate Databases

# Blast searches for sequences against a database.
# Therefore, A script will turn the fasta files of periplasm proteins into databases.

# In[4]:


print("3.1 Generate Databases")

# import
import generateDatabases

# Generate dir for resuts
DIR_PERIPLASM_DATABASE=makeDir("3.1.periplasmDatabase")

# Make databases
generateDatabases.generateDatabases(PERIDIR, DIR_PERIPLASM_DATABASE)

#make backup
DIR_PERIPLASM_DATABASE_BACKUP=makeBackup(DIR_PERIPLASM_DATABASE)


# ## 3.2 Run Blast to find twins

# In[5]:


print("3.2 Run Blast to find twins")

# import
import runBlast

# make dir for results
DIR_BLAST_RESULTS=makeDir("3.2.blastResults")

# runBlast
EVALUE=1e-8
runBlast.runBlast(CYTODIR,DIR_PERIPLASM_DATABASE,DIR_BLAST_RESULTS,evalue=EVALUE)

# make backup
DIR_BLAST_RESULTS_BACKUP=makeBackup(DIR_BLAST_RESULTS)


# ## 3.3 Extract Twins from Blast Results

# In[6]:


print("3.3 Extract Twins from Blast Results")

# import
import imp
import getTwins
imp.reload(getTwins)

# make dir for results
DIR_TWINS=makeDir("3.3.twins")

# getTwins
getTwins.getTwins(DIR_BLAST_RESULTS, DIR_TWINS)

# make backup
DIR_TWINS_BACKUP=makeBackup(DIR_TWINS)


# # 4 Generate MSA (fast way)

# In[ ]:


print("4 Generate MSA (fast way)")


# ## 4.1 Generate lists

# Make sure to provide a maximum of entries per list as the mapping system can not handle lists that are to large.

# In[7]:


print("4.1 Generate lists")

# import
import generateLists4mapping

# make dir for results
DIR_LISTS=makeDir("4.1.listsToMap")

# generate lists to map
MAX_ID_PER_FILE=1e3
generateLists4mapping.generateLists4mapping(DIR_TWINS,DIR_LISTS,maxLength=MAX_ID_PER_FILE)

# make backup
DIR_LISTS_BACKUP=makeBackup(DIR_LISTS)


# ## 4.2 Map proteins to UniRef groups

# To generate a MSA in a very fast way, we try to avoid BLAST.
# Therefore we use the predefined Uniref groups.
# This will result in a less extensive MSA, but it can be run for a lot of proteins.

# In[32]:


print("4.2 Map proteins to UniRef groups")

# import
import mapUniprot2Uniref

# make dir for results
DIR_MAP_UNIPROT_2_UNIREF=makeDir("4.2.mapUniprot2Uniref")

# Mapping
mapUniprot2Uniref.mapUniprot2Uniref(DIR_LISTS, DIR_MAP_UNIPROT_2_UNIREF)

# make backup
DIR_MAP_UNIPROT_2_UNIREF_BACKUP=makeBackup(DIR_MAP_UNIPROT_2_UNIREF)


# ## 4.3 Map Uniref groups back to the proteins they contain

# In[33]:


print("4.3 Map Uniref groups back to the proteins they contain")

# import 
import mapUniref2Uniprot
import imp
imp.reload(mapUniref2Uniprot)

# make dir for resutls
DIR_MAP_UNIREF_2_UNIPROT=makeDir("4.3.mapUniRef2UniProt")

# Mapping
mapUniref2Uniprot.mapUniref2Uniprot(DIR_MAP_UNIPROT_2_UNIREF,DIR_MAP_UNIREF_2_UNIPROT)

# make backup
DIR_MAP_UNIREF_2_UNIPROT_BACKUP=makeBackup(DIR_MAP_UNIREF_2_UNIPROT)


# ## 4.4 Filter proteins and download as tab with sequence in it

# We want to make sure there is evidence that periplasmic protein homologues occur in the periplasm and cytoplasmic in the cytoplasm.
# To achieve this, another uniprot retrieve search is performed using the yourlist:ID

# In[34]:


print("4.4 Filter proteins and download as tab with sequence in it")

# import 
import filterAndDownload

# make dir for resutls
DIR_FILTERED=makeDir("4.4.filteredFiles")

# Filter and download
func = filterAndDownload.filterAndDownload
func(DIR_MAP_UNIREF_2_UNIPROT, DIR_FILTERED)

# make backup
DIR_FILTERED_BACKUP=makeBackup(DIR_FILTERED)


# ## 4.5 Extract fasta files 

# In[35]:


print("4.5 Extract fasta files ")

# import
import extractFastas
import imp
imp.reload(extractFastas)

# make dir for results
DIR_FASTAS=makeDir("4.5.fastas")

# extract fastas from tab
fun=extractFastas.extractFastas
fun(DIR_FILTERED,DIR_FASTAS,DIR_MAP_UNIPROT_2_UNIREF, DIR_MAP_UNIREF_2_UNIPROT)

# make backup
DIR_FASTAS_BACKUP=makeBackup(DIR_FASTAS)


# ## 4.6 CDHIT

# In[36]:


print("4.6 CDHIT")

# import
import runCDHIT

# make dir for results
DIR_CDHIT=makeDir("4.6.CDHIT")

# Run CDHIT
func=runCDHIT.runCDHIT
IDENTITY=0.90
func(DIR_FASTAS,DIR_CDHIT,identity=IDENTITY)

# make Backup
DIR_CDHIT_BACKUP = makeBackup(DIR_CDHIT)


# ## 4.7 ClustalOmega

# In[37]:


print("4.7 ClustalOmegau")

# import
import runClustalOmega
import imp
imp.reload(runClustalOmega)

# make dir
DIR_CLUSTALO=makeDir("4.7.clustalOmega")

# Run
func=runClustalOmega.runClustalOmega
func(DIR_CDHIT,DIR_CLUSTALO)

# make Backup
DIR_CLUSTALO_BACKUP = makeBackup(DIR_CLUSTALO)


# In[ ]:




