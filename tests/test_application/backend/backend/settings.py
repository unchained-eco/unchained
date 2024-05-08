"""
settings for project backend
"""

import typing as t

# INSTALLED_APPS accept a list of string
# examples:
#   INSTALLED_APPS = ["app1", "app2"]
# equals to
#   INSTALLED_APPS = ["app1.apps.Appconfig", "app2.apps.AppConfig"]
INSTALLED_APPS: t.Sequence[str] = []

MIDDLEWARE: t.Sequence[str] = []

DEBUG: bool = True

ROOT_URLCONF: str = "backend.urls"