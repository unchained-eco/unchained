import os

from unchained.core import Unchained


def test_middleware_collect():
    os.environ["UNCHAINED_SETTINGS_MODULE"] = "unchainedproject.settings"

    unchained = Unchained()
    unchained.setup_middlewares()

    assert len(unchained.settings.MIDDLEWARE) == 1
