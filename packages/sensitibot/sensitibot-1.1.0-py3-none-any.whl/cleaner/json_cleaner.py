import os

import pandas as pd

# Ignore warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def clean_json_file(file, replace_file=False):
    """
    Cleans json files.

    Args:
        files (dict): The json file to clean.
        replace_files (bool): If true, the file will be replaced by the clean one.

    Returns:
        None.
    """
    filename = file["name"]
    positive_headers = file["positive_headers"] if "positive_headers" in file else [
    ]
    positive_columns = file["positive_columns"] if "positive_columns" in file else dict(
    )

    try:
        is_linear = filename.endswith(".jsonl")
        data = pd.read_json(
            filename, lines=is_linear, dtype=str)
    except Exception as e:
        error = {"file": filename, "error": str(e)}

    columns = data.columns.values
    for column in columns:
        if column in positive_headers or column in list(positive_columns.keys()):
            data = data.drop(column, axis=1)

    base_filename, extension = os.path.splitext(filename)

    if not replace_file:
        base_filename = base_filename + "_clean"

    new_filename = base_filename + extension
    data.to_json(new_filename, orient="records",
                 lines=is_linear, indent=0 if is_linear else 4)
