"""Core function to base64 encode and decode data"""
from typing import Dict

__contracts__ = ["soft_fail"]


async def base64encode(hub, data: str) -> Dict:
    """Applies Base64 encoding to a string.

    Args:
      data(str):
        The string data which will be encoded.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": list, "ret": None|dict}

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec core.encoding.base64encode data=test_data

        Using in a state:

        .. code-block:: yaml

            Idem-state-name:
              exec.run:
                - path: core.encoding.base64encode
                - kwargs:
                    data: test_data

    """
    hub.log.warning(
        "core.encoding.base64encode Deprecated, use 'core.encoder.base64.encode'"
    )
    return hub.exec.core.encoder.base64.encode(data)


async def base64decode(hub, encoded_data: str) -> Dict:
    """Decode string containing a Base64 character sequence to the original string.

    Args:
      encoded_data(str):
        The encoded data for decoding.

     Returns:
        .. code-block:: python

            {"result": True|False, "comment": list, "ret": None|dict}

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec core.encoding.base64decode encoded_data=dGVzdF9kYXRh

        Using in a state:

        .. code-block:: yaml

            Idem-state-name:
              exec.run:
                - path: core.encoding.base64decode
                - kwargs:
                    encoded_data: dGVzdF9kYXRh

    """
    hub.log.warning(
        "core.encoding.base64decode Deprecated, use 'core.encoder.base64.decode'"
    )
    return hub.exec.core.encoder.base64.decode(encoded_data)
