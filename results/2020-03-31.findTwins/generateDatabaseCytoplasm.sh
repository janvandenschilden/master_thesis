#!/bin/bash

# Define relevant Paths
LOCALDIR=$(dirname $(realpath $0))
CytoplasmFastaDir="${LOCALDIR}/../2020-03-31.signalPeptideBestSeperation/cytoplasm"
OUTPUTDIR="${LOCALDIR}/cytoplasmDatabase"
SCRIPT=${LOCALDIR}/generateDatabase.sh

# Loop through fasta files and generate database
for FASTA in ${CytoplasmFastaDir}/*
do
    BASENAME=$(basename ${FASTA/.fasta/})
    OUTPUT=${OUTPUTDIR}/${BASENAME}
    ${SCRIPT} ${FASTA} ${OUTPUT}
done
