"""_
_contains class to parse INI files
    _
"""

import configparser
from typing import Any

from diffant import exceptions
from diffant.diffabc import DiffABC


class DiffIni(DiffABC):
    """class to produce the structured diff of ini files."""

    def parse_file(self, file: str) -> Any:
        """Given an ini file, return a dict corresponding to the file contents

        Args:
            file (str): file to parse

        Raises:
            exceptions.ParseError: If the configparser library tells us
            we failed to parse

        Returns:
            Dict[str, Any]:  corresponding to the ini file
        """
        config = configparser.ConfigParser()
        try:
            with open(file, "r", encoding="utf-8") as fh:
                config.read_file(fh)
            # convert to a dict
            result = {s: dict(config.items(s)) for s in config.sections()}
        except configparser.Error as exc:
            msg = f"failed to parse: {file}\n {str(exc)}"
            raise exceptions.ParseError(msg) from exc

        return result
