from __future__ import annotations
import logging
from calendar import timegm
from datetime import timedelta, datetime
from mweb import config
from jose import jwt, JWTError
from jose.jwk import construct

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    pass

class TokenService:
    _instance = None

    def __init__(self, public_key_pem: str=None, private_key_pem: str=None):
        self.algorithm = "ES256"

        self.public_key_pem = public_key_pem
        self.private_key_pem = private_key_pem

        if self.public_key_pem:
            self.public_key = construct(self.public_key_pem, algorithm=self.algorithm)
        if self.private_key_pem:
            self.private_key = construct(self.private_key_pem, algorithm=self.algorithm)

    @classmethod
    def get_instance(cls) -> TokenService:
        """
        Returns a singleton instance of TokenService. The JWT keys are read from the config file. They must
        be configured in the mweb.jwt section.

        :return: TokenService
        """
        if cls._instance is None:
            jwt_config = config["mweb"]["jwt"]

            cls._instance = cls(public_key_pem=jwt_config["public_key"], private_key_pem=jwt_config["private_key"])
        return cls._instance

    def encode_jwt(self, data: Dict, expires_delta: timedelta | None = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(seconds=24*3600)

        token_data = data.copy()
        token_data.update({
            "exp": int(timegm(expire.utctimetuple())),
        })

        encoded_jwt = jwt.encode(token_data, self.private_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_jwt(self, access_token: str) -> Dict:
        if not access_token:
            raise JWTError("access token empty or None")

        decoded = jwt.decode(access_token, self.public_key, algorithms=[self.algorithm], options={
            "verify_signature": True,
            "verify_exp": True,
        })
        return decoded
