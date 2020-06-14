#!/bin/bash

# Define relevant Paths
LOCALDIR=$(dirname $(realpath $0))
FastaDir="${LOCALDIR}/../2020-03-31.signalPeptideBestSeperation/periplasm"
OUTPUTDIR="${LOCALDIR}/periplasmDatabase"
SCRIPT=${LOCALDIR}/generateDatabase.sh

# Loop through fasta files and generate database
for FASTA in ${FastaDir}/*
do
    BASENAME=$(basename ${FASTA/.fasta/})
    OUTPUT=${OUTPUTDIR}/${BASENAME}
    ${SCRIPT} ${FASTA} ${OUTPUT}
done
