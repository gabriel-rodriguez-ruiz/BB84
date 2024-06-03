# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 21:56:40 2024

@author: Gabriel
"""

from load_data import assign_roles
from characters import Alice, Bob
from pathlib import Path

data_folder = Path("Data/")
file_name = "BB84 18_05_2024-18_05_2024 .csv"
file_to_open = data_folder / file_name

eavesdropping = False

Alice_list, Bob_list, Eve_list = assign_roles(file_to_open, eavesdropping)

for i in range(len(Alice_list)):
    Alice_list[i].send_to_Bob(Eve_list[i], Bob_list[i])

print(Alice_list, Eve_list, Bob_list)