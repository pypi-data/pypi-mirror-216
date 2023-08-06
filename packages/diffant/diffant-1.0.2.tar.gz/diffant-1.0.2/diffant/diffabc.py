"""
Holds the abstract base class with most of the implemention for comparing
structured configuration files.
"""

import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from diffant import exceptions, nested


@dataclass
class DiffABC(ABC):
    """
    This class is the abstract base class that does the bulk of the work
    of calculating the diff between structured config files in a directory

    It is sub classed by DiffIni, DiffJson, DiffXml, DiffYaml , etc

    Attributes:
    -----------
    _config_dir : str
        The directory holding configuration files we are going to compare

    _config_files : List[str]
        The list of files to parse/compare.

    _files_type : str
        The type of config files. Can be 'ini', 'json', 'yaml'
        SEE ALSO: main.py:DIFF_MAPPING

    _flat_recs : Dict[str, Dict]
        flattening of nested structurres,  to a ':' delimited key pointing to a dict
        with the possible values for that key as keys pointing to a list of files
        containing that key/value pair
        {
            'root:sub_key:sub_sub_key': {
                'values': {
                    'red': ['/path/to/file01.json', '/path/to/jfile02.json'],
                    'purple': ['/path/to/file04.json', '/path/to/jfile05.json']
                }
            },
            ...
        }

    _parsed_file_recs : List[Dict[str, Any]]
        List of dicts, where each dict has filename and parsed contents of that
        file
        Example:
        [
            {
                "filename": "/path/to/jason_file.json"
                "parsed_content":  <content parsed to a python dict>
            }
        ]
    """

    _config_dir: str = ""
    _config_files: List[str] = field(default_factory=list)
    _files_type: str = ""
    _flat_recs: Dict[str, Dict[str, Dict[str, List[str]]]] = field(default_factory=dict)
    _parsed_file_recs: List[Dict[str, Any]] = field(default_factory=list)
    _report: str = ""

    @property
    def report(self) -> str:
        """geter for _report

        Returns:
            str: _report , the string containing human friendly diff between
                           config files _
        """
        return self._report

    def calc(self, config_dir: str, files_type: str) -> None:
        """Given a directory of structured configuration files , calculate
          their differences

        Args:
            config_dir (str):   Dir containing configuration files
            files_type (str):   type/ file extenstion of files in directory examples:
                                json, ini , yml, xml
        """
        self._config_dir = config_dir
        self._files_type = files_type
        try:
            self._get_config_files()
        except (FileNotFoundError, NotADirectoryError) as exc:
            msg = f"FATAL: {type(exc).__name__}: {str(exc)}"
            print(msg, file=sys.stderr)
            sys.exit(os.EX_DATAERR)

        try:
            self._parse_config_files()
        except exceptions.FatalButExpectedError as exc:
            msg = f"FATAL: {type(exc).__name__}: {str(exc)}"
            print(msg, file=sys.stderr)
            sys.exit(os.EX_DATAERR)

        self._create_flat_recs()
        self._add_missing_keys_to_flat_recs()
        self._remove_no_diff_from_flat_recs()
        self._set_report()

    def _get_config_files(self) -> None:
        """Retrieve a sorted list of structured config  files from a dir.
        Raises:
            FileNotFoundError: If there are no config files in input directory
        """
        config_dir_path = Path(self._config_dir)
        config_paths = config_dir_path.glob(f"*.{self._files_type}")

        self._config_files = [str(x) for x in config_paths]
        if not self._config_files:
            msg = f"No {self._files_type} files found in {self._config_dir}"
            raise FileNotFoundError(msg)

    def _parse_config_files(self) -> None:
        """Generate a list of filename/parsed content records from list of files"""
        self._parsed_file_recs = []
        for file in self._config_files:
            rec = {"filename": file, "parsed_content": self.parse_file(file)}
            self._parsed_file_recs.append(rec)

    @abstractmethod
    # Return type Any because stuff like json.loads()
    # has a return value of Any , and we eventually return that
    def parse_file(self, file: str) -> Any:
        """Parse a config file and return correspeonding python dictionary.

        **Must** be overriddpeen by sub class
        Args:
            file (str): The path to the config file to parse

        Returns:
            dict: The parsed data
        """

    def _create_flat_recs(self) -> None:
        """Flattens key/value/filename records from a list of content records."""

        for parsed_rec in self._parsed_file_recs:
            keys, values = self._flatten_item(
                parent="", data=parsed_rec["parsed_content"]
            )
            for key, value in zip(keys, values):
                if key not in self._flat_recs:
                    self._flat_recs[key] = {}

                if "values" not in self._flat_recs[key]:
                    self._flat_recs[key]["values"] = {value: [parsed_rec["filename"]]}
                else:
                    self._flat_recs[key]["values"].setdefault(value, []).append(
                        parsed_rec["filename"]
                    )

    def _flatten_item(self, parent: str, data: Any) -> Tuple[List[str], List[str]]:
        """Flattens a potentially nested structure.

        Args:
            parent (str): Flattened/stringified version of the parent key
                          structure. Examples:
                - "" (empty string)
                - "root"
            data (Any): The data structure to flatten. It can be a string, integer,
                        float, list, dictionary, or None.

        Returns:
            Tuple[List[str], List[str]]: A tuple containing two unnested, (flat) lists:
                - keys: Flattened key structures. Example:
                    [
                        'appearance:color',
                        'appearance:shape',
                        'digits:0',
                        'digits:1',
                        'digits:2',
                    ]
                - values: Corresponding values for each key. Example:
                    [
                        'red',
                        'square',
                        '0',
                        '3',
                        '22',
                    ]
        """

        if isinstance(data, (bool, float, int, str, type(None))):
            return [f"{parent}"], [str(data)]

        keys = []
        values = []

        if not parent:  # sort everything  recursively only once
            data = nested.sort(data)

        if isinstance(data, dict):
            for key, value in data.items():
                nparent = f"{parent}{key}:"
                nkeys, nvalues = self._flatten_item(parent=nparent, data=value)
                keys.extend(nkeys)
                values.extend(nvalues)

            values_sorted = [x for _, x in sorted(zip(keys, values))]
            keys.sort()
            return (keys, values_sorted)

        if isinstance(data, list):
            for index, value in enumerate(data):
                nparent = f"{parent}{index}:"
                nkeys, nvalues = self._flatten_item(parent=nparent, data=value)
                keys.extend(nkeys)
                values.extend(nvalues)

            values_sorted = [x for _, x in sorted(zip(keys, values))]
            keys.sort()
            return (keys, values_sorted)

        # if not isinstance(rec, (bool,float,dict,int,list,str, type(None))):
        return ([f"parse error:{data}"], [f"type: {type(data)}"])

    def _add_missing_keys_to_flat_recs(self) -> None:
        """
        For each key in self._flat_recs, if a file name from  self.config_files' list
        does not exist in any value record of the key, add the file name to the
        '/*MISSING*/' value record.

        Create the '/*MISSING*/' value record if needed.

        Example:
            Before:
                self._flat_recs = {
                    'root:sub_key:sub_sub_key': {
                        'values': {
                            'red': ['/path/to/file01.json', '/path/to/file02.json'],
                            'purple': ['/path/to/file04.json', '/path/to/file05.json']
                        }
                    }
                }

            After note_missing_keys(['/path/to/file/no_key.json'], flat_recs):
                {
                    'root:sub_key:sub_sub_key': {
                        'values': {
                            'red': ['/path/to/file01.json', '/path/to/file02.json'],
                            'purple': ['/path/to/file04.json', '/path/to/file05.json'],
                            '/*MISSING*/': ['/path/to/file/no_key.json']
                        }
                    }
                }
        """
        unique_files = set(self._config_files)
        for key in self._flat_recs:
            existing_files = self._extract_filenames(self._flat_recs[key]["values"])

            if missing_files := unique_files.difference(existing_files):
                self._flat_recs[key]["values"]["/*MISSING*/"] = sorted(
                    list(missing_files)
                )

    def _extract_filenames(self, value_rec: Dict[str, List[str]]) -> Set[str]:
        """
        Extracts a set of filenames from a dict mapping values to lists of filenames.

        Args:
            value_rec (Dict[str, List[str]]): A dictionary where each key-value pair
                    represents a value and its corresponding list of filenames.

        Returns:
            A set of unique filenames found in the input dictionary.

        Example:
            Input:
                {
                    'red': ['/path/to/file01.json', '/path/to/file02.json'],
                    'purple': ['/path/to/file04.json', '/path/to/file05.json'],
                    '/*MISSING*/': ['/path/to/file/no_key.json']
                }

            Output:
                {'/path/to/file01.json', '/path/to/file02.json', '/path/to/file04.json',
                '/path/to/file05.json', '/path/to/file/no_key.json'}
        """
        result: Set[str] = set()
        for filenames in value_rec.values():
            result.update(filenames)
        return result

    def _remove_no_diff_from_flat_recs(self) -> None:
        """
        Traverses each dictionary in 'flat_recs', removing those that have only a
        single key-value pair in their 'values' dictionary. Because that means
        there is no difference for that key/value between two files

                Example:
            Before:
            {
                'root:sub_key:sub_sub_key': {
                    'values': {
                        'red': ['f01.json', 'f02.json'],
                        'purple': ['f04.json', 'f05.json'],
                        '/*MISSING*/': ['/path/to/file/no_key.json']
                    }
                },
                'root:sub:': {
                    'values': {
                        'zeus':['f01.json','f02.json','f03.json','f04.json','f05.json']
                    }
                }
            }

            After:
            {
                'root:sub_key:sub_sub_key': {
                    'values': {
                        'red': ['f01.json', 'f02.json'],
                        'purple': ['f04.json', 'f05.json'],
                        '/*MISSING*/': ['/path/to/file/no_key.json']
                    }
                }
            }
        """

        self._flat_recs = {
            key: value
            for key, value in self._flat_recs.items()
            if len(value["values"]) != 1
        }

    def _set_report(self) -> None:
        """
        Generate a human-readable string representation of
        the difference between key/values found in config files.

        This method formats a dictionary of key-value pairs and corresponding config
        filenames into a readable string. The  keys follow the pattern
        'key:sub_key:sub_key:', extracted from the original confg file. The inner
        dictionary contains  'values' as keys pointing to a list of filenames where
        the outer key (e.g., 'fruit') can be found.

            Example:
                fruit:  apple
                        tests/sample_input.d/file01.json
                        tests/sample_input.d/file03.json

                        cherry
                        tests/sample_input.d/file02.json

        """
        indent = " " * 4
        self._report = ""
        for key, value_rec in self._flat_recs.items():
            self._report += f"{key}"

            first_value_padding = " " * 2
            remaining_value_padding = " " * len(key) + " " * 2
            filename_padding = " " * len(key) + indent
            for number_of_different_values, value in enumerate(
                value_rec["values"], start=1
            ):
                value_rec["values"][value].sort()
                filenames = "".join(
                    f"{filename_padding}{filename}\n"
                    for filename in value_rec["values"][value]
                )
                padded_value = (
                    f"{remaining_value_padding}{value}"
                    if number_of_different_values > 1
                    else f"{first_value_padding}{value}"
                )
                self._report += f"{padded_value}\n"
                self._report += f"{filenames}\n"
