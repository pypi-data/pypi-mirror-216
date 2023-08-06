import pandas as pd

from reader import columns_reader, headers_reader


def read_tsv_file(file, deep_search=False):
    """
    Analyzes the tsv file.

    Args:
        files (str): The file to analyze.
        deep_search (bool): If true, the content of the files will be analyzed.

    Returns:
        dict: The result of analyzing the tsv file.
    """
    try:
        data = pd.read_csv(file, comment='#', sep='\t',
                           engine='python', skip_blank_lines=True, dtype=str)
    except Exception as e:
        error = {"file": file, "error": str(e)}
        return None, error

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
