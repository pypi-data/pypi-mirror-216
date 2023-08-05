"""Core function for string data type."""
from typing import Dict

__contracts__ = ["soft_fail"]


async def replace(hub, data: str, to_replace: str, replace_with: str) -> Dict:
    """Replace all occurrences of the given substring with another substring in the given string.

    Args:
        data(str):
            String in which substring to be replaced

        to_replace(str):
            substring to replace in the given string

        replace_with(str):
            substring to replace with in the given string

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": list, "ret": None|dict}

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec core.string.replace data="test_data" to_replace="test" replace_with="test_updated"

        Using in a state:

        .. code-block:: yaml

            Idem-state-name:
              exec.run:
                - path: core.string.replace
                - kwargs:
                    data: test_data
                    to_replace: test
                    replace_with: test_updated

    """
    result = dict(comment=[], ret=None, result=True)

    if (
        not isinstance(data, str)
        or not isinstance(to_replace, str)
        or not isinstance(replace_with, str)
    ):
        result["result"] = False
        result["comment"].append(f"data for replace should be in string format")
        return result

    replaced_string = data.replace(to_replace, replace_with)

    result["ret"] = {"data": replaced_string}
    return result
