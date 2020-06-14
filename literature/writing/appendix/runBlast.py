import os
from tqdm.auto import tqdm

def runBlast(queryDir,databaseDir,outputDir,evalue=1e-10,outfmt=6):
    def blastp(query,database,output,evalue=1e-10,outfmt=6):
        cmd="blastp -query {0} -db {1} -evalue {2} -outfmt {3} > {4}"\
        .format(query, database, evalue, outfmt, output)
        os.system(cmd)
    for query in tqdm(os.listdir(queryDir)):
        try:
            queryPath="{0}/{1}".format(queryDir,query)
            databasePath="{0}/{1}".format(databaseDir,query.replace(".fasta",""))
            outputPath="{0}/{1}".format(outputDir,query.replace(".fasta",".blast"))
            blastp(queryPath,databasePath,outputPath,evalue=evalue,outfmt=outfmt)
            # Remove empty files
            if os.stat(outputPath).st_size == 0:
                os.remove(outputPath)
        except:
            pass