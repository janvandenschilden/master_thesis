# Generate dataset from UniprotKb ppiA/ppiB text search

This pipeline starts from a uniprot text search for ppiA and ppiB proteins.
In subsequent steps these proteins are filtered. 
We want homologues to ppiA and ppiB of E. coli.

## Retrieve ppiA / ppiB
### explanation
We want to retrieve a list of proteins with the gene name ppiA/ppiB
of organismsin the same class as E. coli (gammaproteobacteria).
In addiation we only select ppiA proteins WITH signal peptide 
and ppiB proteins WITHOUT signal peptide.

### procedure
1. Look for following search terms on Uniprot.

"""
ppiA

gene:ppia annotation:(type:signal) taxonomy:gammaproteobacteria
"""

"""
ppiB

gene:ppib NOT annotation:(type:signal) taxonomy:gammaproteobacteria
"""

2. Download "Tab-separated", "Fasta" and "List" Files

### INPUT FILES
none

### OUTPUT FILES
ppiA.list
ppiA.fasta
ppiA.tab

ppiB.list
ppiB.fasta
ppiB.tab

## MSA with clustalOmega
### explanation
To know how much the retrieved sequences differ with each other,
a MSA is run with ClustalOmega which also gives the pim (protein identity matrix).

### procedure
https://www.ebi.ac.uk/Tools/msa/clustalo/

1. Run clustalOmega and choose FASTA output. input ppiA.fasta/ppiB.fasta
2. Download aligment and pim matrix

### INPUT FILES
ppiA.fasta
ppiB.fasta

###
ppiA_alignment.fasta
ppiA_alignment.pim
ppiB_alignment.fasta
ppiB_alignment.pim

## Check SI distributions
### Explanation
We want to know how pairwise sequence identities 
are distributed for ppiA- and ppiB homologues.
A custom script is written that counts this.

### Procedure
"""
for pim in ppiA_alignment.pim ppiB_alignment.pim 
do 
	echo "# Summary of ${pim}" > ${pim/.pim/_pim-summary.txt} 
	for i in " " 1 2 3 4 5 6 7 8 9 
	do 
		echo "${i}0%: "$(grep "${i}[0-9].[0-9][0-9]" ${pim} | wc -l) >> ${pim/.pim/_pim-summary.txt} 
	done 
done
"""

### INPUT FILES
ppiA_alignment.pim
ppiB_alignment.pim

### OUTPUT FILES
ppiA_alignment_pim-summary.txt
ppiB_alignment_pim-summary.txt


## select organims with both ppiA and ppiB
### Explanation
We want to examine ppiA and ppiB in organisms that have  both ppiA and ppiB.
Therefore the "tab seperated" FILES are used to search for organism that
have both ppiA and ppiB.

### Procedure
Python was used with the pandas library.
ppiA.tab and ppiB.tab files were read as Dataframes and merged on organisms.
I noticed that Organisms could have multiple ppiA and ppiB proteins.
Therefore I combined the ppiA and ppiB proteins into the same list per organism.
I also wrote two files with the final ppiA and ppiB protein sets.

### INPUT FILES
ppiA.tab
ppiB.tab

### OUTPUT FILES
organisms_ppiA_ppiB.tab
ppiA_final.list
ppiB_final.list


## Get Fasta sequences for final ppiA/ppiB sets
### Explanation
We now have two lists of the final sets of ppiA and ppiB proteins.
We want also to know the associated sequences.

### Procedure
https://www.uniprot.org/uploadlists/
ppiA_final.list and ppiB_final.list are used as input with for the uniprot Rertrieve/ID mapping.
Fasta is downloaded.

### INPUT FILES
ppiA_final.list
ppiB_final.list

### OUTPUT FILES
ppiA_final.fasta
ppiB_final.fasta


## Remove redundancy from dataset 
### Explanation
In the current ppiA_final.fasta and ppiB_final.fasta,
some sequences will be more similar to each other than others.
Because i do not want to bias towards very similar sequences observed very often,
I will cluster those together and choose a representative.

### Procedure
For this CDHIT is used with default parameters. 
Sequences with more than 90 percent sequence identity
are clustered together.
For each cluster one sequence will represent the others.

### INPUT FILES 
ppiA_final.fasta
ppiB_final.fasta

### OUTPUT FILES
ppiA_final_CDHIT90.clstr
ppiA_final_CDHIT90.fasta
ppiB_final_CDHIT90.clstr
ppiB_final_CDHIT90.fasta


## Generate MSA of sequence representatives of clusters
### Explanation
With a MSA, we can see which residue of one sequence corresponds with one of 
the other sequences.

### Procedure 
clustalomega with default parameters was used to produce the MSA.

### INPUT FILES
ppiA_final_CDHIT90.fasta
ppiB_final_CDHIT90.fasta

### OUTPUT FILES
ppiA_final_CDHIT90_MSA.fasta
ppiB_final_CDHIT90_MSA.fasta
