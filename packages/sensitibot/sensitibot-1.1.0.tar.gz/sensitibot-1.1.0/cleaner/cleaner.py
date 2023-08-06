from cleaner import (csv_cleaner, excel_cleaner, json_cleaner, show_matches,
                     tsv_cleaner)


def process_cleaner(files):
    generate_clean_files = input(
        "\nDo you want to generate clean files? (yes/no): ")
    while generate_clean_files.lower() not in ("yes", "no"):
        generate_clean_files = input("Please enter either 'yes' or 'no': ")
    if generate_clean_files.lower() == "yes":
        clean_files(files)


def clean_files(files):
    """
    Initiates the process of cleaning the files.

    Args:
        files (dict): The files to clean.
        replace_files (bool): If true, the files will be replaced by the clean ones.

    Returns:
        None.
    """
    repository = files["repositories"][0]

    for file in repository["files"]:
        clean_file(file)


def clean_file(file):
    """
    Cleans the file.

    Args:
        file (str): The file to clean.

    Returns:
        None.
    """
    print("\nCleaning file: " + file["name"])

    matches = ""

    basic_extensions = [".csv", ".tsv", ".json", ".jsonl"]
    if any(file["name"].endswith(ext) for ext in basic_extensions):
        matches = show_matches.get_matches(file)

    if file["name"].endswith('.xlsx') or file["name"].endswith('.xls'):
        matches = show_matches.get_matches_excel(file)

    if file["name"].endswith('.mdb') or file["name"].endswith('.accdb'):
        matches = show_matches.get_matches_access(file)

    print(matches)

    clean, replace = ask_clean_file()

    if clean:
        if file["name"].endswith('.csv'):
            csv_cleaner.clean_csv_file(file, replace)

        if file["name"].endswith('.tsv'):
            tsv_cleaner.clean_tsv_file(file, replace)

        excel_extensions = [".xlsx", ".xlsm", ".xltx", ".xltm"]
        if any(file["name"].endswith(ext) for ext in excel_extensions):
            excel_cleaner.clean_excel_file(file, replace)

        if file["name"].endswith('.json') or file["name"].endswith('.jsonl'):
            json_cleaner.clean_json_file(file, replace)


def ask_clean_file():
    """
    Asks the user if he wants to clean the file.

    Args:
        None.

    Returns:
        bool: True if the user wants to clean the file, False otherwise.
        bool: True if the user wants to replace the file, False otherwise.
    """
    ask_clean = input("Do you want to clean this file? (yes/no): ")
    while ask_clean.lower() not in ("yes", "no"):
        ask_clean = input("Please enter either 'yes' or 'no': ")
    if ask_clean.lower() == "yes":

        replace_file = input(
            "Do you want to replace the file? (yes/no): ")
        while replace_file.lower() not in ("yes", "no"):
            replace_file = input("Please enter either 'yes' or 'no': ")
        if replace_file.lower() == "yes":

            replace_file_2 = input(
                "Are you sure you want to replace the file? (yes/no): ")
            while replace_file_2.lower() not in ("yes", "no"):
                replace_file_2 = input(
                    "Please enter either 'yes' or 'no': ")
            if replace_file_2.lower() == "yes":
                return True, True
            else:
                return True, False
        else:
            return True, False
    else:
        return False, False
