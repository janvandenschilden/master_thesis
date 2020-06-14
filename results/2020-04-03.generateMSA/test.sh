#!/bin/bash

INPUT=./Sample.fasta
OUTPUT1=./SampleCDHIT
OUTPUT2=./SampleMSA.fasta



for i in {1..1000}
do

    rm ${OUTPUT1} ${OUTPUT2}

    ./runCDHIT.sh  ${INPUT} ${OUTPUT1}
    ./runClustalo.sh ${OUTPUT1} ${OUTPUT2}
done
