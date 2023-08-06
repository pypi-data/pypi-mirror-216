"""
    custom exceptions used by diffant
"""


class FatalButExpectedError(Exception):
    """
    We can't recover from failing these input valdidations,
    but we can provide info so the user can correct them.
    We also want to avoid dumping stack as these are not
    programming errors and a stack dump won't make a clearer
    error for the user
    """


class ParseError(FatalButExpectedError):
    """We failed to parse the json/ini whatever file.

    Args:
        FatalButExpectedError : base class
    """


class InputDirContentsError(FatalButExpectedError):
    """We were passed a directory with contents we can't read unambigiously"""
