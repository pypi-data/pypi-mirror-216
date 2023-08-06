"""
holds class to parse yaml files
"""
from typing import Any

import yaml

from diffant import exceptions
from diffant.diffabc import DiffABC


class DiffYML(DiffABC):
    """class to produce the structured diff of yml files."""

    def parse_file(self, file: str) -> Any:
        """Given a yaml file, return a dict corresponding to the file contents

        Args:
            file (str): file to parse

        Raises:
            exceptions.ParseError: If the yaml library tells us we failed to parse

        Returns:
            Dict[str, Any]:  corresponding to the yaml
        """
        with open(file, "r", encoding="utf-8") as fh:
            try:
                result = yaml.safe_load(fh)
            except yaml.YAMLError as exc:
                msg = f"failed to parse: {file}\n {str(exc)}"
                raise exceptions.ParseError(msg) from exc

        if not isinstance(result, dict):
            msg = f"failed to parse: {file}\n "
            msg += "no key/values delimted with ':' found in contents:\n"
            msg += str(result)
            raise exceptions.ParseError(msg)
        return result
