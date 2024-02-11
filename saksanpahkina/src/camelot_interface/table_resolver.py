# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:03:46 2024

@author: Neovius
"""

import camelot

class TableResolver:
    """Class to load the text and preprocess it"""

    def __init__(self, document):
        self.doc = document
       

    def read_tables(self):
        # Read PDF into a list of tables
#        tables = camelot.read_pdf("your_pdf_file.pdf")

        # Access tables in the list
        for table in self.doc:
            print(table.df)       