#!/bin/bash

LOCALDIR=$(dirname $(realpath ${0}))
EVALUE="1e-10"
QUERYDIR="${LOCALDIR}/../2020-03-31.signalPeptideBestSeperation/cytoplasm"
DBDIR=${LOCALDIR}/"periplasmDatabase"
OUTPUTDIR="${LOCALDIR}/blast_q-cytoplasm_db-periplasm"
SCRIPT="${LOCALDIR}/runBlast.sh"

mkdir ${OUTPUTDIR}

for QUERY in ${QUERYDIR}/*
do
    BASENAME=$(basename ${QUERY/.fasta/})
    DB="${DBDIR}/${BASENAME/cytoplasm/periplasm}"
    OUTPUT="${OUTPUTDIR}/${BASENAME}.blast"
    
    ${SCRIPT} ${QUERY} ${DB} ${EVALUE} ${OUTPUT}
done
