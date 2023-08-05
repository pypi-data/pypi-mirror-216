"""Core function to base64 encode and decode data"""
import base64
from typing import Any
from typing import Dict

__contracts__ = ["soft_fail"]


async def encode(hub, data: str) -> Dict[str, Any]:
    """
    Applies Base64 encoding to a string.

    Args:
      data(str):
        The string data which will be encoded.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": list, "ret": None|dict}

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec core.encoder.base64.encode data=test_data

        Using in a state:

        .. code-block:: yaml

            Idem-state-name:
              exec.run:
                - path: core.encoder.base64.encode
                - kwargs:
                    data: test_data
    """
    result = dict(comment=[], ret=None, result=True)
    if not data:
        result["result"] = False
        result["comment"].append(f"data for base64encode is empty")
        return result
    try:
        b64encode_str = base64.b64encode(data.encode()).decode()
        result["comment"].append(f"base64Encode succeeded")
        result["ret"] = {"data": b64encode_str}
    except UnicodeError as e:
        hub.log.debug(f"base 64 encoding failed {e}")
        result["result"] = False
        result["comment"] = (f"{e.__class__.__name__}: {e}",)

    return result


async def decode(hub, encoded_data: str) -> Dict[str, Any]:
    """
    Decode string containing a Base64 character sequence to the original string.

    Args:
      encoded_data(str):
        The encoded data for decoding.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": list, "ret": None|dict}

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec core.encoder.base64.decode encoded_data=dGVzdF9kYXRh

        Using in a state:

        .. code-block:: yaml

            Idem-state-name:
              exec.run:
                - path: core.encoder.base64.decode
                - kwargs:
                    encoded_data: dGVzdF9kYXRh

    """
    result = dict(comment=[], ret=None, result=True)
    if not encoded_data:
        result["result"] = False
        result["comment"].append(f"encoded_data for base64decode is empty")
        return result
    try:
        base64decode_str = base64.b64decode(encoded_data.encode()).decode()
        result["comment"].append(f"base64decode succeeded")
        result["ret"] = {"data": base64decode_str}
    except UnicodeError as e:
        hub.log.debug(f"base 64 decoding failed {e}")
        result["result"] = False
        result["comment"] = (f"{e.__class__.__name__}: {e}",)

    return result
