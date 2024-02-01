# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 13:13:04 2024

@author: Neovius
"""

from pathlib import Path
#from typing import List
#from urllib.request import urlretrieve
#from sklearn.preprocessing import StandardScaler
import fitz 
import cv2
import numpy as np
import pandas as pd
import openpyxl


class TextExtractor:
    """Class to load the text and preprocess it"""

    #data_url: str = "https://www.chesdata.eu/s/CHES2019V3.dta"

    def __init__(self, uri):
        #self.party_data = self._download_data()
        self.data_uri = uri
        self.document = self._fetch_data()
        self.textBlocks = self.preprocess_data()
       # self.non_features = []
       # self.index = ["party_id", "party", "country"]

    def _fetch_data(self) -> pd.DataFrame:
        #data_path, _ = urlretrieve(
        #    self.data_url,
        #    Path(__file__).parents[2].joinpath(*["data", "CHES2019V3.dta"]),
        #)
        return fitz.open(self.data_uri)
        #return pd.read_stata(data_path)
    
    #def _download_data(self) -> pd.DataFrame:
    #    data_path, _ = urlretrieve(
    #        self.data_url,
    #        Path(__file__).parents[2].joinpath(*["data", "CHES2019V3.dta"]),
    #    )
    #    return pd.read_stata(data_path)

# =============================================================================
#     def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Write a function to remove duplicates in a dataframe"""
#         ##### YOUR CODE GOES HERE #####
#         columns_to_check = df.columns
#         pdf_nonDuplicates = df.drop_duplicates(subset=columns_to_check)
#         return pdf_nonDuplicates
# 
#     def remove_nonfeature_cols(
#         self, df: pd.DataFrame, non_features: List[str], index: List[str]
#     ) -> pd.DataFrame:
#         """Write a function to remove certain features cols and set certain cols as indices
#         in a dataframe"""
#         ##### YOUR CODE GOES HERE #####
#         pdf = df.drop(non_features, axis = 1)
#         pdf = pdf.set_index(index)
#         return pdf
# 
#     def handle_NaN_values(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Write a function to handle NaN values in a dataframe"""
#         ##### YOUR CODE GOES HERE #####
#         df = df.dropna(axis=1, how='all')
#         pdf = df.apply(lambda col: col.fillna(col.mean()), axis=0)
#         return pdf
#     
#     def scale_features(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Write a function to normalise values in a dataframe. Use StandardScaler."""
#         ##### YOUR CODE GOES HERE #####
#         scaler = StandardScaler()
#         pdf = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
#         return pdf
# 
# 
    def preprocess_data(self):
        blocks_info = []
        for page in range(len(self.document)):
            ### If there are splits of a page (as is the case on page 2) 
            ### then the page must first be converted into an image (grayscale)
            ### and split where such lines are present in the PDF. 
            ### We cannot operate on the image, otherwise OCR would need to be 
            ### applied introducing problems. Rudimentary example below.
                        
            one_page_blocks = self.document[page].get_text("blocks")
            ### order by x0, y0 coordinates
            sorted_blocks = sorted(one_page_blocks , key=lambda x:(x[0], x[1]))

            for block in range(len(sorted_blocks)):
                x0 = sorted_blocks[block][0] ### writing out for clarity
                y0 = sorted_blocks[block][1]
                x1 = sorted_blocks[block][2]
                y1 = sorted_blocks[block][3]
                text = sorted_blocks[block][4]
                sequenceNr = block ### this goes sometimes wrong -> fixed
                isImage = sorted_blocks[block][6]
           # text = onePageBlocks[4]
                #pp = page + 1
            
                blocks_info.append({'page': page, 
                               #'box': coordinates,
                               'x0': x0,
                               'y0': y0,
                               'x1': x1,
                               'y1': y1,
                               'text': text,
                               'blockSequence': sequenceNr,
                               'isImage': isImage
                               #'text': text
                               #'all': onePageBlocks
                               
                               })
            #print(page+1)
        #self.document.close()
        return blocks_info

    def write_to_excel(self, output_file_name):
        

#def write_list_to_excel(output_file, data_list):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        
        ### get the keys (only once to get the column names)
        sheet.append(list(self.textBlocks[0].keys()))
        
        for row_data in self.textBlocks: #data_list:
            #print(row_data)
            sheet.append(list(row_data.values()))

        workbook.save(output_file_name)
        print("file written")

    def split_page_by_divisor_line(self, page_number):
        ## convert a page to an image and order this as a numpy array
        image_of_a_page = self.document[page_number].get_pixmap()
        image_of_a_page_np = np.frombuffer(image_of_a_page.samples, dtype=np.uint8).reshape((image_of_a_page.height, image_of_a_page.width, 3))
        
        ## make it grayscale
        gray_scale_image = cv2.cvtColor(image_of_a_page_np, cv2.COLOR_BGR2GRAY)
        ## find lines
        edges = cv2.Canny(gray_scale_image, 50, 150, apertureSize=3)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        combined_lines = []
        for contour in contours:
            # Use the contour to extract the coordinates of the line
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Assuming the contour represents a line if it has only two points
            if len(approx) == 2:
                combined_lines.append(approx)
        
#     def preprocess_data(self):
#         """Write a function to combine all pre-processing steps for the dataset"""
#         ##### YOUR CODE GOES HERE #####
#         self.party_data = self.remove_nonfeature_cols(self.party_data, self.non_features, self.index)
#         self.party_data = self.remove_duplicates(self.party_data)
#         self.party_data = self.handle_NaN_values(self.party_data)
#         self.party_data = self.scale_features(self.party_data)
# =============================================================================
        