#!/usr/bin/env python
# coding: utf-8

import urllib.parse
import urllib.request
from time import sleep
import os

def mapping(queryFile,outputFile, parameterDictionary):
    def addQuery():
        with open(queryFile) as f:
            parameterDictionary["query"]="".join(f.readlines())
    def main():
        addQuery()
        url = 'https://www.uniprot.org/uploadlists/'
        data = urllib.parse.urlencode(parameterDictionary)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as f:
           response = f.read()
        with open(outputFile, 'b+w') as f:
            f.write(response)
    for i in range(10):
        main()
        try:
            if os.stat(outputFile).st_size != 0:
                break
        except:
            print("Try",i,"Failed")
            sleep(5*(i+1))