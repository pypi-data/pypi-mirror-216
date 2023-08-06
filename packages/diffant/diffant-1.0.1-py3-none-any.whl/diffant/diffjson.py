"""
    class to produce the structured diff of json files.
"""
import json
from typing import Any

from diffant import exceptions
from diffant.diffabc import DiffABC


class DiffJson(DiffABC):
    """class to produce the structured diff of json files."""

    # Return type Any because stuff like json.loads()
    # has a return value of Any , and we eventually return that
    def parse_file(self, file: str) -> Any:
        # def parse_file(self, file: str) -> Any:
        """Given a json file, return a dict corresponding to the file contents

        Args:
            file (str): file to parse

        Raises:
            exceptions.ParseError: If the json library tells us we failed to parse

        Returns:
            Dict[str, Any]:  corresponding to the json
        """
        with open(file, "r", encoding="utf-8") as fh:
            fh_contents = fh.read()
        try:
            result = json.loads(fh_contents)
        except json.decoder.JSONDecodeError as exc:
            msg = f"failed to parse: {file}\n {str(exc)}"
            raise exceptions.ParseError(msg) from exc

        return result
