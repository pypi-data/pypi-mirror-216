import shutil
import tempfile

import pandas as pd
import requests
import sqlalchemy as sa

from reader import columns_reader, headers_reader


def read_access_file(file, deep_search=False, wide_search=False):
    """
    Analyzes the access file.

    Args:
        files (str): The file to analyze.
        deep_search (bool): If true, the content of the files will be analyzed.
        wide_search (bool): If true, all the tables or sheets will be analyzed.

    Returns:
        dict: The result of analyzing the access file.
    """
    new_file = file
    if file.startswith("http"):
        new_file = download_file(file)

    try:
        # Establish a connection to the Access database
        connection_string = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" +
            r"DBQ={};".format(new_file) +
            r"ExtendedAnsiSQL=1;"
        )
        connection_url = sa.engine.URL.create(
            "access+pyodbc", query={"odbc_connect": connection_string})
        engine = sa.create_engine(connection_url)
    except Exception as e:
        error = {"file": file, "error": str(e)}
        return None, error

    try:
        # Query to retrieve table names
        inspector = sa.inspect(engine)
        table_names = inspector.get_table_names()
    except Exception as e:
        error = {"file": file, "error": str(e)}
        return None, error

    tables_to_read = table_names
    if not wide_search and len(table_names) > 1:
        read_all_sheets = ask_read_all_tables(len(table_names))
        if not read_all_sheets:
            tables_to_read = ask_which_tables(table_names)

    result_file = {"name": file}

    result_tables = []
    for table_name in tables_to_read:

        # Query to retrieve all records from the table
        query = f"SELECT * FROM {table_name}"
        table_data = pd.read_sql_query(query, engine)

        result_table = read_table(table_name, table_data, deep_search)

        if result_table != None:
            result_tables.append(result_table)

    if len(result_tables) != 0:
        result_file["positive_tables"] = result_tables

    if len(result_file) == 1:
        return None, None

    engine.dispose()

    return result_file, None


def read_table(table_name, table_data, deep_search=False):
    result_table = {"name": table_name}

    headers = table_data.columns.values
    result_headers = headers_reader.analize_headers(headers)

    # Only show headers that have errors
    if len(result_headers) != 0:
        result_table["positive_headers"] = result_headers

    # Only analyze columns if deep_search is enabled
    if deep_search:
        result_columns = columns_reader.analize_columns(table_data, headers)

        # Only show columns that have errors
        if len(result_columns) != 0:
            result_table["positive_columns"] = result_columns

    if len(result_table) == 1:
        return None

    return result_table


def ask_read_all_tables(number_of_tables):
    ask_read_all_tables = input(
        f"\n\t\tDo you want to read all ({number_of_tables}) tables? (yes/no): ")
    while ask_read_all_tables.lower() not in ("yes", "no"):
        ask_read_all_tables = input(
            "\t\tPlease enter either 'yes' or 'no': ")
    return ask_read_all_tables.lower() == "yes"


def ask_which_tables(table_names):
    tables_to_read = []

    print("\t\tSelect which tables to read:")

    for table_name in table_names:
        ask_table = input(
            f"\t\t\tRead table {table_name}? (yes/no): ")

        while ask_table.lower() not in ("yes", "no"):
            ask_table = input(
                "\t\t\tPlease enter either 'yes' or 'no': ")

        if ask_table.lower() == "yes":
            tables_to_read.append(table_name)

    return tables_to_read


def download_file(file):
    # Create a temporary file to save the downloaded Access file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_path = temp_file.name

    # Download the Access file from GitHub
    response = requests.get(file, stream=True)
    with open(temp_file_path, "wb") as f:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)

    return temp_file_path
