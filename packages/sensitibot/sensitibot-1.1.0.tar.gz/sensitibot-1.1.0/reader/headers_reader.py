import itertools


def analize_headers(headers):
    """
    Analyzes the headers of a file.

    Args:
        headers (list): The headers of the file.

    Returns:
        list: The headers that may have sensitive information.
    """
    terms = ["email", "phone", "mobile", "iban", "account", "sha", "gpg", "socialsecurity",
             "creditcard", "debitcard", "card", "name", "surname", "lastname", "firstname", "dni",
             "license", "licenses", "lecenseplates", "ip", "ips", "address", "addresses", "gps",
             "coordinate", "coordinates", "location", "password", "latitud", "latitude", "longitud",
             "longitude", "passwords", "secret", "secrets", "key", "hash"]
    suffixes = ["number", "value", "key"]

    combinations = []
    for term, suffix in itertools.product(terms, suffixes):
        combinations.append(term)
        combinations.append(term + ' ' + suffix)
        combinations.append(term + suffix)

    positive_headers = []
    for header in headers:
        header_str = str(header)
        clean_eader = header_str.strip().lower().replace("_", " ").replace("-", " ")
        if clean_eader in combinations:
            positive_headers.append(header)

    return positive_headers
