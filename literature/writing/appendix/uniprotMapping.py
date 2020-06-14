import urllib.parse
import urllib.request
import os

def uniprotMapping(fileName, query, From="ACC",To="ACC",Format="fasta",Columns="",outputDir=""):
    """ Implementation of UniProtKB mapping REST API
    
    
    PARAMETERS
    ----------
    fileName : str
        Name of file where the output of the mapping is stored to
    query : str
        list of identifiers (depending on database) separated by spaces or new lines
    From : str
        Database to map from, the ones the query use
    To : str
        Database to map to
    Format : str
        Format of the downloaded file
    Columns : str
        Columns to show in the file (if format is tab or xls)
    OutputDir : str
        Directory where to store the file (Default is current directory)
        
    RETURNS
    -------
    fileName : str
        file name where output is stored
    
    """
    
    for i in range(10):
        try:
            url = 'https://www.uniprot.org/uploadlists/'
            params={
                "query":query,
                "from":From,
                "to":To,
                "format":Format,
                "columns":Columns,
            }
            data = urllib.parse.urlencode(params)
            data = data.encode('utf-8')
            req = urllib.request.Request(url, data)
            with urllib.request.urlopen(req) as f:
                response = str(f.read(),encoding="utf-8")
            outputPath="{}{}".format(outputDir,fileName)
            if outputDir and not os.path.exists(outputDir):
                os.makedirs(outputDir)
            with open(outputPath,"w") as f:
                f.write(response)
            return fileName
        except:
            print("request failed, wait for", i*5,"seconds and try again")
            time.sleep(i*5)