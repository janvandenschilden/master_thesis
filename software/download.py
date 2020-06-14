#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import wget
import os

def download(link, name):
    """ Download link and give file specific name
    
    Function will download link and give resulting file given name.
    If already a file exists with this name, it will be deleted.
    
    Parameters
    ----------
    link : str
        Link which has to be downloaded
    name : str
        resulting file name
    """
    print("Download from:",link)
    for i in range(1,11):
        try:
            try:
                os.remove(name)
            except:
                pass
            print("      try ",i)
            wget.download(link,out=name, bar=False)
            break
        except:
            if i>=10:
                raise "Download with wget failed"