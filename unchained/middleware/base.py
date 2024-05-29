from unchained.protocol import MiddleWareProtocol
from unchained.types import ASGIApp, Receive, Scope, Send

from unchained.http import Request


class BaseMiddleWare(MiddleWareProtocol):
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> ASGIApp:
        if scope["type"] == "http":
            return await self.app(scope, receive, send)

        await self.app(scope, receive, send)
