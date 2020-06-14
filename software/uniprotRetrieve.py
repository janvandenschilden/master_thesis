#!/usr/bin/env python
#------------------------------------------------------------------------------
#   Import all the libraries
#------------------------------------------------------------------------------
import argparse
import wget
from uniprotGroupId import uniprotGroupId
import os
from download import download

def addField(URL, parameterPrefix, parameterValue):
    """ Adds new parameter to URL

    Parameters
    ----------
    URL : str
        Partially completed URL (e.g. https://www.uniprot.org/uniprot/?).
    parameterPrefix : str
        Prefix of parameter that has to glued to the URL before the actual
        value (e.g. query).
    parameterValue : str
        Value that is glued to the URL after the parameterPrefix 
        (e.g. id:Q9Y6M0+or+id:Q9Y6M1)

    Returns
    -------
    str
        Glued URL (e.g. https://www.uniprot.org/uniprot/?query=id:Q9Y6M0+or+id:Q9Y6M1i&)
        Only when parameterValue is given. Otherwise return original URL.
    """
    if parameterValue:
        return URL + parameterPrefix+"="+parameterValue+"&"
    else:
        return URL

def addQuery(URL, query, proteinList=""):
    """ Adds query to URL

    Function will add the query to a partially completed URL. The query 
    must be provided form as it would by in the final URL. 

    Parameters
    ----------
    URL : str
        Partially completed URL
    query : str
        Formatted query that will be searched by Uniprot
    proteinList : str
        Path to the protein list

    Returns
    -------
    str
        URL that now contains the query.
    """
    if proteinList:
        if query:
            query=uniprotGroupId(proteinList)+"+"+query
        else:
            query=uniprotGroupId(proteinList)
    # replace spaces by + for url
    query=query.replace(" ","+")
    return addField(URL,"query",query)

def addFormat(URL, form):
    """ Adds format to URL

    Parameters
    ----------
    URL : str
        Partially completed URL.
        (e.g. https://www.uniprot.org/uniprot/?)
    form : str
        Format in which you want to retrieve your results.
        (e.g. list)

    Returns
    -------
    str
        URL that now contains the format.
        (e.g. https://www.uniprot.org/uniprot/?format=list&)
    """
    return addField(URL, "format", form)

def addColumns(URL, columns):
    """ Adds columns to URL

    Parameters
    ----------
    URL : str
        Partially completed URL.
        (e.g. https://www.uniprot.org/uniprot/?)
    columns : str
        Columns you want in "tab" or "xls" downloaded file
        (e.g. "id,protein name")

    Returns
    -------
    str
        URL that now contains the columns.
        (e.g. https://www.uniprot.org/uniprot/?columns=id,protein name&)
    """
    return addField(URL,"columns",columns)

def addInclude(URL, include):
    """ Adds Include to URL

    Parameters
    ----------
    URL : str
        Partially completed URL.
        (e.g. https://www.uniprot.org/uniprot/?)
    include : bool
        True when you want to include isoforms or descriptions, otherwise
        False
        (e.g. False)

    Returns
    -------
    str
        URL that now contains the include field. The value is 'yes' when True,
        'no' when false.
        (e.g. https://www.uniprot.org/uniprot/?include=no&)
    """
    if include:
        return addField(URL,"include","yes")
    else:
        return addField(URL,"include","no")

def addCompress(URL, compress):
    """ Adds compress to URL

    Parameters
    ----------
    URL : str
        Partially completed URL.
        (e.g. https://www.uniprot.org/uniprot/?)
    compress : bool
        True when you want to gzip the file, otherwise False
        (e.g. False)

    Returns
    -------
    str
        URL that now contains the compress field. The value is 'yes' when True,
        'no' when false.
        (e.g. https://www.uniprot.org/uniprot/?include=no&)
    """
    if compress:
        return addField(URL,"compress","yes")
    else:
        return addField(URL,"compress","no")

def addLimit(URL, limit):
    """ Adds limit to URL

    Parameters
    ----------
    URL : str
        Partially completed URL.
        (e.g. https://www.uniprot.org/uniprot/?)
    limit : str
        The maximum amount of items you want in the file.
        (e.g. 5)

    Returns
    -------
    str
        URL that now contains the limit.
        (e.g. https://www.uniprot.org/uniprot/?limit=5&)
    """
    return addField(URL,"limit",str(limit)) # Format limit to string

def addOffset(URL, offset):
    """ Adds offset to URL

    Parameters
    ----------
    URL : str
        Partially completed URL.
        (e.g. https://www.uniprot.org/uniprot/?)
    offset : str
        From which entry you want to start in the resulting file.
        Often combined with limit.
        (e.g. 5)

    Returns
    -------
    str
        URL that now contains the offset.
        (e.g. https://www.uniprot.org/uniprot/?offset=5&)
    """
    return addField(URL,"offset",str(offset)) # Format offset to string

def generateURL(query, form, columns, include, compress, limit, offset, 
                proteinList=""):
    """Generates URL for uniprot with provided input

    Parameters
    ----------
    URL : str
        Partially completed URL.
        (e.g. https://www.uniprot.org/uniprot/?)
    query : str
        Formatted query that will be searched by Uniprot
    form : str
        Format in which you want to retrieve your results.
    columns : str
        Columns you want in "tab" or "xls" downloaded file
    include : bool
        True when you want to include isoforms or descriptions, otherwise
        False
    compress : bool
        True when you want to gzip the file, otherwise False
    limit : str
        The maximum amount of items you want in the file.
    offset : str
        From which entry you want to start in the resulting file.
        Often combined with limit.
    proteinList : str
        Path to the protein list
    
    Returns
    -------
    str
        URL that now contains all the parameters
    """
    URL="https://www.uniprot.org/uniprot/?"
    URL=addQuery(URL,query, proteinList=proteinList)
    URL=addFormat(URL,form)
    URL=addColumns(URL,columns)
    URL=addInclude(URL,include)
    URL=addCompress(URL,compress)
    URL=addLimit(URL,limit)
    URL=addOffset(URL,offset)
    return URL[:-1].replace(" ","+")     # Last "&" is removed from string

def uniprotRetrieve(query="", 
                    form="list", 
                    columns="", 
                    include=False, 
                    compress=False, 
                    limit="0", 
                    offset="0", 
                    output=False, proteinList=""):
    """ Download uniprot data with given parameters

    Given parameters are used to generate URL for uniprot REST API.
    File is downloaded to specified outputName.

    Parameters
    ----------
    URL : str
        Partially completed URL.
        (e.g. https://www.uniprot.org/uniprot/?)
    query : str
        Formatted query that will be searched by Uniprot
    form : str
        Format in which you want to retrieve your results.
    columns : str
        Columns you want in "tab" or "xls" downloaded file
    include : bool
        True when you want to include isoforms or descriptions, otherwise
        False
    compress : bool
        True when you want to gzip the file, otherwise False
    limit : str
        The maximum amount of items you want in the file.
    offset : str
        From which entry you want to start in the resulting file.
        Often combined with limit.
    output: str
        Name of the output file. By default temp.ext
    proteinList : str
        Path to the protein list
        
    Returns
    -------
    str
        Name of generated file
    """
    if output:
        outputName=output
    else:
        outputName="temp."+form
    URL=generateURL(query, form, columns, include, compress, limit, offset, 
                    proteinList=proteinList)
    
    #--------------------------------------------------------------------------
    #   If the filename already exists, it gets removed
    #--------------------------------------------------------------------------
    try:
        os.remove(outputName)
    except:
        pass
    
    download(URL,outputName)
    return outputName

#------------------------------------------------------------------------------
#   Code to run when called as a script with arguments
#------------------------------------------------------------------------------
if __name__ == '__main__':
    #--------------------------------------------------------------------------
    #   Definition of the command line arguments
    #--------------------------------------------------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--proteinList", default="",
                        help="""Path to file that contains a list of protein 
                        accession numbers""")
    parser.add_argument("-q","--query", default="" ,
                        help="""Query uniprot entries have to agree with. 
                        More information about the query syntax is found on 
                        https://www.uniprot.org/help/text-search. 
                        A list of available query fields is found on 
                        https://www.uniprot.org/help/query-fields. It is also 
                        possible to do an advanced search on the uniprot 
                        website and look in the resulting URL how the fields 
                        are represented.""") 
    parser.add_argument("-f","--format", default="tab",
                        help="""Format in which the results are returned. 
                        Possible values are: html | tab | xls | fasta | gff 
                        | txt | xml | rdf | list | rss""") 
    parser.add_argument("-c","--columns", default="",
                        help="""Columns to select for retrieving results in tab
                        or xls format. Full list of column names is found on 
                        https://www.uniprot.org/help/uniprotkb_column_names. 
                        Values should be comma separated 
                        (e.g. 'id,reviewed,protein names').""") 
    parser.add_argument("-i","--include", action="store_true",
                        help="""Include isoform sequences when the format 
                        parameter is set to fasta. Include description of 
                        referenced data when the format parameter is set to 
                        rdf. This parameter is ignored for all other values of 
                        the format parameter. """) 
    parser.add_argument("-C","--compress", action="store_true",
                        help="""Return results gzipped. Note that if the client 
                        supports HTTP compression, results may be compressed 
                        transparently even if this parameter is not set.""") 
    parser.add_argument("-l","--limit",default="0",
                        help="""Maximum number of results to retrieve.""") 
    parser.add_argument("-o","--offset",default="0",
                        help="""Offset of the first result, typically used 
                        together with the limit parameter.""") 
    parser.add_argument("-O","--output",default="",
                        help="""Name of the output file.""") 
    args = parser.parse_args()
    
    #--------------------------------------------------------------------------
    #   Main code
    #--------------------------------------------------------------------------
    uniprotRetrieve(args.query,args.format,args.columns, args.include, 
                    args.compress, args.limit, args.offset, 
                    output=args.output, proteinList=args.proteinList)
