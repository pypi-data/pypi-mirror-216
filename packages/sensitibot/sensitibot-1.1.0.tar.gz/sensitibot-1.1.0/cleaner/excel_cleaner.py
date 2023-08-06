import os

import pandas as pd


def clean_excel_file(file, replace_file=False):
    """
    Cleans excel files.

    Args:
        files (dict): The excel file to clean.
        replace_files (bool): If true, the file will be replaced by the clean one.

    Returns:
        None.
    """
    filename = file["name"]
    positive_sheets = file["positive_sheets"] if "positive_sheets" in file else [
    ]

    try:
        data = pd.ExcelFile(filename, engine='openpyxl')
    except Exception as e:
        error = {"file": filename, "error": str(e)}

    base_filename, extension = os.path.splitext(filename)

    if not replace_file:
        base_filename = base_filename + "_clean"

    new_filename = base_filename + extension

    writer = pd.ExcelWriter(new_filename, engine='xlsxwriter')

    for sheet_name in data.sheet_names:
        sheet_data = data.parse(sheet_name, dtype=str)

        positive_sheet = next(
            (sheet for sheet in positive_sheets if sheet["name"] == sheet_name), None)

        if positive_sheet != None:
            positive_headers = positive_sheet["positive_headers"] if "positive_headers" in positive_sheet else [
            ]
            positive_columns = positive_sheet["positive_columns"] if "positive_columns" in positive_sheet else dict(
            )

            columns = sheet_data.columns.values
            for column in columns:
                if column in positive_headers or column in list(positive_columns.keys()):
                    sheet_data = sheet_data.drop(column, axis=1)

        sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

    writer.close()
