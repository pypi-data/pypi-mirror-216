import pandas as pd

from reader import columns_reader, headers_reader


def read_excel_file(file, deep_search=False, wide_search=False):
    """
    Analyzes the excel file.

    Args:
        files (str): The file to analyze.
        deep_search (bool): If true, the content of the files will be analyzed.
        wide_search (bool): If true, all the tables or sheets will be analyzed.

    Returns:
        dict: The result of analyzing the excel file.
    """
    try:
        data = pd.ExcelFile(file, engine='openpyxl')
    except Exception as e:
        error = {"file": file, "error": str(e)}
        return None, error

    sheet_names = data.sheet_names
    sheets_to_read = sheet_names

    if not wide_search and len(sheet_names) > 1:
        read_all_sheets = ask_read_all_sheets(len(sheet_names))
        if not read_all_sheets:
            sheets_to_read = ask_which_sheets(sheet_names)

    result_file = {"name": file}

    result_sheets = []
    for sheet_name in sheets_to_read:
        sheet_data = data.parse(sheet_name, dtype=str)
        result_sheet = read_sheet(sheet_name, sheet_data, deep_search)

        if result_sheet != None:
            result_sheets.append(result_sheet)

    if len(result_sheets) != 0:
        result_file["positive_sheets"] = result_sheets

    if len(result_file) == 1:
        return None, None

    return result_file, None


def read_sheet(sheet_name, sheet_data, deep_search=False):
    result_sheet = {"name": sheet_name}

    headers = sheet_data.columns.values
    result_headers = headers_reader.analize_headers(headers)

    # Only show headers that have errors
    if len(result_headers) != 0:
        result_sheet["positive_headers"] = result_headers

    # Only analyze columns if deep_search is enabled
    if deep_search:
        result_columns = columns_reader.analize_columns(sheet_data, headers)

        # Only show columns that have errors
        if len(result_columns) != 0:
            result_sheet["positive_columns"] = result_columns

    if len(result_sheet) == 1:
        return None

    return result_sheet


def ask_read_all_sheets(number_of_sheets):
    ask_read_all_sheets = input(
        f"\n\t\tDo you want to read all ({number_of_sheets}) sheets? (yes/no): ")
    while ask_read_all_sheets.lower() not in ("yes", "no"):
        ask_read_all_sheets = input(
            "\t\tPlease enter either 'yes' or 'no': ")
    return ask_read_all_sheets.lower() == "yes"


def ask_which_sheets(sheet_names):
    sheets_to_read = []

    print("\t\tSelect which sheets to read:")

    for sheet_name in sheet_names:
        ask_sheet = input(
            f"\t\t\tRead sheet {sheet_name}? (yes/no): ")

        while ask_sheet.lower() not in ("yes", "no"):
            ask_sheet = input(
                "\t\t\tPlease enter either 'yes' or 'no': ")

        if ask_sheet.lower() == "yes":
            sheets_to_read.append(sheet_name)

    return sheets_to_read
