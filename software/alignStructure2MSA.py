#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 14:54:58 2020

@author: jan
"""
#------------------------------------------------------------------------------
#   Import Libraries
#------------------------------------------------------------------------------
import argparse

#------------------------------------------------------------------------------
#   functions
#------------------------------------------------------------------------------
def parsePrediction(predictionFile):
    """Parses predictonFile
    
    Parameters
    ----------
    predictionFile : str
        Path to prediction file
        
    Returns
    -------
    predictions : dictionary
        dictionary where each key is an identifier and each value a couple.
        First value of the couple is the Sequence in string.
        Second value is a list of prediction values.
    """
    predictions = dict()
    with open(predictionFile) as f:
        newIdIdentifier="* for "
        for line in f:
            if line.startswith(newIdIdentifier):
                """
                When a line starts with the newIdIdentifier, the name on that
                line is used as key for the dictionary.
                """
                ID=line.replace(newIdIdentifier,"").split(" ")[0]
                predictions[ID]=["",list()]
            elif line.startswith("*"):
                """
                Other lines starting with "*" are ignored
                """
                pass
            elif not line.strip():
                """
                Empty lines are ignored
                """
                pass
            else:
                """
                In other cases, the line should contain an amino acid and its
                predicted value. Amino acid is added to sequence string. 
                Prediction value added to prediction list.
                """
                aminoAcid = line[0]
                predictionValue = float(line[1:])
                predictions[ID][0]+=aminoAcid               # Append to seq
                predictions[ID][1].append(predictionValue)  # add Value list
    return predictions

def parseFasta(fastaFile):
    """Parses fasta file
    
    Parameters
    ----------
    fastaFile : str
        Path to fasta file
        
    Returns
    -------
    sequences : dict
        Dictionary where keys are the IDs and values the sequences
    """
    sequences =dict()
    with open(fastaFile) as f:
        newIdIdentifier=">"
        for line in f:
            if line.startswith(newIdIdentifier):
                """
                When a line starts with the newIdIdentifier, the name on that
                line is used as key for the dictionary. Also, the "|" symbol is
                replaced by "_" symbol.
                """
                ID=line.replace(newIdIdentifier,"").replace("|","_").split(" ")[0]
                sequences[ID]=""
            elif not line.strip():
                """
                Empty lines are ignored
                """
                pass
            else:
                """
                Other cases should contain (part) of the amino acid sequence.
                Add this to the sequence
                """
                sequences[ID]+=line.strip()
    return sequences
            

def generateFilter(seq1,seq2):
    """
    Looks for positions where there is no amino acid present in both positions.
    Sequences (including gaps) have equal length.
    
    Parameters 
    ----------
    seq1 : str
        First sequence
    seq2 : str
        Second sequence
        
    Returns
    -------
    Filter : set
        set of positions that are not allowed because there is a gap in one of
        two sequences.
    """
    Filter = list()
    for i in range(len(seq1)):
        if seq1[i] == "-" or seq2[i] =="-":
            Filter.append(i)
    return set(Filter)
   
def mapSequences(seq1,seq2, filter1=list(), filter2=list()):
    """ Maps relative positions of sequences to each other
    
    Parameters
    ----------
    seq1 : Bio.SeqRecord.SeqRecord
        First sequence
    seq2 : Bio.SeqRecord.SeqRecord
        Second sequence
        
    Returns
    -------
    mapping : list of triples
        list of triples of amino acid and relative positions
    """
    i1 = 0          #Position in seq1
    i2 = 0          #Position in seq2
    mappingTemp = list()
    while i1 < len(seq1) and i2 < len(seq2):
        """
        Amino acids are compared to each other one by one. We essentially
        expect the same sequence two times but with different gabs. Therefore,
        when a gab is observed in a sequence we go to the next position in that
        sequence untill we are for both sequences at a position with an amino
        acid.
        Also, when a given filter forbids 
        These amino acids should be the same and the relative positions are 
        given back.
        """
        if seq1[i1]=="-":
            i1+=1
        elif seq2[i2]=="-":
            i2+=1
        elif seq1[i1] == seq2[i2]:
            mappingTemp.append((i1,i2))
            i1+=1
            i2+=1
        else:
           print("ERROR: Ungapped sequences must be identical")
           return -1
    """
    Only retain those couples where the positions are not in on of the 2 
    filter lists.
    """
    mapping = {i:j for i,j in mappingTemp if i not in filter1 and j not in filter2}
    return mapping

def addProtein(fileName, ID, sequenceMSA, prediction, mapMSA2Str, 
               verbose=False):
    """Format protein and add to file
    
    Parameters
    ----------
    fileName : str
        Path of the file the formatted info will be written to
    ID : str
        ID of the protein sequence
    sequenceMSA : str
        sequence when aligned in the MSA
    prediction : list
        List that contains the sequence and a sublist with predictions for each
        amino acid
    mapStr2MSA : Dict
        Mapping of sequence in structural alignment to sequence in MSA
    """
    seqPred = prediction[0] # Extract sequence from prediction object
    predPred =prediction[1] # Extract prediction from prediction object
    
    #Extract positions that are relevant for the structural alignment
    mapMSA2Pred = mapSequences(sequenceMSA,seqPred)
    positions = set(mapMSA2Pred.keys()) & set(mapMSA2Str.keys()) 
    
    # Combine and format information, write to file
    with open(fileName,"a") as f:
        for posMSA in positions:
            # Map position MSA to position in prediction
            posPred = mapMSA2Pred[posMSA]  
            # Map position MSA to position in structure
            posStr = mapMSA2Str[posMSA]    
            # Extract amino acid from sequence
            aminoAcid = seqPred[posPred]
            # Extract prediction for that amino acid from predicion list
            predValue = predPred[posPred]
            # Write to file
            line = " ".join([str(ID),str(aminoAcid),str(posMSA),str(predValue),str(posStr),"\n"])
            if verbose:
                print(line)
            f.write(line)

def alignStructure2MSA(structureAlignmentFile, 
                       MSA1File, predictions1File, name1, 
                       MSA2File, predictions2File, name2,
                       verbose =False):
    """
    Generate files that are needed as input for Visualisation script of
    Rosan Kuin.
    
    Parameters
    ----------
    structureAlignmentFile : str
        PATH to file that contains the two structurally aligned protein 
        sequences (in FASTA format).
    MSA1File : str
        PATH to file that contains the Multiple Sequence Alignment (MSA) 
        corresponding to the first protein in the structureAlignment file
        (in FASTA format). The first protein of structureAlignment needs to 
        be present with the same ID.
    predictions1File : str
        PATH to file that contains the biophysical predictions for the proteins
        in MSA1.
    name1 : str
        Name of the generated file for the first protein.
    MSA2File : str
        Similar as MSA1 but for second protein in structureAlignment file.
    predictions2File : str
        Similar as prediction1 but for second protein in structureAlignment file.
    name2 : str
        Name of the generated file for the second protein.
    """
    def parseSequences(name,MSA,predictions,mapping):
        """Loop through all proteins in MSA / prediction and parse them
        
        Parameters
        ----------
        name : str
            Name of the file to be written
        MSA : Dict
            key: ID's of the different proteins
            value: aligned sequences
        predicitons : Dict
            key : ID's of the different proteins
            value : [sequence, list of predictions]
        mapping : Dict
            mapping from the MSA to the structurally aligned sequence
        """
        # Write header to file
        with open(name,"w") as f:
            if verbose:
                print("Writing header to file:", name)
            f.write("seq, aa, msa_map, dynamine, struct_map\n")
        """ 
        sets are used to excluse IDs of structurally aligned proteins.
        For those there are no predictions available.
        """
        if verbose:
            print("MSA\n",MSA,"\n\n")
            print("Predictions\n",predictions,"\n\n")
            print("Mapping\n",mapping,"\n\n")
        for ID in set(MSA.keys()) & set(predictions.keys()):
            addProtein(name, ID, MSA[ID], predictions[ID], mapping, 
                       verbose=verbose)
            
    # Extract ID's and sequences of structurally aligned sequences 1 & 2
    strAlign = parseFasta(structureAlignmentFile)
    idStr1, idStr2 =strAlign.keys()
    seqStr1,seqStr2 = strAlign.values()
    
    # Parse MSA's
    MSA1 = parseFasta(MSA1File)
    MSA2 = parseFasta(MSA2File)
    
    # Parse predictions
    predictions1 = parsePrediction(predictions1File)
    predictions2 = parsePrediction(predictions2File)
    
    # Generate mappings from MSA to structures
    Filter = generateFilter(seqStr1,seqStr2)
    mapMSA1Str = mapSequences(MSA1[idStr1], seqStr1, filter2=Filter)
    mapMSA2Str = mapSequences(MSA2[idStr2], seqStr2, filter2=Filter)
    
    # Generate parsed files
    parseSequences(name1,MSA1,predictions1,mapMSA1Str)
    parseSequences(name2,MSA2,predictions2,mapMSA2Str)


#------------------------------------------------------------------------------
#   Code to run when called as a script with arguments
#------------------------------------------------------------------------------
if __name__ == '__main__':
    #--------------------------------------------------------------------------
    #   Definition of the command line arguments
    #--------------------------------------------------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("structureAlignmentFile",
                        help="""
                        File that contains the two structurally aligned 
                        sequences for which to compare the evolutionary data.
                        Provide in Fasta format
                        """)
    parser.add_argument("MSA1File",
                        help="""
                        File that contains the multiple sequence alignment of 
                        the first protein (The first entry in the 
                        structureAlignmentFile). 
                        """)
    parser.add_argument("predictions1File",
                        help="""
                        File that contains biophysical prediction for MSA1.
                        """)
    parser.add_argument("outputName1",
                        help="""
                        Name of the file for the formatted output of protein 1. 
                        """)
    parser.add_argument("MSA2File",
                        help="""
                        File that contains the multiple sequence alignment of 
                        the second protein (The first entry in the 
                        structureAlignmentFile). 
                        """)
    parser.add_argument("predictions2File",
                        help="""
                        File that contains biophysical prediction for MSAs.
                        """)
    parser.add_argument("outputName2",
                        help="""
                        Name of the file for the formatted output of protein s. 
                        """)
    parser.add_argument("-v","--verbose", action="store_true",
                        help="""Verbose output""") 
    args = parser.parse_args()
    
    #--------------------------------------------------------------------------
    #   Main Code
    #--------------------------------------------------------------------------
    alignStructure2MSA(args.structureAlignmentFile,
                       args.MSA1File,
                       args.predictions1File,
                       args.outputName1,
                       args.MSA2File,
                       args.predictions2File,
                       args.outputName2,
                       verbose= args.verbose)