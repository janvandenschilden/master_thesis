#!/bin/bash

FASTA=${1}      # Fasta from which to create the database
OUTPUT=${2}     # Path of outputh

makeblastdb -in ${FASTA} -dbtype 'prot' -out ${OUTPUT}
