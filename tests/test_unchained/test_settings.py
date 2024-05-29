import os

from unchained.core import Unchained


def test_setup_settings():
    os.environ["UNCHAINED_SETTINGS_MODULE"] = "unchainedproject.settings"
    unchained = Unchained()

    unchained.setup_settings()

    assert unchained.settings.INSTALLED_APPS == ["unchainedproject.app"]
    assert unchained.settings.MIDDLEWARE == [
        "unchainedproject.middlewares.m1.CustomMiddleware1"
    ]
    assert unchained.settings.DEBUG is True
    assert unchained.settings.ROOT_URLCONF == "unchainedproject.routes"
    assert unchained.settings.PROJECT_NAME == "unchainedproject"
