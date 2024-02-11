# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 13:13:04 2024

@author: Neovius
"""

from pathlib import Path
import fitz 
import cv2
import numpy as np
import pandas as pd
import openpyxl


class TextExtractor:
    """Class to load the text and preprocess it"""

    def __init__(self, uri):
        self.data_uri = uri
        self.document = self._fetch_data()
        self.text_blocks = self._preprocess_data()


    def _fetch_data(self) -> pd.DataFrame:
        return fitz.open(self.data_uri)

        
    def _preprocess_data(self):
        blocks_info = []
        for page in range(len(self.document)):
            ### If there are splits of a page (as is the case on page 2) 
            ### then the page must first be converted into an image (grayscale)
            ### and split where such lines are present in the PDF. 
            ### We cannot operate on the image, otherwise OCR would need to be 
            ### applied introducing problems. Rudimentary example below 
            ### function "_split_page_by_divisor_line"
                        
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
            
                blocks_info.append({'page': page, 
                               'x0': x0,
                               'y0': y0,
                               'x1': x1,
                               'y1': y1,
                               'text': text,
                               'blockSequence': sequenceNr,
                               'isImage': isImage
                               })
        return blocks_info


    def _split_page_by_divisor_line(self, page_number):
        ## convert a page to an image and order this as a numpy array
        image_of_a_page = self.document[page_number].get_pixmap()
        image_of_a_page_np = np.frombuffer(image_of_a_page.samples, dtype=np.uint8).reshape((image_of_a_page.height, image_of_a_page.width, 3))
        
        ## make it grayscale
        gray_scale_image = cv2.cvtColor(image_of_a_page_np, cv2.COLOR_BGR2GRAY)
        #### NOTE!
        #### I would do this by histograms capturing vertical and horizontal lines (not diagonal)
        #### in order to split a page to "sections" by meaning, e.g. page 2 with content listing
        #### causes hickups otherwise
        
        ### find lines 
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

        