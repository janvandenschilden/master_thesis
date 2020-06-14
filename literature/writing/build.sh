#!/bin/bash

LOCAL=$(realpath $(dirname $0))
LITERATURE_STUDY=${LOCAL}/thesis.tex

cd ${LOCAL}

cat ${LOCAL}/../papers/*.bib > ${LOCAL}/sources.bib
pdflatex ${LITERATURE_STUDY}
biber ${LITERATURE_STUDY/.tex/}
pdflatex ${LITERATURE_STUDY}
