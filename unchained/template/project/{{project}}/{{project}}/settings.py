"""
settings for project {{project}}
"""

import typing as t

INSTALLED_APPS: t.Sequence[str] = []

MIDDLEWARE: t.Sequence[str] = []

DEBUG: bool = True

ROOT_URLCONF: str = "{{project}}.urls"
