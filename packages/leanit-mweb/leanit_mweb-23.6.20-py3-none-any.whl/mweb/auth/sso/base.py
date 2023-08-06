from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    pass


class SessionHandler:
    """
    Base class. Implement your own session handler.
    """
    async def get_session(self, session_id: str) -> Dict:
        pass

    async def create_async(self, id, **kwargs):
        pass
