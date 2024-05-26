import os

from unchained.core import Unchained


def test_models_center():
    os.environ["UNCHAINED_SETTINGS_MODULE"] = "unchainedproject.settings"

    unchained = Unchained()

    unchained.setup_models()

    models = unchained.models_center.models
    assert len(models) == 1
