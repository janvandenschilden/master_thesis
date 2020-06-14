# Introduction
*getPpiAPpiBDataset.py* combines python scripts that automate the process to generate a dataset.

# Download set of proteins from Uniprot using a query and API
Set of proteins is downloaded in tab format.
At least the "Organism" and "entry" column needs to be present.
## ppiA
For ppiA, we want to make sure that a signal peptide is present.
Furthermore, it is also checked whether ppiA is present in the gene name.
Finally, We want the proteins to be similar to ppiA from E. coli.
Therefore, we limit the result to those entries that are from the taxonomic group: **gammaproteobacteria**.

"""
query: "gene:ppia annotation:(type:signal) taxonomy:gammaproteobacteria"
"""

## ppiB
Very similar to ppiA, except that we want to make sure there is no signal peptide present.

"""
query: "gene:ppib taxonomy:gammaproteobacteria NOT annotation:(type:signal)"
"""

# Filter for proteins where ppiA and ppiB occur in the same organism
We want a list of organisms in which both ppiA and ppiB occur at the same time.
To solve this, a custom python script using pandas was written that groups the entries by "Organism".
Only entries with both ppiA and ppiB are kept.

# get Fasta of ppiA and ppiB
For these reduced lists of ppiA and ppiB proteins, we want a fasta file.
A python script that automates web browsing.
This script uploads the protein list to uniprot and get a group ID back.
In a next step, this group ID can be used in a query as was done in the first step.
The fasta is downloaded. 

# Reduce redundancy with CDHIT0.90
We don't want to bias overrepresented sequences.
Therefore the fasta files of ppiA and ppiB are uploaded to a CDHIT webserver.
The .clstr files and reduced fasta files were subsequently downloaded.

# Generate MSA
Finally, We want to generate a Multiple Sequence Alignment for the ppiA and ppiB set.
The fasta files of previous step were uploaded to the ClustalOmega server and alignment was downloaded as fasta and pim.
