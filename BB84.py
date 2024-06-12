# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 21:56:40 2024

@author: Gabriel
"""
import pandas as pd
from load_data import assign_roles, load_data
from characters import Alice, Bob
from pathlib import Path
import matplotlib.pyplot as plt
from draw_table import draw_table
import sys

if __name__=="__main__":
    data_folder = Path("Data/")
    # file_name = sys.argv[1]
    file_name = "BB84 03_06_2024-03_06_2024 .csv"
    file_to_open = data_folder / file_name
    
    eavesdropping = True
    
    Alice_list, Bob_list, Eve_list = assign_roles(file_to_open, eavesdropping)
    
    for i in range(len(Alice_list)):
        Alice_list[i].send_to_Bob(Eve_list[i], Bob_list[i])
    
    draw_table(Alice_list, Bob_list)
