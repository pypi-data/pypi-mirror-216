def get_matches(file):
    matches = ""

    if "positive_headers" in file:
        for positive_header in file['positive_headers']:
            matches = f"{matches}\tHeader {positive_header} may contain sensible data\n"

    if "positive_columns" in file:
        for positive_column, positive_fields in file['positive_columns'].items():
            matches = f"{matches}\tColumn: {positive_column}:\tDetected fields: {positive_fields}\n"

    return matches


def get_matches_excel(file):
    matches = ""

    if "positive_sheets" in file:
        for positive_sheet in file['positive_sheets']:
            matches = f"{matches}\tSheet {positive_sheet['name']}:\n"

            if "positive_headers" in positive_sheet:
                for positive_header in positive_sheet['positive_headers']:
                    matches = f"{matches}\t\tHeader {positive_header} may contain sensible data\n"

            if "positive_columns" in positive_sheet:
                for positive_column, positive_fields in positive_sheet['positive_columns'].items():
                    matches = f"{matches}\t\tColumn: {positive_column}:\tDetected fields: {positive_fields}\n"
    return matches


def get_matches_access(file):
    matches = ""

    if "positive_tables" in file:
        for positive_table in file['positive_tables']:
            matches = f"{matches}\tTable {positive_table['name']}:\n"

            if "positive_headers" in positive_table:
                for positive_header in positive_table['positive_headers']:
                    matches = f"{matches}\t\tHeader {positive_header} may contain sensible data\n"

            if "positive_columns" in positive_table:
                for positive_column, positive_fields in positive_table['positive_columns'].items():
                    matches = f"{matches}\t\tColumn: {positive_column}:\tDetected fields: {positive_fields}\n"
    return matches
