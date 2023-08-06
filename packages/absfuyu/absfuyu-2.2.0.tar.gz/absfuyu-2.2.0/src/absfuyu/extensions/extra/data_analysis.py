"""
Absfuyu: Data Analysis
---
Extension for `pd.DataFrame`

Version: 2.0.0
Date updated: 15/06/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import random
import itertools
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats



# Function
###########################################################################
def summary(data: Union[list, np.ndarray]):
    """
    Quick summary of data
    
    data : np.ndarray | list
    """
        
    if not isinstance(data, np.ndarray):
        data = np.array(data)

    output = {
        "Observations": len(data),
        "Mean": np.mean(data),
        "Median": np.median(data),
        "Mode": stats.mode(data)[0][0],
        "Standard deviation": np.std(data),
        "Variance": np.var(data),
        "Max": max(data),
        "Min": min(data),
        "Percentiles": {
            "1st Quartile": np.quantile(data, 0.25),
            "2nd Quartile": np.quantile(data, 0.50),
            "3rd Quartile": np.quantile(data, 0.75),
            "IQR": stats.iqr(data),
        },
    }
    return output


def mplt_fmt_str(
        marker = None,
        linestyle = None,
        color = None,
        alt: bool = False,
        random: bool = True,
        raw: bool = False,
    ):
    r"""
    matplotlib format string helper
    ---
    This helper is ripped from the original matplotlib"s documentation

    Init
    ---
    Format string is in the form of: [marker][line][color]
    or [color][marker][line]

    Marker
    ---
    ".":    point marker
    ",":    pixel marker
    "o":    circle marker
    "v":    triangle_down marker
    "^":    triangle_up marker
    "<":    triangle_left marker
    ">":    triangle_right marker
    "1":    tri_down marker
    "2":    tri_up marker
    "3":    tri_left marker
    "4":    tri_right marker
    "8":    octagon marker
    "s":    square marker
    "p":    pentagon marker
    "P":    plus (filled) marker
    "*":    star marker
    "h":    hexagon1 marker
    "H":    hexagon2 marker
    "+":    plus marker
    "x":    x marker
    "X":    x (filled) marker
    "D":    diamond marker
    "d":    thin_diamond marker
    "|":    vline marker
    "_":    hline marker

    Linestyle
    ---
    "-":    solid line style
    "--":   dashed line style
    "-.":   dash-dot line style                     \
    ":":    dotted line style

    Color
    ---
    "b":    blue
    "g":    green
    "r":    red
    "c":    cyan
    "m":    magenta
    "y":    yellow
    "k":    black
    "w":    white

    Parameters
    ---
    alt : bool
        Alternative format string

    random : bool
        Generate random format string, 
        else generate combination
    
    raw : bool
        Return format string in list
    """

    if marker is None:
        marker_list = [
            ".", ",", "o", "v", "^", "<", ">", "1", "2", "3",
            "4", "8", "s", "p", "P", "*", "h", "H", "+", "x",
            "X", "D", "d", "|", "_",
        ]
    else:
        marker_list = marker
    
    if linestyle is None:
        linestyle_list = [
            "-", "--", "-.", ":",
        ]
    else:
        linestyle_list = linestyle
    
    if color is None:
        color_list = [
            "b", "g", "r", "c", "m", "y", "k",
            # "w",
        ]
    else:
        color_list = color
    
    if not random:
        fmt_str = [marker_list, linestyle_list, color_list]
        fmt_str_comb = ["".join(x) for x in list(itertools.product(*fmt_str))]
        return fmt_str_comb

    format_string = [
        random.choice(marker_list),
        random.choice(linestyle_list),
        random.choice(color_list),
    ]

    if raw:
        return format_string

    if alt:
        return "".join([format_string[2], format_string[0], format_string[1]])
    else:
        return "".join(format_string)

def gen_mptl_fmt_str(num):
    """
    Generate a list of matplotlib format string
    """
    # Init list
    fs = []
    
    # Error loop break
    error_count = 0
    max_error = 20000

    # Main
    while len(fs) < num:
        temp = mplt_fmt_str()
        if temp not in fs:
            fs.append(temp)
        else:
            error_count += 1
            if error_count > max_error:
                break
    
    # Output
    return fs


def divide_dataframe(df: pd.DataFrame, by: str) -> list:
    """
    Divide df into a list of df
    """
    divided = [y for _, y in df.groupby(by)]
    # divided[0] # this is the first separated df
    # divided[len(divided)-1] # this is the last separated df
    return divided


def delta_date(df: pd.DataFrame, date_field: str, col_name: str="delta_date"):
    """
    Calculate date interval between row
    """
    dated = df[date_field].to_list()
    cal = []
    for i in range(len(dated)):
        if i==0:
            cal.append(dated[i]-dated[i])
        else:
            cal.append(dated[i]-dated[i-1])
    df[col_name] = [x.days for x in cal]
    return df



def modify_date(df: pd.DataFrame, date_col: str):
    """
    Add date, week, and year column for date_col
    """
    df["Date"] = pd.to_datetime(df[date_col])
    df["Week"] = df["Date"].dt.isocalendar().week
    df["Year"] = df["Date"].dt.isocalendar().year
    return df


def equalize_df(data: dict, fillna = np.nan):
    """
    Make all list in dict have equal length to make pd.DataFrame
    """
    max_len = 0
    for _, v in data.items():
        if len(v) >= max_len:
            max_len = len(v)
    for _, v in data.items():
        if len(v) < max_len:
            missings = max_len-len(v)
            for _ in range(missings):
                v.append(fillna)
    return data



# Class
###########################################################################
class MatplotlibFormatString:
    pass


class DataFrameKai(pd.DataFrame):
    def get_unique(self, col: str):
        """
        Return a list of unique values in a column
        """
        return list(self[col].unique())
    
    def convert_to_SeriesKai(self):
        pass

    def summary(self, col: str):
        """
        Quick summary of data
        """
        data = self[col]
            
        if not isinstance(data, np.ndarray):
            data = np.array(data)

        output = {
            "Observations": len(data),
            "Mean": np.mean(data),
            "Median": np.median(data),
            "Mode": stats.mode(data)[0][0],
            "Standard deviation": np.std(data),
            "Variance": np.var(data),
            "Max": max(data),
            "Min": min(data),
            "Percentiles": {
                "1st Quartile": np.quantile(data, 0.25),
                "2nd Quartile": np.quantile(data, 0.50),
                "3rd Quartile": np.quantile(data, 0.75),
                "IQR": stats.iqr(data),
            },
        }
        return output


class SeriesKai(pd.Series):
    pass

# Run
###########################################################################
if __name__ == "__main__":
    pass