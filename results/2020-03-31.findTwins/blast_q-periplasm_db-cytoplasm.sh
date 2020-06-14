#!/bin/bash

LOCALDIR=$(dirname $(realpath ${0}))
EVALUE="1e-10"
QUERYDIR="${LOCALDIR}/../2020-03-31.signalPeptideBestSeperation/periplasm"
DBDIR=${LOCALDIR}/"cytoplasmDatabase"
OUTPUTDIR="${LOCALDIR}/blast_q-periplasm_db-cytoplasm"
SCRIPT="${LOCALDIR}/runBlast.sh"

mkdir ${OUTPUTDIR}

for QUERY in ${QUERYDIR}/*
do
    BASENAME=$(basename ${QUERY/.fasta/})
    DB="${DBDIR}/${BASENAME/periplasm/cytoplasm}"
    OUTPUT="${OUTPUTDIR}/${BASENAME}.blast"
    
    ${SCRIPT} ${QUERY} ${DB} ${EVALUE} ${OUTPUT}
done
