#!/bin/bash

## ppiA
firefox -new-window "https://www.uniprot.org/uniprot/P0AFL3"
firefox "https://www.uniprot.org/uniprot/?query=cluster:(uniprot:P0AFL3*%20identity:0.5)%20not%20id:P0AFL3"
firefox "https://www.uniprot.org/uniprot/?query=cluster%3A%28uniprot%3Ap0afl3*+identity%3A0.5%29+annotation%3A%28type%3Asignal%29&sort=score"

## ppiB
firefox "https://www.uniprot.org/uniprot/P23869"
firefox "https://www.uniprot.org/uniprot/?query=cluster:(uniprot:P23869*%20identity:0.5)"
firefox "https://www.uniprot.org/uniprot/?query=cluster%3A%28uniprot%3Ap23869*+identity%3A0.5%29+NOT+annotation%3A%28type%3Asignal%29&sort=score"

## webservers
firefox "http://weizhong-lab.ucsd.edu/cdhit-web-server/cgi-bin/index.cgi?cmd=cd-hit"
firefox "https://www.ebi.ac.uk/Tools/msa/clustalo/"
firefox "https://toolkit.tuebingen.mpg.de/tools/hhblits"
firefox "https://www.uniprot.org/uploadlists/"
