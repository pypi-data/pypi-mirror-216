import unittest
from unittest.mock import AsyncMock, Mock, patch
from starlette.requests import Request
from starlette.responses import RedirectResponse
from typing import Dict

from mweb.auth.sso.microsoft import auth_callback
from mweb.auth.sso.base import SessionHandler


class TestAuthCallback(unittest.TestCase):
    @patch('MicrosoftAuthService.get_instance')
    @patch('TokenService.get_instance')
    async def test_auth_callback(self, mock_token_service, mock_ms_auth_service):
        # Create mock objects for the session_handler and request parameters
        mock_session_handler = AsyncMock(spec=SessionHandler)
        mock_request = Mock(spec=Request)
        mock_request.query_params = {"code": "test_code", "state": "12345"}

        # Set up the return values for the mocked methods
        mock_session_handler.get_session.return_value = {"code_verifier": "test_verifier"}
        mock_ms_auth_service.fetch_token.return_value = {"expires_in": 3600}
        mock_token_service.encode_jwt.return_value = "test_sid"

        # Call the auth_callback function with the mocked parameters
        response = await auth_callback(mock_request, mock_session_handler)

        # Assert that the expected methods were called with the correct arguments
        mock_session_handler.get_session.assert_called_once_with(session_id="12345")
        mock_ms_auth_service.fetch_token.assert_called_once_with(code="test_code", code_verifier="test_verifier")
        mock_token_service.encode_jwt.assert_called_once_with(data={"sid": 12345}, expires_delta=3540)

        # Assert that the response is a RedirectResponse with the expected cookie value
        self.assertIsInstance(response, RedirectResponse)
        self.assertEqual(response.cookies["sid"], "test_sid")

if __name__ == '__main__':
    unittest.main()
