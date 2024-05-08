"""

from unchained.http import Request, Response


async def hello(request: Request) -> Response:
    return Response("Hello, world!")

"""
