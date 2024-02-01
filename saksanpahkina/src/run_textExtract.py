# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 12:51:13 2024

@author: Neovius
"""

from pathlib import Path

from pdf_analysis.loader import TextExtractor

if __name__ == "__main__":
    
    ### uri for pdf to load
    ### if being in a queue, doint this in a for loop loading one pdf after the other
    data_uri: str = "C:/Users/Neovius/OneDrive/Desktop/Työhakemuksia/TheWalnutAI/keppel-corporation-limited-annual-report-2018.pdf"
    
    ### Create an object loading this pdf and extracting the details
    text_loader = TextExtractor(data_uri)
    
    ### write to file
    file_name = "myExcel.xls"
    text_loader.write_to_excel(file_name)
    # Data pre-processing step
    # x1 = text_loader.document[3].get_text("blocks")
    #x2 = text_loader.bl
    ##### YOUR CODE GOES HERE #####
# =============================================================================
#     data_loader.preprocess_data()
# 
#     # Dimensionality reduction step
#     ##### YOUR CODE GOES HERE #####
#     dim_reduced = DimensionalityReducer(data_loader.party_data)
#     reduced_dim_data = dim_reduced.return2dpdf()
#     
#     ## Uncomment this snippet to plot dim reduced data
#     pyplot.figure()
#     splot = pyplot.subplot()
#     scatter_plot(
#         reduced_dim_data,
#         color="r",
#         splot=splot,
#         label="dim reduced data",
#     )
#     # pyplot.savefig(Path(__file__).parents[1].joinpath(*["plots", "dim_reduced_data.png"]))
# 
#     # Density estimation/distribution modelling step
#     ##### YOUR CODE GOES HERE #####
# 
#     # Plot density estimation results here
#     ##### YOUR CODE GOES HERE #####
#     pyplot.savefig(Path(__file__).parents[1].joinpath(*["plots", "density_estimation.png"]))
# 
#     # Plot left and right wing parties here
#     pyplot.figure()
#     splot = pyplot.subplot()
#     ##### YOUR CODE GOES HERE #####
#     pyplot.savefig(Path(__file__).parents[1].joinpath(*["plots", "left_right_parties.png"]))
#     pyplot.title("Lefty/righty parties")
# 
#     # Plot finnish parties here
#     ##### YOUR CODE GOES HERE #####
# 
# =============================================================================
    print("Analysis Complete")


print("test")
