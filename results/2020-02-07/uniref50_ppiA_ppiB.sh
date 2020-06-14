#!/bin/bash
#======================================================================================
#
#          FILE: uniref50_ppiA_ppiB.sh
#
#         USAGE: uniref50_ppiA_ppiB.sh
#
#   DESCRIPTION: Download the uniref50 members for ppiA and ppiB of E. coli
#
#       OPTIONS: See function 'usage' below (not yet implemented)
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Ir. Jan Van den Schilden (jan.vandenschilden@gmail.com)
#       COMPANY: ---
#       VERSION: 1.0
#       CREATED: 2020.02.07
#      REVISION: ---
#     COPYRIGHT: ---
#       LICENCE: ---
#
#======================================================================================



#--------------------------------------------------------------------------------------
#   Test Functions
#--------------------------------------------------------------------------------------
testSpacer(){
    #==================================================================================
    #           NAME: testSpacer
    #    DESCRIPTION: Provide a Spacer of full width window
    #    PARAMETER 1: Symbol to be repeated in the spacer
    #==================================================================================
    n=`tput col`
    SPACERSYMBOL=$1
    SPACER=$(printf "%0.s${SPACERSYMBOL}" $(seq 1 $n))
    echo ${SPACER}
}

testHeader(){
    #==================================================================================
    #           NAME: testHeader
    #    DESCRIPTION: Provide a header of TEST function
    #    PARAMETER 1: Title of TEST function
    #==================================================================================
    testSpacer "="
    TITLE=$1
    echo "  TEST: ${TITLE}"
    testSpacer "-"
}

testFooter(){
    #==================================================================================
    #           NAME: testFooter
    #    DESCRIPTION: Provide a Footer for the TEST function
    #==================================================================================
    testSpacer "="
    echo ""
    echo ""
}

testPaths(){
    #==================================================================================
    #           name: testPaths
    #    description: prints all the different paths on the screens
    #==================================================================================
    testHeader "paths"
    for var in SCRIPTPATH SCRIPTDIR PROJECTHOME PROJECTSOFTWARE getUniref
    do
        echo "${var}: ${!var}"
    done
    testFooter
}


#--------------------------------------------------------------------------------------
#   Provide paths to the necessary files and software
#--------------------------------------------------------------------------------------
SCRIPTPATH=$(realpath $0)
SCRIPTDIR=$(dirname $SCRIPTPATH)
PROJECTHOME=$(realpath ${SCRIPTDIR}/../../)
PROJECTSOFTWARE=$(realpath ${PROJECTHOME}/software)
getUniref=$(realpath ${PROJECTSOFTWARE}/getUniref.sh)
#testPaths


#--------------------------------------------------------------------------------------
#   Download ppiA and ppiB
#--------------------------------------------------------------------------------------
ppiA="P0AFL3"
ppiB="P23869"
for VAR in ppiA ppiB
do
    ${getUniref} -a ${!VAR} -O "uniref50_${VAR}.csv"
done

