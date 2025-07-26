"""
Run this file to generate all data files.
"""

from data_excel_to_csv import convert
from data_processing import process_data

# ------------------------------
# define constants
# ------------------------------
fps = 30
initial_targets = 19
total_blocks = 57


# ------------------------------
# main 
# ------------------------------
if __name__ == '__main__':
    convert()
    process_data(fps, initial_targets, total_blocks)
