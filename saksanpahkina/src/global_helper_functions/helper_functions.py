# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:16:03 2024

@author: Neovius
"""

import numpy as np
import pandas as pd
import openpyxl


class HelperFunctions:
    def _write_to_excel(text_blocks, output_file_name):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        
        ### get the keys (only once to get the column names)
        sheet.append(list(text_blocks[0].keys()))
        
        for row_data in text_blocks: #data_list:
            #print(row_data)
            sheet.append(list(row_data.values()))

        workbook.save(output_file_name)
        print("file written")