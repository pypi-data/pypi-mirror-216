import re


def analize_columns(data, columns):
    """
    Analyzes the columns of a file.

    Args:
        data (list): The data of the file.
        headers (list): The headers of the file.

    Returns:
        list: The columns that may have sensitive information.
    """
    positive_columns = {}
    number_of_rows = len(data)
    ratio = number_of_rows * 0.1

    for column in columns:
        positive_fields = set()

        count = 0
        for index, value in data[column].items():
            result_field = analize_field(str(value))
            if result_field != None:
                count += 1
                positive_fields.add(result_field)

            if count >= ratio:
                break

        if len(positive_fields) != 0:
            positive_columns[column] = list(positive_fields)

    return positive_columns


def analize_field(field):
    """
    Analyzes a field.

    Args:
        field (str): The field to analyze.

    Returns:
        str: The type of sensitive information that the field may have.
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    iban_pattern = r'^[a-zA-Z]{2}\d{2}[a-zA-Z0-9]{4}\d{7}([a-zA-Z0-9]?){0,16}$'
    phone_pattern_optional_prefix = r'^(\+\d{1,3})?(\d{4,15})$'
    phone_pattern_with_prefix = r'^\+\d{1,3}\d{4,15}$'
    dni_pattern = r'^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]$'

    patterns = {"email": email_pattern, "iban": iban_pattern,
                "phone": phone_pattern_with_prefix, "dni": dni_pattern}

    for type, pattern in patterns.items():
        if re.match(pattern, field):
            return type

    return None
