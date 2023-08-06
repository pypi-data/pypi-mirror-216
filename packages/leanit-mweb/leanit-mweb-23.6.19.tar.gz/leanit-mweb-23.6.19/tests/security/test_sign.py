import unittest
from jose.exceptions import JWSError

from mweb.security import sign, unsign


class TestSignUnsign(unittest.TestCase):
    def test_sign_unsign(self):
        secret_key = "my_secret_key"
        value = "my_value"
        signed_value = sign(value, secret_key)
        unsigned_value = unsign(signed_value, secret_key)
        self.assertEqual(unsigned_value, value)

    def test_unsign_invalid_signature(self):
        secret_key = "my_secret_key"
        value = "my_value"
        signed_value = sign(value, secret_key)
        with self.assertRaises(JWSError):
            unsign(signed_value, "wrong_secret_key")

if __name__ == '__main__':
    unittest.main()
