#!/usr/bin/env python
# coding: utf-8

import urllib.parse
import urllib.request

url = 'https://www.uniprot.org/uploadlists/'

params = {
'from': 'NF50',
'to': 'ACC',
'format': 'tab',
'columns':"id",
}
with open("doubleMapping2.list") as f:
    params["query"]=" ".join(f.readlines())

params["query"]+=" database:(type:pdb)"


data = urllib.parse.urlencode(params)
data = data.encode('utf-8')
req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as f:
   response = f.read()
with open('doubleMappingResults.tab', 'b+w') as f:
    f.write(response)
