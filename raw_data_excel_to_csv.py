""" Processing Excel to CSV Files

This script processes the spreadsheet into csv files for further data extraction.
It is mainly to:
    - unmerge cells
    - assign values to N/A columns

It accepts only excel files (.xlsx). Users should put all data starting from the very top left corner in the excel sheet.
The excel file should also have the name "Raw Data Excel" and be put under the "Raw Data Files" folder.
All cells should either contain data or NaN values, apart from columns A, B, C, where merging is allowed.
A sample excel file can be found in the folder. Format should be strictly followed to allow a working script.

This script requires that `pandas` and 'openpyxl' be installed within the Python environment you are running this script in.

This file can is imported as a module and contains the following functions:
    * convert()
"""

import pandas as pd

def convert():
    """
    Main functionality: 
        - unmerge cells
        - assign values to N/A columns
    """

    # change excel file name here if necessary
    df = pd.read_excel("./Raw Data Files/Raw Data.xlsx", engine='openpyxl')      
 
    # Fill merged cells
    cols_to_fill = df.columns[[0, 1, 2]]
    df[cols_to_fill] = df[cols_to_fill].fillna(method='ffill')

    # Strip whitespace from all string columns
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Export to CSV
    df.to_csv('./Raw Data Files/Raw Data.csv', index=False)


