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
            df.loc[i, "Basis"] = "\u2795" # +
            df.loc[i, "Result"] = "\u24EA" #0
        elif df.loc[i, "Measurement"]=="B":
            df.loc[i, "Basis"] = "\u2795" # +
            df.loc[i, "Result"] = "\u2460" #1
        elif df.loc[i, "Measurement"]=="C":
            df.loc[i, "Basis"] = "\u274C" #x
            df.loc[i, "Result"] = "\u24EA" #0
        elif df.loc[i, "Measurement"]=="D":
            df.loc[i, "Basis"] = "\u274C" #x
            df.loc[i, "Result"] = "\u2460" #1
    return df

def load_data(file_to_open):
    "Load data from a csv file to a dataframe."
    df = read_csv(file_to_open)
    df = translate_df(df)
    even_count = len([x for x in df["Card_Number"] if x%2==0]) # Number of Bobs
    odd_count = len(df["Card_Number"]) - even_count # Number of Alices
    if even_count>odd_count:     # add an Alice
        d = even_count - odd_count
        for i in range(d):
            df.loc[len(df.index)] = [65 + 2*i, "X",      
                                     random.choice(["\u2795", "\u274C"]),
                                     random.choice([0, 1])]
    elif odd_count>even_count:   # add a Bob
        d = odd_count - even_count
        for i in range(d):
            df.loc[len(df.index)] = [64 + 2*i, "X", 
                                     random.choice(["\u2795", "\u274C"]),
                                     None]
    return df

def assign_roles(file_to_open, eavesdropping):
    Alice_list = []
    Bob_list = []
    Eve_list = []
    df = load_data(file_to_open)
    for i, n in enumerate(df["Card_Number"]):
        if n%2==1:
            Alice_list.append(Alice(df[df["Card_Number"]==n].at[i, "Basis"],
                                    df[df["Card_Number"]==n].at[i, "Result"],
                                    df[df["Card_Number"]==n].at[i, "Card_Number"],
                                    df[df["Card_Number"]==n].at[i, "Measurement"])
                              )
            Eve_list.append(Eve(random.choice(["\u2795", "\u274C"]), eavesdropping))
        else:
            Bob_list.append(Bob(df[df["Card_Number"]==n].at[i, "Basis"],
                                    df[df["Card_Number"]==n].at[i, "Card_Number"],
                                    df[df["Card_Number"]==n].at[i, "Measurement"])
                            )
    return Alice_list, Bob_list, Eve_list
