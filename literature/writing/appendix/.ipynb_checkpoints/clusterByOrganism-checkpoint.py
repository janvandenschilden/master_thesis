import pandas as pd
from tqdm.auto import tqdm

def generateFastas(cytoplasmicProteinsFile, cytoplasmicFastaDir,
                   periplasmicProteinsFile, periplasmicFastaDir): 
    def commonOrganisms(proteins1,proteins2):
        organism1=set(proteins1["Organism"].unique())
        organism2=set(proteins2["Organism"].unique())
        common=sorted(list(organism1&organism2))
        return common
    def genFasta(proteins, directory):
        def newFileName():
            baseNameRaw = proteins["Organism"].unique()[0]
            baseName=baseNameRaw\
            .replace("/","")\
            .replace("(","")\
            .replace(")","")\
            .replace(" ","_")\
            +".fasta"
            fileName="{0}/{1}".format(directory,baseName)
            return fileName
        def generateEntry(row):
            entry=str(row["Entry"])
            ec=str(row["EC number"])
            line=">|{0}|{1}\n".format(entry,ec)
            return line
        def generateSequence(row):
            sequence=str(row["Sequence"])
            n=80
            sequenceSplitted = \
            [sequence[i:i+n] for i in range(0, len(sequence), n)]            
            line="\n".join(sequenceSplitted)+"\n"
            return line
        file = newFileName()
        with open(file,"w") as f:
            for i, row in proteins.iterrows():
                entryLine=generateEntry(row)
                f.write(entryLine)                
                sequenceLine=generateSequence(row)
                f.write(sequenceLine)

            
    # Read tab files
    cytoplasmicProteins = pd.read_csv(cytoplasmicProteinsFile, sep="\t")
    periplasmicProteins = pd.read_csv(periplasmicProteinsFile, sep="\t")
    
    # Extract common organisms
    common = commonOrganisms(cytoplasmicProteins,periplasmicProteins)
    
    # Loop through organims
    for organism in tqdm(common):
        cytoplasmProteinsOrganism = \
        cytoplasmicProteins[cytoplasmicProteins["Organism"]==organism]
        genFasta(cytoplasmProteinsOrganism, cytoplasmicFastaDir)
        
        periplasmicProteinsOrganism= \
        periplasmicProteins[periplasmicProteins["Organism"]==organism]
        genFasta(periplasmicProteinsOrganism, periplasmicFastaDir)
    