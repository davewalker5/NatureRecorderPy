"""
Species and category common and scientific naming logic
"""

class Casing:
    TITLE_CASE = "title_case"
    CAPITALISED = "capitalised"


def tidy_string(text, required_case):
    """
    Tidy the case of the specified string and remove duplicate spaces

    :param name: Text string to tidy
    :param required_case: Required casing
    :returns: Tidied text string
    """

    tidied_text = None

    if text:
        match required_case:
            case Casing.TITLE_CASE:
                tidied_text = " ".join(text.split()).title().replace("'S", "'s")
            case Casing.CAPITALISED:
                tidied_text = " ".join(text.split()).capitalize()
            case _:
                tidied_text = text

    return tidied_text
