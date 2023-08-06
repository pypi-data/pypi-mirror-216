from tqdm import tqdm

from reader import csv_reader, excel_reader, json_reader, tsv_reader


def process_files(files, deep_search=False, wide_search=False):
    """
    Initiates the process of analyzing the files.

    Args:
        files (dict): The files to analyze.
        deep_search (bool): If true, the content of the files will be analyzed.
        wide_search (bool): If true, all the tables or sheets will be analyzed.

    Returns:
        dict: The result of analyzing the files.
    """
    repositories = files["repositories"]
    number_of_repositories = len(repositories)

    if number_of_repositories > 1:
        print(f"\t{number_of_repositories} repositories found to have dataset files")

    result = {"repositories": []}

    for index in range(number_of_repositories):
        repository = repositories[index]

        if number_of_repositories > 1:
            print(
                f"\nAnalyzing repository ({index+1}/{number_of_repositories}) {repository['name']}:")
        else:
            print(f"\nAnalyzing repository {repository['name']}:")

        result_repository = {"name": repository["name"]}

        result_files = []
        result_errors = []

        pbar = tqdm(repository["files"],
                    desc="Analyzing files", ncols=300, unit=" file", ascii=' █', bar_format="\tAnalyzing file {n_fmt}/{total_fmt} |{bar:20}| f:{desc}")
        for file in pbar:
            pbar.set_description(file[-50:])

            result_file, result_error = read_file(
                file, deep_search, wide_search)
            if result_file != None:
                result_files.append(result_file)
            if result_error != None:
                result_errors.append(result_error)

        if len(result_files) != 0:
            result_repository["files"] = result_files
        if len(result_errors) != 0:
            result_repository["errors"] = result_errors

        # Only add repository if it has files with errors
        if len(result_repository) != 1:
            result["repositories"].append(result_repository)

    if len(result['repositories']) == 0:
        print("\nYour files are clean!")
        return None

    return result


def read_file(file, deep_search=False, wide_search=False):
    """
    Analyzes the file.

    Args:
        file (str): The file to analyze.
        deep_search (bool): If true, the content of the files will be analyzed.
        wide_search (bool): If true, all the tables or sheets will be analyzed.

    Returns:
        dict: The result of analyzing the file.
    """
    if file.endswith('.csv'):
        result_file, result_error = csv_reader.read_csv_file(file, deep_search)
        return result_file, result_error

    if file.endswith('.tsv'):
        result_file, result_error = tsv_reader.read_tsv_file(file, deep_search)
        return result_file, result_error

    excel_extensions = [".xlsx", "xlsm", "xltx", "xltm"]
    if any(file.endswith(ext) for ext in excel_extensions):
        result_file, result_error = excel_reader.read_excel_file(
            file, deep_search, wide_search)
        return result_file, result_error

    if file.endswith('.json') or file.endswith('.jsonl'):
        result_file, result_error = json_reader.read_json_file(
            file, deep_search)
        return result_file, result_error

    return None, None
