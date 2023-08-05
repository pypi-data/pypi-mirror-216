"""Core function to encrypt and decrypt message with gpg"""
from typing import Any
from typing import Dict
from typing import List
from typing import Union

import gnupg

__contracts__ = ["soft_fail"]


async def encrypt(
    hub,
    data: str,
    recipients: List[str] = [],
    sign: str = None,
    always_trust: bool = False,
    passphrase: str = None,
    armor: bool = True,
    output: str = None,
    symmetric: Union[bool, str] = False,
    extra_args: List[str] = None,
    public_key: str = None,
) -> Dict[str, Any]:
    """
    Encrypt the message contained in the string 'data'.

    Args:
        data(str):
            The data or message that needs to be encrypted.
        recipients(list[str], Optional):
            A list of key fingerprints for recipients.
        sign(str, Optional):
            Either the Boolean value True, or the fingerprint of a key which is used to sign the encrypted data.
        always_trust(bool, Optional):
            Skip key validation and assume that used keys are always fully trusted.
        passphrase(str, Optional):
            A passphrase to use when accessing the keyrings.
        armor(bool, Optional):
            Whether to use ASCII armor. If False, binary data is produced.
        output(str, Optional):
            The name of an output file to write to.
        symmetric(Union[bool, str], Optional):
            If specified, symmetric encryption is used. In this case, specify recipients as None.
            If True is specified, then the default cipher algorithm (CAST5) is used.
            The cipher-algorithm to use (for example, 'AES256') can also be specified.
        extra_args(list[str], Optional):
            A list of additional arguments to pass to the gpg executable.
            For example, Pass extra_args=['-z', '0'] to disable compression
        public_key(str, Optional):
            Public key of the recipient. This public key will be imported and trusted, if not already.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": list, "ret": None|dict}

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec core.encryption.gpg.encrypt data=test-data-for-encryption

        Using in a state:

        .. code-block:: yaml

            Idem-state-name:
              exec.run:
                - path: core.encryption.gpg.encrypt
                - kwargs:
                    data: test-data-for-encryption

    """
    result = dict(comment=[], ret=None, result=True)
    if not data:
        result["result"] = False
        result["comment"].append("data for gpg_encrypt is empty")
        return result

    try:
        gpg = gnupg.GPG()

        if public_key:
            import_result = await _import_and_trust_keys(gpg=gpg, key_data=public_key)
            if not import_result["result"]:
                result["result"] = False
                result["comment"].append(import_result["comment"])
                return result

        response = gpg.encrypt(
            data=data,
            recipients=recipients,
            sign=sign,
            always_trust=always_trust,
            passphrase=passphrase,
            armor=armor,
            output=output,
            symmetric=symmetric,
            extra_args=extra_args,
        )

        if not response.ok:
            result["result"] = False
            result["comment"].append(response.status)
            return result

        result["comment"].append(response.status)
        # decode is to remove b' prefix
        result["ret"] = {"data": str(response.data.decode("utf-8"))}
    except Exception as e:
        result["result"] = False
        hub.log.debug(f"gpg_encrypt failed {e}")
        result["comment"] = (f"{e.__class__.__name__}: {e}",)

    return result


async def decrypt(
    hub,
    message: str,
    always_trust: bool = False,
    passphrase: str = None,
    output: str = None,
    extra_args: List[str] = None,
    private_key: str = None,
) -> Dict[str, Any]:
    """
    Decrypt the message.

    Args:
        message(str):
            The encrypted message.
        always_trust(bool, Optional):
            Skip key validation and assume that used keys are always fully trusted.
        passphrase(str, Optional):
            A passphrase to use when accessing the keyrings.
        output(str, Optional):
            The name of an output file to write to.
        extra_args(list[str], Optional):
            A list of additional arguments to pass to the gpg executable.
        private_key(str, Optional):
            The private key of the recipient for decryption. This private key will be imported and trusted, if not already.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": list, "ret": None|dict}

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec core.encryption.gpg.decrypt message="This is for decryption test" passphrase="test"

        Using in a state:

        .. code-block:: yaml

            Idem-state-name:
              exec.run:
                - path: core.encryption.gpg.decrypt
                - kwargs:
                    message: This is for decryption test
                    passphrase: test
    """
    result = dict(comment=[], ret=None, result=True)
    if not message:
        result["result"] = False
        result["comment"].append("message for gpg_decrypt is empty")
        return result

    try:
        gpg = gnupg.GPG()
        if private_key:
            import_result = await _import_and_trust_keys(gpg=gpg, key_data=private_key)
            if not import_result["result"]:
                result["result"] = False
                result["comment"].append(import_result["comment"])
                return result

        response = gpg.decrypt(
            message=message,
            always_trust=always_trust,
            passphrase=passphrase,
            output=output,
            extra_args=extra_args,
        )

        if not response.ok:
            result["result"] = False
            result["comment"].append(response.status)
            return result

        result["comment"].append(response.status)
        # decode is to remove b' prefix
        result["ret"] = {"data": str(response.data.decode("utf-8"))}
    except Exception as e:
        result["result"] = False
        hub.log.debug(f"gpg_decrypt failed {e}")
        result["comment"] = (f"{e.__class__.__name__}: {e}",)

    return result


async def _import_and_trust_keys(gpg: gnupg.GPG, key_data: str):
    result = dict(comment=[], ret=None, result=True)
    import_result = gpg.import_keys(key_data=key_data, passphrase=None)
    if not import_result.fingerprints:
        result["result"] = False
        for r in import_result.results:
            result["comment"].append(r["problem"])
            result["comment"].append(r["text"])
        return result

    for fingerprint in import_result.fingerprints:
        # trust these fingerprints, so that decrypt can work
        gpg.trust_keys(fingerprint, "TRUST_ULTIMATE")

    result["comment"].append("successfully imported key_data")
    result["ret"] = {"fingerprints": import_result.fingerprints}
    return result
