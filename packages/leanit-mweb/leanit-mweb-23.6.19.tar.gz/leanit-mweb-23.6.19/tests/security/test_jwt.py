import unittest
from datetime import timedelta
from typing import Dict

from mweb.security.jwt import TokenService


class TestTokenService(unittest.TestCase):
    def setUp(self):
        self.public_key_pem = """-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEiM5Nn9CTjdrkcK786DmtwHWgnpVv
mzzuShZ9+j8cBhEyNe5C+RyzxxQTRjnCSGGVxC7LXF19W/SLMAJ2GYT7tg==
-----END PUBLIC KEY-----"""
        self.private_key_pem = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIPnaCOp5+yNp58sLdm+zVOMDcWFp7PXXJoEW1ibOH6EPoAoGCCqGSM49
AwEHoUQDQgAEiM5Nn9CTjdrkcK786DmtwHWgnpVvmzzuShZ9+j8cBhEyNe5C+Ryz
xxQTRjnCSGGVxC7LXF19W/SLMAJ2GYT7tg==
-----END EC PRIVATE KEY-----"""
        self.token_service = TokenService(self.public_key_pem, self.private_key_pem)

    def test_encode_decode_jwt(self):
        data = {"key": "value"}
        expires_delta = timedelta(seconds=24*3600)
        encoded_jwt = self.token_service.encode_jwt(data, expires_delta)
        decoded_jwt = self.token_service.decode_jwt(encoded_jwt)
        self.assertEqual(decoded_jwt["key"], data["key"])

if __name__ == '__main__':
    unittest.main()
