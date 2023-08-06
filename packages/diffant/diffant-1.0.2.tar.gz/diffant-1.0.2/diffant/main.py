"""
Contents:
    the main() entry point for the diffant script
    with associated functions and constants
"""
import argparse
import os
import sys
from pathlib import Path
from typing import Dict, Type

from diffant import exceptions
from diffant.diffabc import DiffABC
from diffant.diffini import DiffIni
from diffant.diffjson import DiffJson
from diffant.diffyml import DiffYML

# map file types: 'ini' to class to process that type: IniDiff
DIFF_MAPPING: Dict[str, Type[DiffABC]] = {
    "ini": DiffIni,
    "json": DiffJson,
    "yml": DiffYML,
}


def main() -> bool:
    """main as is tradition

    Returns:
        bool: mainly for unit testing _
    """
    try:
        input_dir = get_input_dir()
        files_type = get_config_files_type(input_dir)
        differ = create_differ(mapping=DIFF_MAPPING, file_type=files_type)
    except exceptions.FatalButExpectedError as exc:
        msg = f"FATAL: {type(exc).__name__}: {str(exc)}"
        print(msg, file=sys.stderr)
        sys.exit(os.EX_DATAERR)

    differ.calc(config_dir=input_dir, files_type=files_type)
    print(differ.report)
    return True


def get_input_dir() -> str:
    """Retrieve and validate input of directory with  config files
       from command-line arguments using argparse.

    Returns:
        str: The input directory.

    Raises:
        FileNotFoundError: If the supplied directory does not exist.
        NotADirectoryError: If the supplied path is not a directory.
        SystemExit (via argparse): If the required argument is not provided.
    """
    parser = argparse.ArgumentParser(description="JSON file comparison tool.")
    parser.add_argument(
        "input_dir",
        type=str,
        help="Path to dir containing config files of the same type.",
    )

    args = parser.parse_args()
    input_dir = str(args.input_dir)

    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"The directory '{input_dir}' does not exist")

    if not os.path.isdir(input_dir):
        raise NotADirectoryError(f"'{input_dir}' is not a directory")

    return input_dir


def get_config_files_type(input_dir: str) -> str:
    """Return extension of the files in the directory

    Args:
        input_dir (str): dir with configuration files we want the extension of

    Raises:
        exceptions.InputDirContentsError:
        raise this If there are sub directories, files without
        extensions or more than 1 type of file

    Returns:
        str: examples: 'json', 'yml', 'ini'
    """
    path = Path(input_dir)

    file_extensions = set()
    subdirs = []
    no_ext_files = []

    for item in path.glob("*"):
        if item.is_dir():
            subdirs.append(item)
        elif item.suffix == "":
            no_ext_files.append(item)
        else:
            file_extensions.add(item.suffix)

    errors = []
    if subdirs:
        errors.append(f"Sub-directories not allowed in input dir: {input_dir}")
    if no_ext_files:
        errors.append(f"Files without extensions not allowed in input dir: {input_dir}")
    if len(file_extensions) > 1:
        msg = f"Expected 1 file extension in {input_dir} found {list(file_extensions)}"
        errors.append(msg)

    if errors:
        raise exceptions.InputDirContentsError("\n".join(errors))

    extension = next(iter(file_extensions))  # Get the first and only item from the set

    return str(extension[1:])  # remove the leading dot from the extension


def create_differ(mapping: Dict[str, Type[DiffABC]], file_type: str) -> DiffABC:
    """ Return the Diff class we want to instanciate.

    Args:
        mapping (Dict): map file type strings to Diff* classes
        file_type (str): extension / file type examples: 'json', 'ini'

    Raises:
        exceptions.InputDirContentsError:
            if we dont have sub class that can parse the presented file type

    Returns:
        DiffABC: A sub class of DiffABC that can parse files of type: file_type
    """
    diff_class = mapping.get(file_type)
    if diff_class is None:
        supported_types = " ".join(mapping.keys())
        msg = f"unspported file type: '{file_type}'\nsupported types: {supported_types}"
        raise exceptions.InputDirContentsError(msg)
    return diff_class()
