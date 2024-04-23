import typing as t

from pydantic import BaseModel


class AppCommand(BaseModel):
    name: str
    import_path: str


class AppRoute(BaseModel):
    url: str
    view: t.Callable


class AppInfo(BaseModel):
    name: str
