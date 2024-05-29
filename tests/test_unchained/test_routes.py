from unchained.core import Unchained


def test_route_collect():
    unchained = Unchained()
    unchained.setup_routes()

    routes = unchained.router.routes

    assert len(routes) == 2
