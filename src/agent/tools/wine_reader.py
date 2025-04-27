"""This module provides tools for reading wine data.

It includes a function `wine_reader` that reads wine data from a CSV file
and returns it as a pandas DataFrame.
"""

import os

import pandas as pd
from langchain_core.tools import tool


@tool
def wine_reader() -> str:
    """Read wine data from a CSV file and return it as a JSON string.
    
    This tool reads wine inventory data from a CSV file located at 'data/fratellos_2025.csv'.
    The data contains a curated selection of wines with their pricing and details.
    
    The CSV contains the following columns:
    - Category: The type of wine (Red or White)
    - Wine Name: The name of the wine
    - Region: The origin of the wine (e.g., California, Italy, New Zealand)
    - Glass Price: Price per glass (some entries may be empty)
    - Bottle Price: Price per bottle (some entries may be empty)
    
    The data includes various wine types such as:
    - Red wines: Pinot Noir, Chianti, Merlot, Malbec, Cabernet Sauvignon, etc.
    - White wines: Pinot Grigio, Sauvignon Blanc, Chardonnay, Prosecco, etc.
    
    Returns:
        str: A JSON string containing the wine data. The JSON is in 'records' orientation,
             meaning each row of the CSV becomes a separate JSON object in an array.
             Each object contains the column names as keys and the corresponding values.
             
    Example:
        >>> wine_data = wine_reader()
        >>> # The returned JSON string can be parsed into a list of dictionaries:
        >>> import json
        >>> wines = json.loads(wine_data)
        >>> # Each wine in the list will have properties like:
        >>> # {
        >>> #     'Category': 'Red',
        >>> #     'Wine Name': 'Stemmari Pinot Noir',
        >>> #     'Region': 'Italy',
        >>> #     'Glass Price': '$12',
        >>> #     'Bottle Price': '$46'
        >>> # }
    """
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "..", "data", "fratellos_2025.csv")
    return pd.read_csv(file_path).to_json(orient="records")