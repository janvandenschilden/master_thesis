#!/bin/bash

INPUT=$1
OUTPUT=$2

clustalo \
    -i ${INPUT} \
    -o ${OUTPUT} \
    --force
