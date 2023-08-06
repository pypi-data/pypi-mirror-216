import unittest
from unittest.mock import AsyncMock, patch
from typing import Dict

from mweb.auth.sso.microsoft import MicrosoftAuthService
from mweb.auth.sso.base import SessionHandler


class TestMicrosoftAuthService(unittest.TestCase):
    @patch('MicrosoftAuthService.get_code_verifier_and_challange')
    async def test_build_auth_url(self, mock_get_code_verifier_and_challange):
        # Create a mock object for the session_handler parameter
        mock_session_handler = AsyncMock(spec=SessionHandler)

        # Set up the return values for the mocked methods
        mock_get_code_verifier_and_challange.return_value = ("test_verifier", "test_challenge")

        # Create a MicrosoftAuthService object with test values for the constructor parameters
        ms_auth_service = MicrosoftAuthService(client_id="test_id", client_secret="test_secret", authority="https://test_authority.com", redirect_url="https://test_redirect.com")

        # Call the build_auth_url method with the mocked session_handler parameter and a test session_id value
        auth_uri = await ms_auth_service.build_auth_url(session_id=12345, session_handler=mock_session_handler)

        # Assert that the expected methods were called with the correct arguments
        mock_session_handler.create_async.assert_called_once_with(id=12345, code_verifier="test_verifier", code_challenge="test_challenge")

        # Assert that the returned auth_uri has the expected value
        expected_auth_uri = "https://test_authority.com/oauth2/v2.0/authorize?response_type=code&client_id=test_id&scope=openid&redirect_uri=https://test_redirect.com&code_challenge=test_challenge&code_challenge_method=S256&state=12345"
        self.assertEqual(auth_uri, expected_auth_uri)

if __name__ == '__main__':
    unittest.main()
