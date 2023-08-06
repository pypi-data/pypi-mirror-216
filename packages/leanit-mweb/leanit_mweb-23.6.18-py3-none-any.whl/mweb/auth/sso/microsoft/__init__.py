from __future__ import annotations

import base64
import hashlib
import logging
import os
import re
from datetime import timedelta

import aiohttp
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from mweb import config
from mweb.auth.sso.base import SessionHandler
from mweb.security.jwt import TokenService

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING, Dict, Tuple

if TYPE_CHECKING:
    pass


async def auth_callback(request: Request, session_handler: SessionHandler):
    code = request.query_params["code"]
    session_id = int(request.query_params["state"])

    session_result = await session_handler.get_session(session_id=str(session_id))
    if not session_result:
        raise HTTPException(status_code=400, detail="Session not found")

    code_verifier = session_result["code_verifier"]

    ms_auth_service = MicrosoftAuthService.get_instance()

    token_data = await ms_auth_service.fetch_token(code=code, code_verifier=code_verifier)
    expires_in = token_data["expires_in"]

    response = RedirectResponse(url="/")

    token_service = TokenService.get_instance()
    expires_delta = timedelta(seconds=expires_in - 60)

    sid = token_service.encode_jwt(data={"sid": session_id}, expires_delta=expires_delta)
    response.set_cookie("sid", sid)
    return response


class MicrosoftAuthService:
    _instance = None

    def __init__(self, client_id: str, client_secret: str, authority: str, redirect_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authority = authority
        self.redirect_url = redirect_url

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            ms_auth_config = config["mweb"]["auth"]["sso"]["microsoft"]

            cls._instance = cls(
                client_id=ms_auth_config["client_id"],
                client_secret=ms_auth_config["client_secret"],
                authority=ms_auth_config["authority"],
                redirect_url=ms_auth_config["redirect_url"],
            )
        return cls._instance

    @classmethod
    def get_code_verifier_and_challange(cls) -> Tuple[str, str]:
        code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
        code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)

        code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
        code_challenge = code_challenge.replace('=', '')

        return code_verifier, code_challenge

    async def build_auth_url(self, session_id: int, session_handler: SessionHandler):
        code_verifier, code_challenge = self.get_code_verifier_and_challange()

        await session_handler.create_async(session_id=session_id, code_verifier=code_verifier, code_challenge=code_challenge)

        auth_uri = f"{self.authority}/oauth2/v2.0/authorize?response_type=code&client_id={self.client_id}&scope=openid&redirect_uri={self.redirect_url}&code_challenge={code_challenge}&code_challenge_method=S256&state={session_id}"
        return auth_uri

    async def fetch_token(self, code: str, code_verifier: str) -> Dict:
        """
        :param code: The code returned from the authorize call
        :param code_verifier: The code verifier used to generate the code challenge
        :return: {'access_token': 'eyJ0e...',
             'expires_in': 3660,
             'ext_expires_in': 3660,
             'id_token': 'eyJ0eXAiOiJKV1QiL...',
             'scope': 'openid profile User.ReadBasic.All email',
             'token_type': 'Bearer'}
        """
        scope = ["User.ReadBasic.All"]

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.authority}/oauth2/v2.0/token",
                                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                                    data={
                                        "client_id": self.client_id,
                                        "scope": " ".join(scope),
                                        "code": code,
                                        "code_verifier": code_verifier,
                                        "redirect_uri": self.redirect_url,
                                        "grant_type": "authorization_code",
                                        "client_secret": self.client_secret,
                                    }) as resp:

                resp.raise_for_status()
                return await resp.json()

    async def fetch_me(self, access_token: str) -> Dict:
        """
        :param access_token:
        :return: {'@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#users/$entity',
             'businessPhones': [],
             'displayName': 'Martin Klapproth',
             'givenName': 'Martin',
             'id': 'ed5accab-31a5-48c7-852c-14aff1393639',
             'jobTitle': None,
             'mail': 'martin.klapproth@makrotan.com',
             'mobilePhone': None,
             'officeLocation': None,
             'preferredLanguage': None,
             'surname': 'Klapproth',
             'userPrincipalName': 'martin.klapproth_makrotan.com#EXT#@martinklapprothmakrotan.onmicrosoft.com'}
        """
        graph_endpoint = 'https://graph.microsoft.com/v1.0/me'

        headers = {
            'Authorization': 'Bearer ' + access_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(graph_endpoint, headers=headers) as resp:
                resp.raise_for_status()
                return await resp.json()
