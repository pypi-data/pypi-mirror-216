import os


def process_local(directory=None):
    """
    Initiates the process of getting the files from the local repository.

    Args:
        directory (str): The directory to search.

    Returns:
        dict: The result of getting the files.
    """
    files = get_files_recursively(directory)

    if files == None:
        print("\nNo dataset files found")
        return None

    return files


def get_files_recursively(directory=None):
    """
    Gets the files from the local directory.

    Args:
        directory (str): The directory to search.

    Returns:
        dict: The files from the local directory.
    """
    if directory == None:
        directory = "./"

    result = {"repositories": [{"name": "local", "files": []}]}

    extensions = [".csv", ".tsv", ".xlsx", "xlsm", "xltx",
                  "xltm", ".json", ".jsonl"]

    print(f'Searching directory {directory}:')

    for root, _, files in os.walk(directory):
        for filename in files:

            if any(filename.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, filename)
                result["repositories"][0]["files"].append(filepath)

    # Only return the result if there are files of any type
    if len(result["repositories"][0]["files"]) == 0:
        return None

    return result
