#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
#   Import all the libraries
#------------------------------------------------------------------------------
import argparse
from selenium import webdriver

#'''
try:
    from xvfbwrapper import Xvfb      # To hide the browser
except:
    pass
#'''

import os
from time import sleep


#------------------------------------------------------------------------------
#   Functions
#------------------------------------------------------------------------------
def openWebDriver():
    """Opens a webdriever
    
    Returns
    -------
    selenium.webdriver object
        Variable with webdriver object
    """
    return webdriver.Firefox()

def openUniprotMappingURL(webDriver):
    """Given webdriver opens given URL
    
    Parameters
    ----------
    webDriver : selenium.webdriver object
        Given webdriver for specific browser (e.g. Firefox)
    """
    webDriver.get("https://www.uniprot.org/uploadlists/")
    
def uploadList(webDriver, proteinList):
    """Uploads proteinList to https://www.uniprot.org/uploadlists/
    
    Parameters
    ----------
    webDriver : selenium.webdriver object
        Given webdriver for specific browser (e.g. Firefox)
    proteinList : str
        Path of the protein list
    """
    uploadFileField = webDriver.find_element_by_id("uploadfile")
    proteinListPath=os.path.realpath(proteinList)
    uploadFileField.send_keys(proteinListPath)
    
def submit(webDriver):
    """Push submit button
    
    Parameters
    ----------
    webDriver : selenium.webdriver object
        Given webdriver for specific browser (e.g. Firefox)
    """
    try: # Tries to close the banner first (if there is one) 
        webDriver.find_element_by_id("privacy-panel-accept").click()
    except:
        pass
    submitButton = webDriver.find_element_by_id("upload-submit")
    submitButton.click()
        
def waitForPageRefresh(webDriver, oldURL):
    """ Checks whether the page has been refreshed
    
    Parameters
    ----------
    webDriver : selenium.webdriver object
        Given webdriver for specific browser (e.g. Firefox)
    oldURL : str
        the URL that was being used before the refresh
    """
    while webDriver.current_url == oldURL:
        sleep(0.1)

def extractYoulistID(webDriver):
    """Extract yourlist ID from query
    
    Parameters
    ----------
    webDriver : selenium.webdriver object
        Given webdriver for specific browser (e.g. Firefox)
    
    Returns
    -------
    yourlist : str
        yourlist:ID, this value can furhter on be used in queries
    """
    currentURL=webDriver.current_url
    yourlist = currentURL.split("query=")[1].split(r"&sort")[0]
    return yourlist

def closeDriver(webDriver):
    """Closes the webbrowser and driver
    
    Parameters
    ----------
    webDriver : selenium.webdriver object
        Given webdriver for specific browser (e.g. Firefox)
    """
    webDriver.quit()
    
def uniprotGroupId(proteinList):
    """ Gets yourlist:ID for provided protein list
    
    Parameters
    ----------
    proteinList : str
        Path to the protein list
        
    Returns
    -------
    yourlist : str
        yourlist:ID, this value can furhter on be used in queries
    """
    #--------------------------------------------------------------------------
    #   To Hide the Browser
    #--------------------------------------------------------------------------
    try:
        display = Xvfb()
        display.start()
    except:
        pass
    
    #--------------------------------------------------------------------------
    #   Main Code
    #--------------------------------------------------------------------------
    driver= openWebDriver()
    openUniprotMappingURL(driver)
    uploadList(driver,proteinList)
    submit(driver)
    waitForPageRefresh(driver,"https://www.uniprot.org/uploadlists/")
    yourlist = extractYoulistID(driver)
    closeDriver(driver)
    os.remove("geckodriver.log")
    
    #--------------------------------------------------------------------------
    #   Stop Hiding the Browser
    #--------------------------------------------------------------------------
    try:
        display.stop()
    except:
        pass
    
    #--------------------------------------------------------------------------
    #   Return result
    #--------------------------------------------------------------------------
    return yourlist

#------------------------------------------------------------------------------
#   Code to run when called as a script with arguments
#------------------------------------------------------------------------------
if __name__ == '__main__':
    #--------------------------------------------------------------------------
    #   Definition of the command line arguments
    #--------------------------------------------------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("proteinList",
                        help="""Path to file that contains a list of protein 
                        accession numbers""")
    args = parser.parse_args()
    
    #--------------------------------------------------------------------------
    #   Main Code
    #--------------------------------------------------------------------------
    print(uniprotGroupId(args.proteinList))
    