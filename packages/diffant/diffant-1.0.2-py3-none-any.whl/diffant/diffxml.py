"""" first effort from chat-gpt quote:
Please note that this is a simple example and may not handle all XML
intricacies like attributes, namespaces or comments. It also assumes
that your XML structure does not contain mixed content (i.e., text
and child elements interspersed). Depending on your use case, you
 may need a more complex or robust XML to dict conversion function.
"""

import xml.etree.ElementTree as ET
from typing import Any, Dict
from xml.etree.ElementTree import Element

from diffant import exceptions
from diffant.diffabc import DiffABC


class DiffXML(DiffABC):
    """Class to produce the structured diff of XML files."""

    def parse_file(self, file: str) -> Any:
        """
        Given an XML file, return a dictionary corresponding to the file contents.

        Args:
            file (str): file to parse

        Raises:
            exceptions.ParseError: If the ElementTree library tells us we
            failed to parse

        Returns:
            Any: corresponding to the XML
        """
        try:
            tree = ET.parse(file)
            # get the root element of XML
            root = tree.getroot()
            result = self._xml_to_dict(root)
        except ET.ParseError as exc:
            msg = f"Failed to parse: {file}\n {str(exc)}"
            raise exceptions.ParseError(msg) from exc

        return result

    def _xml_to_dict(self, elem: Element) -> Dict[str, Any]:
        """
        Convert an XML element to a Python le.

        Args:
            elem (xml.etree.ElementTree.Element): XML element

        Returns:
            dict: Python dictionary representation of the XML element
        """
        dict_value: Dict[str, Any] = {}
        for child in elem:
            child_data = self._xml_to_dict(child)
            if child.tag in dict_value:
                if isinstance(dict_value[child.tag], list):
                    dict_value[child.tag].append(child_data)
                else:
                    dict_value[child.tag] = [dict_value[child.tag], child_data]
            else:
                dict_value[child.tag] = child_data
        return dict_value
