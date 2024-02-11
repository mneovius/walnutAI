# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 12:51:13 2024

@author: Neovius
"""

from pathlib import Path
from pdf_analysis.loader import TextExtractor
from camelot_interface.table_resolver import TableResolver
from global_helper_functions.helper_functions import HelperFunctions

if __name__ == "__main__":
    
    ### uri for pdf to load
    ### if being in a queue, doint this in a for loop loading one pdf after the other
    data_uri: str = "C:/Users/Neovius/OneDrive/Desktop/Työhakemuksia/TheWalnutAI/keppel-corporation-limited-annual-report-2018.pdf"
    
    #####¤¤¤¤¤ TASK 1 ¤¤¤¤¤#####
    ### Create an object loading this pdf and extracting the details
    text_loader = TextExtractor(data_uri)
    
    ### write to file
    file_name = "allTextAsExcel.xls"
    HelperFunctions._write_to_excel(text_loader.text_blocks, file_name)
    
    #####¤¤¤¤¤ TASK 2 ¤¤¤¤¤#####
    ### NOTE! check readme file for reasons why using camelot only
    tables = TableResolver(text_loader.document) ### sends the document to the class    
    
   
# =============================================================================
    print("Analysis Complete")

