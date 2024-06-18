# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:11:17 2024

@author: Gabriel
"""
import pandas as pd
import matplotlib.pyplot as plt
import panel as pn

def draw_table(Alice_list, Bob_list):
    Alice_data = pd.DataFrame({"Alice´s Basis": [Alice_list[i].Basis for i in range(len(Alice_list))],
                         "Alice´s Result": [Alice_list[i].Result for i in range(len(Alice_list))]})
    Bob_data = pd.DataFrame({"Bob´s Basis": [Bob_list[i].Basis for i in range(len(Alice_list))],
                         "Bob´s Result": [Bob_list[i].Result for i in range(len(Alice_list))]})
    
    fig = plt.figure(figsize=(4, 3), dpi=300)
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

def get_qbit(Alice_list, Bob_list, Eve_list):
    qubit_list = []
    for i in range(len(Alice_list)):
        Alice_list[i].send_to_Bob(Eve_list[i], Bob_list[i])
        qubit_list.append(Alice_list[i].df.join(Bob_list[i].df,
                                     lsuffix='_Alice',
                                     rsuffix='_Bob', how="outer"))
    qubit_df = pd.concat(qubit_list, ignore_index=True)
    qubit_df.columns = pd.MultiIndex.from_product([['Alice', 'Bob'],
                                                   [c for c in Alice_list[0].df.columns]])
    return qubit_df

def make_table(Alice_list, Bob_list, Eve_list):
    qubit_df = get_qbit(Alice_list, Bob_list, Eve_list)
    qubit_df.columns = qubit_df.columns.set_levels(["Base", "Número", "Letra", "Resultado"], level=1)
    
    groups = {group: [f"('{group}', 'Número')", f"('{group}', 'Letra')", f"('{group}', 'Base')", f"('{group}', 'Resultado')",
                 f"('{group}', 'Número')", f"('{group}', 'Letra')", f"('{group}', 'Base')", f"('{group}', 'Resultado')"] for group in qubit_df.columns.get_level_values(0).unique()}
    titles1 = {(f'{group}', 'Número'): "Número" for group in qubit_df.columns.get_level_values(0).unique()}
    titles2 = {(f'{group}', 'Letra'): "Letra" for group in qubit_df.columns.get_level_values(0).unique()}
    titles3 = {(f'{group}', 'Base'): "Base" for group in qubit_df.columns.get_level_values(0).unique()}
    titles4 = {(f'{group}', 'Resultado'): "Resultado" for group in qubit_df.columns.get_level_values(0).unique()}
    titles={**titles1, **titles2, **titles3, **titles4, **titles1, **titles2, **titles3, **titles4}
    
    table = pn.widgets.Tabulator(value=qubit_df.set_axis(qubit_df.columns.to_flat_index(), axis=1), groups=groups, titles=titles)
    return table
