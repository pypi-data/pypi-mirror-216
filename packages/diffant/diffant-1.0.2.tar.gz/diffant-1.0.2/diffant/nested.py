"""
    Contains the public function sort which recursively sorts a nested
    data structure
"""
from typing import Any, Dict, List, Tuple, Union


def sort(sort_me: Union[Dict[Any, Any], List[Any]]) -> Union[Dict[Any, Any], List[Any]]:
    """Recursively sorts a nested data structure.

    This function acts as a router, deciding whether to sort a list or a dictionary
    based on the type of data structure it receives.

    Args:
        sort_me: The data structure to be sorted. It can contain nested
                 lists and dictionaries.

    Returns:
        The sorted data structure.

    Examples:
        >>> data = [4, 2, [7, 5, 3], 1, {'b': 6, 'a': 8}]
        >>> sorted_data = sort_nested(data)
        >>> sorted_data
        [1, 2, [3, 5, 7], 4, {'a': 8, 'b': 6}]
    """
    if isinstance(sort_me, list):
        return _sort_nested_list(sort_me)
    if isinstance(sort_me, dict):
        return _sort_nested_dict(sort_me)

    return sort_me


def _sort_nested_list(sort_me: List[Any]) -> List[Any]:
    """Recursively sorts a nested list.

    Args:
        sort_me: The list to be sorted. It can contain nested lists and dicts

    Returns:
        The sorted list.
    """
    sort_list_result: List[Any] = []
    sort_list_clues: List[str] = []
    for item in sort_me:
        if isinstance(item, (dict, list)):
            item = sort(item)
        sort_list_result.append(item)

        # we remove " and ' because at times str creates 1
        # and 'c' and 1 < c  but not 1 < "'""
        str_item = str(item).replace('"', "").replace("'", "")
        sort_list_clues.append(str_item)
    return [x for _, x in sorted(zip(sort_list_clues, sort_list_result))]


def _sort_nested_dict(sort_me: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursively sorts a nested dictionary.

    Args:
        sort_me: The dictionary to be sorted. It can contain nested lists and dicts.

    Returns:
        The sorted dictionary.
    """
    sort_dict_result = {}
    sort_dict_clues: List[Tuple[Any, str]] = []
    for key, value in sort_me.items():
        if isinstance(value, (dict, list)):
            value = sort(value)
        sort_dict_result[key] = value

        # we remove " and ' because at times str creates 1
        # and 'c' and 1 < c  but not 1 < "'""
        str_value = str(value).replace('"', "").replace("'", "")
        sort_dict_clues.append((key, str_value))
    sort_dict_clues.sort(key=lambda x: x[1])
    sort_dict_result = {k: sort_dict_result[k] for k, _ in sort_dict_clues}
    return sort_dict_result
