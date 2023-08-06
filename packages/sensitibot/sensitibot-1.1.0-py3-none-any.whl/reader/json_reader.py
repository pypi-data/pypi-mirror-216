# Ignore warnings
import warnings

import pandas as pd

from reader import columns_reader, headers_reader

warnings.simplefilter(action='ignore', category=FutureWarning)


def read_json_file(file, deep_search=False):
    """
    Analyzes the json file.

    Args:
        files (str): The file to analyze.
        deep_search (bool): If true, the content of the files will be analyzed.

    Returns:
        dict: The result of analyzing the json file.
    """
    try:
        data = pd.read_json(file, lines=file.endswith(".jsonl"), dtype=str)
    except Exception as e:
        error = {"file": file, "error": str(e)}
        return None, None

    result_file = {"name": file}

    headers = data.columns.values
    result_headers = headers_reader.analize_headers(headers)

    # Only show headers that have errors
    if len(result_headers) != 0:
        result_file["positive_headers"] = result_headers

    # Only analyze columns if deep_search is enabled
    if deep_search:
        result_columns = columns_reader.analize_columns(data, headers)

        # Only show columns that have errors
        if len(result_columns) != 0:
            result_file["positive_columns"] = result_columns

    if len(result_file) == 1:
        return None, None

    return result_file, None
