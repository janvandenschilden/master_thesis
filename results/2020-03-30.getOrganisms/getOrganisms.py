#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:32:12 2020

@author: jan
"""
# Import libraries
import requests
import os
from time import sleep
import pandas as pd

#------------------------------------------------------------------------------
#   Section with help functions
#------------------------------------------------------------------------------
def download(url, fileName):
    for i in range(10):
        try:
            # Delete existing files with filename
            try:
                os.remove(fileName) 
            except:
                pass
            
            """ Use requests to download file. 
            Works with streams to be able large files without having the need of a 
            large memory.
            """
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(fileName, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        if chunk:
                            f.write(chunk)
            return fileName
        except:
            print("Download", url,"failed:",i)
            sleep(5)
            
def uniprotRetrieve(fileName, query="",format="list",columns="",include="no",compress="no",limit=0,offset=0):
    """Downloads file from uniprot for given parameters
    
    If no parameters are given the function will download a list of all the 
    proteins ID's. More information about how the URL should be constructed can
    be found on: 
    https://www.uniprot.org/help/api%5Fqueries
    
    Parameters
    ----------
    fileName : str
        name for the downloaded file
    query : str (Default='')
        query that would be searched if as you used the webinterface on 
        https://www.uniprot.org/. If no query is provided, all protein entries
        are selected. 
    format : str (Default='list')
        File format you want to retrieve from uniprot. Available format are:
        html | tab | xls | fasta | gff | txt | xml | rdf | list | rss
    columns : str (Default='')
        Column information you want to know for each entry in the query 
        when format tab or xls is selected.
    include : str (Default='no')
        Include isoform sequences when the format parameter is set to fasta.
        Include description of referenced data when the format parameter is set to rdf.
        This parameter is ignored for all other values of the format parameter.
    compress : str (Default='no')
        download file in gzipped compression format.
    limit : int (Default=0)
        Limit the amount of results that is given. 0 means you download all.
    offset : int (Default=0)
        When you limit the amount of results, offset determines where to start.
        
    Returns
    -------
    fileName : str
        Name of the downloaeded file.
    """
    def generateURL(baseURL, query="",format="list",columns="",include="no",compress="no",limit="0",offset="0"):
        """Generate URL with given parameters"""
        def glueParameters(**kwargs):
            gluedParameters = ""
            for parameter, value in kwargs.items():
                gluedParameters+=parameter + "=" + str(value) + "&"
            return gluedParameters.replace(" ","+")[:-1] #Last "&" is removed, spacec replaced by "+"
        return baseURL + glueParameters(query=query,
                                        format=format,
                                        columns=columns,
                                        include=include,
                                        compress=compress,
                                        limit=limit,
                                        offset=offset)
    URL = generateURL("https://www.uniprot.org/uniprot/?",
               query=query,
               format=format,
               columns=columns,
               include=include,
               compress=compress,
               limit=limit,
               offset=offset)
    return download(URL, fileName)


#------------------------------------------------------------------------------
#   Main Code
#
#   1. Download tab seperated file with 1 column, the organism
#   2. extract unique organisms and id's
#    3. Write results to file
#------------------------------------------------------------------------------
# Download organisms of all proteins in gammaproteobacteria 
#QUERY="taxonomy:gammaproteobacteria"
QUERY='taxonomy:gammaproteobacteria'
FORMAT="tab"
COLUMNS="organism,lineage(SPECIES),lineage(GENUS)"
FILENAME="gammaproteobacteriaOrganisms.tab"
FILENAME = uniprotRetrieve(FILENAME,query=QUERY,format=FORMAT,columns=COLUMNS)

'''
# Genearate a unique list of organisms
proteins = pd.read_csv(FILENAME,sep="\t")
uniqueOrganisms = proteins["Organism"].unique()
organisms = pd.DataFrame(uniqueOrganisms,columns=["Organism"])
organisms.to_csv("organisms.tab",sep="\t")

# remove big file of all the proteins
os.remove(FILENAME)
'''