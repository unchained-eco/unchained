import os
import typing as t

PathLike = t.Union[str, bytes, os.PathLike]
Context = t.Mapping[str, str | int | float]

type CanBeImported = t.Annotated[
    str,
    "split by dot, can be imported by importlib.import_module",
]
type Email = str
type TimeZone = str


type InstalledApp = t.Sequence[CanBeImported]
type Middlewares = t.Sequence[CanBeImported]
