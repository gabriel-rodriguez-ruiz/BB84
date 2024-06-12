# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 12:27:34 2024

@author: Gabriel
"""

import pandas as pd
import random
from characters import Alice, Bob, Eve
from pathlib import Path

data_folder = Path("Data/")
file_name = "BB84 18_05_2024-18_05_2024 .csv"
file_to_open = data_folder / file_name

def read_csv(file_to_open):
    "Read a csv file and return a panda´s data frame."
    df = pd.read_csv(file_to_open, skiprows=[0, 1, 3, 4, 5], usecols=[0, 6])
    df.rename(columns={ df.columns[0]: "Card_Number" }, inplace = True)
    df.rename(columns={ df.columns[1]: "Measurement" }, inplace = True)
    return df

def translate_df(df):
    "Traslate dataframe measurement to qbit basis and result."
    df["Basis"] = None
    df["Result"] = None
    for i in range(len(df)):
        if df.loc[i, "Measurement"]=="A":
            df.loc[i, "Basis"] = "H/V"
            df.loc[i, "Result"] = 0
        elif df.loc[i, "Measurement"]=="B":
            df.loc[i, "Basis"] = "H/V"
            df.loc[i, "Result"] = 1
        elif df.loc[i, "Measurement"]=="C":
            df.loc[i, "Basis"] = "+45/-45"
            df.loc[i, "Result"] = 0
        elif df.loc[i, "Measurement"]=="D":
            df.loc[i, "Basis"] = "+45/-45"
            df.loc[i, "Result"] = 1
    return df

def load_data(file_to_open):
    "Load data from a csv file to a dataframe."
    df = read_csv(file_to_open)
    df = translate_df(df)
    if len(df)%2==1:
        df.loc[len(df.index)] = [41, "X", 
                                 random.choice(["H/V", "+45/-45"]),
                                 random.choice([0, 1])]    
    return df

def assign_roles(file_to_open, eavesdropping):
    Alice_list = []
    Bob_list = []
    Eve_list = []
    df = load_data(file_to_open)
    for i in range(len(df)):
        if i%2==0:
            Alice_list.append(Alice(df.loc[i, "Basis"], df.loc[i, "Result"]))
            Eve_list.append(Eve(random.choice(["H/V", "+45/-45"]), eavesdropping))
        else:
            Bob_list.append(Bob(df.loc[i, "Basis"]))
    return Alice_list, Bob_list, Eve_list
