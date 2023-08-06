import unittest

from mweb.auth.sso.microsoft import MicrosoftAuthService


class TestMicrosoftAuthService(unittest.TestCase):
    def test_get_code_verifier_and_challange(self):
        code_verifier, code_challenge = MicrosoftAuthService.get_code_verifier_and_challange()
        self.assertIsInstance(code_verifier, str)
        self.assertIsInstance(code_challenge, str)
        self.assertRegex(code_verifier, '^[a-zA-Z0-9]+$')
        self.assertRegex(code_challenge, '^[a-zA-Z0-9_-]+$')
        self.assertEqual(len(code_challenge), 43)

if __name__ == '__main__':
    unittest.main()