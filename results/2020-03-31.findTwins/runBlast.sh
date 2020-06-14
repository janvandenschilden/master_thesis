#!/bin/bash

QUERY=${1}
DB=${2}
EVALUE=${3}
OUTPUT=${4}

blastp \
    -query ${QUERY} \
    -db ${DB} \
    -evalue ${EVALUE} \
    -outfmt 6 \
    > ${OUTPUT}
