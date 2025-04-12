"""This module provides tools for reading wine data.

It includes a function `wine_reader` that reads wine data from a CSV file
and returns it as a pandas DataFrame.
"""

import os

import pandas as pd
from langchain_core.tools import tool


@tool
def wine_reader() -> str:
    """Read wine data from a CSV file."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "..", "data", "fratellos_2025.csv")
    return pd.read_csv(file_path).to_json(orient="records")