""" Processing Excel to CSV Files

This script processes the spreadsheet into csv files for further data extraction.
It is mainly to:
    - unmerge cells
    - assign values to N/A columns

It accepts only excel files (.xlsx). Users should put all data starting from the very top left corner in the excel sheet.
The column headers of the excel file should follow the exact same naming convention and order as follows:
    - ON/OFF	
    - Trial No.	
    - Trial Name	
    - Accuracy (/5)	
    - Cycle Start (seconds)	
    - Cycle Start (frames)	
    - Found Target (seconds)	
    - Found Target (frames)	
    - Release Target (seconds)	
    - Release Target (frames)	
    - No. of Objects Encountered
The excel file should also have the name "Raw Data Excel" and be put under the "Raw Data Files" folder.
A sample excel file can be found in the folder.

This script requires that `pandas` and 'openpyxl' be installed within the Python environment you are running this script in.

This file can is imported as a module and contains the following functions:
    * 
"""

import pandas as pd

def convert():
    """
    Main functionality: 
        - unmerge cells
        - assign values to N/A columns
    """
    df = pd.read_excel("./Raw Data Files/Raw Data.xlsx", engine='openpyxl')      # change excel file name here if necessary
 
    # Fill merged cells
    cols_to_fill = df.columns[[0, 1, 2]]
    df[cols_to_fill] = df[cols_to_fill].fillna(method='ffill')

    # Export to CSV
    df.to_csv('./Raw Data Files/Raw Data.csv', index=False)

convert()
