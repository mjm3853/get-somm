"""This module provides tools for reading beer data.

It includes a function `beer_reader` that reads beer data from a CSV file
and returns it as a pandas DataFrame.
"""

import os

import pandas as pd
from langchain_core.tools import tool


@tool
def beer_reader() -> str:
    """Read beer data from a CSV file and return it as a JSON string.

    This tool reads beer inventory data from a CSV file located at 'data/beer_list.csv'.
    The data contains a curated selection of beers with their details and pricing.

    The CSV contains the following columns:
    - name: The name of the beer
    - abv: Alcohol by volume percentage
    - brewery: The brewery that produces the beer
    - location: The origin location of the brewery
    - description: A description of the beer's characteristics
    - servingSize: The size of the serving (e.g., 16oz, 12oz)
    - price: The price of the beer

    Returns:
        str: A JSON string containing the beer data. The JSON is in 'records' orientation,
             meaning each row of the CSV becomes a separate JSON object in an array.
             Each object contains the column names as keys and the corresponding values.

    Example:
        >>> beer_data = beer_reader()
        >>> # The returned JSON string can be parsed into a list of dictionaries:
        >>> import json
        >>> beers = json.loads(beer_data)
        >>> # Each beer in the list will have properties like:
        >>> # {
        >>> #     'name': 'IPA',
        >>> #     'abv': '6.5%',
        >>> #     'brewery': 'Local Brewery',
        >>> #     'location': 'Portland, OR',
        >>> #     'description': 'Hoppy and citrusy IPA',
        >>> #     'servingSize': '16oz',
        >>> #     'price': '$7'
        >>> # }
    """
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "..", "data", "beer_list.csv")
    return pd.read_csv(file_path).to_json(orient="records")
