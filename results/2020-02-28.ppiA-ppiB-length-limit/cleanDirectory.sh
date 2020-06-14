#!/bin/bash

LOCALDIR=$(realpath $(dirname $0))

rm ${LOCALDIR}/*.fasta
rm ${LOCALDIR}/*.clstr
rm ${LOCALDIR}/*.list
rm ${LOCALDIR}/*.tab
rm ${LOCALDIR}/*.log
rm ${LOCALDIR}/*.pim
rm -rf __pycache__
