import importlib
import os
import typing as t

from pydantic import BaseModel

type CanBeImported = str
type Email = str
type TimeZone = str


type InstalledApp = t.Sequence[CanBeImported]
type Middlewares = t.Sequence[CanBeImported]


class BaseSettings(BaseModel):
    INSTALLED_APPS: InstalledApp
    MIDDLEWARE: Middlewares
    DEBUG: bool
    ROOT_URLCONF: str

    @classmethod
    def setup(cls):
        settings_module = os.environ.get("UNCHAINED_SETTINGS_MODULE")
        if not settings_module:
            raise Exception("UNCHAINED_SETTINGS_MODULE environment variable is not set")
        try:
            settingskv = importlib.import_module(settings_module).__dict__
        except ImportError:
            raise ImportError(f"Could not import settings module {settings_module}")

        # get all key-value settings from the settings module
        return cls(**settingskv)
