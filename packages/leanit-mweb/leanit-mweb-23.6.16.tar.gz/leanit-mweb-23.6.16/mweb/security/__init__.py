from __future__ import annotations
import logging

from jose import jws

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

def sign(value: str, secret_key: str) -> str:
    signed = jws.sign(value.encode(), secret_key, algorithm="HS256")
    return signed

def unsign(value: str, secret_key: str) -> str:
    """
    :raises: jose.exceptions.JWSError if the signature is invalid
    :param value:
    :return:
    """
    unsigned = jws.verify(value, secret_key, algorithms=["HS256"])
    return unsigned.decode()
