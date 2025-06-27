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
import sys
import matplotlib
import panel as pn
import hvplot.pandas
from draw_table import draw_table, get_qbit, make_table


pn.extension(sizing_mode="stretch_width")
pn.extension('tabulator')
pn.extension('katex', 'mathjax')
pn.extension()
#%matplotlib widget

data_folder = Path("Data/")
# file_name = sys.argv[1]
file_name = "BB84 17_06_2024-18_06_2024 .csv"
file_to_open = data_folder / file_name

eavesdropping = True

Alice_list, Bob_list, Eve_list = assign_roles(file_to_open, eavesdropping)

for i in range(len(Alice_list)):
    Alice_list[i].send_to_Bob(Eve_list[i], Bob_list[i])
    
table, qubit_df, checkbox_group = make_table(Alice_list, Bob_list, Eve_list)


column = pn.Column(table, checkbox_group).servable()
