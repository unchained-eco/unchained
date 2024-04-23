from unchained.http import Request, Response


async def hello(req: Request) -> Response:
    return Response("Hello, world!")
