import os
import shutil

import pandas as pd
import sqlalchemy as sa


def clean_access_file(file, replace_file=False):
    """
    Cleans access files.

    Args:
        files (dict): The access file to clean.
        replace_files (bool): If true, the file will be replaced by the clean one.

    Returns:
        None.
    """
    filename = file["name"]
    positive_tables = file["positive_tables"] if "positive_tables" in file else [
    ]

    base_filename, extension = os.path.splitext(filename)

    if not replace_file:
        base_filename = base_filename + "_clean"

    new_filename = base_filename + extension

    if not replace_file:
        shutil.copyfile(filename, new_filename)

    try:
        connection_string = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" +
            r"DBQ={};".format(new_filename) +
            r"ExtendedAnsiSQL=1;"
        )
        connection_url = sa.engine.URL.create(
            "access+pyodbc", query={"odbc_connect": connection_string})
        engine = sa.create_engine(connection_url)
    except Exception as e:
        error = {"file": new_filename, "error": str(e)}

    for positive_table in positive_tables:
        positive_name = positive_table["name"] if "name" in positive_table else ""
        positive_headers = positive_table["positive_headers"] if "positive_headers" in positive_table else [
        ]
        positive_columns = positive_table["positive_columns"] if "positive_columns" in positive_table else dict(
        )

        deleted_columns = []

        for positive_header in positive_headers:
            if positive_header not in deleted_columns:
                delete_column(
                    new_filename, positive_table["name"], positive_header, engine)
                deleted_columns.append(positive_header)

        for positive_column in positive_columns.keys():
            if positive_column not in deleted_columns:
                delete_column(
                    new_filename, positive_table["name"], positive_column, engine)
                deleted_columns.append(positive_column)

    engine.dispose()


def delete_column(filename, table_name, column_name, engine):
    # If the column exists, remove it from the table
    with engine.begin() as connection:
        connection.execute(
            sa.text(f'ALTER TABLE "{table_name}" DROP COLUMN "{column_name}"'))
