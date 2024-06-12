# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:11:17 2024

@author: Gabriel
"""
import pandas as pd
import matplotlib.pyplot as plt

def draw_table(Alice_list, Bob_list):
    Alice_data = pd.DataFrame({"Alice´s Basis": [Alice_list[i].Basis for i in range(len(Alice_list))],
                         "Alice´s Result": [Alice_list[i].Result for i in range(len(Alice_list))]})
    Bob_data = pd.DataFrame({"Bob´s Basis": [Bob_list[i].Basis for i in range(len(Alice_list))],
                         "Bob´s Result": [Bob_list[i].Result for i in range(len(Alice_list))]})
    
    fig = plt.figure(figsize=(16/2.54, 6/2.54), dpi=300)
    ax = plt.subplot()
    
    ncols = 4
    nrows = Alice_data.shape[0]
    
    ax.set_xlim(0, ncols)
    ax.set_ylim(0-0.5, nrows + 1.5)
    
    positions = [0.5, 1.5, 2.5, 3.5]
    columns = ["Alice´s Basis", "Alice´s Result", "Bob´s Basis", "Bob´s Result"]
    
    # Add table's main text
    for i in range(nrows):
        for j, column in enumerate(columns):
            if column in Alice_data.columns:
                ha = 'center'
                ax.annotate(
                    xy=(positions[j], i),
                    text=Alice_data[column].iloc[i],
                    ha=ha,
                    va='center'
                )
            else:
                ha = 'center'
                ax.annotate(
                    xy=(positions[j], i),
                    text=Bob_data[column].iloc[i],
                    ha=ha,
                    va='center'
                )
    
    # Add column names
    ax.annotate(
        xy=(1, nrows+1),
        text='Alice',
        weight='bold',
        ha='center',
        va="center"
    )
    ax.annotate(
        xy=(3, nrows+1),
        text='Bob',
        weight='bold',
        ha='center',
        va="center"
    )
    column_names = ['Base', 'Resultado', 'Base', 'Resultado']
    for index, c in enumerate(column_names):
        ha = 'center'
        ax.annotate(
            xy=(positions[index], nrows),
            text=column_names[index],
            ha=ha,
            va='center',
            weight='bold'
        )
    
    # Add dividing lines
    ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [nrows-0.5, nrows-0.5], lw=1.5, color='black', marker='', zorder=4)
    ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [0-0.5, 0-0.5], lw=1.5, color='black', marker='', zorder=4)
    for x in range(1, nrows):
        ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [x-0.5, x-0.5], lw=1.15, color='gray', ls=':', zorder=3 , marker='')
        ax.axvline(x=nrows, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], lw=1.5, color='black', marker='', zorder=4)
    
    ax.set_axis_off()
    plt.savefig("BB84.pdf")
    # plt.show()
    return fig, ax