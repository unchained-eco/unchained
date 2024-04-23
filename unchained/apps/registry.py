import typing as t
from threading import Lock

from unchained.apps.base import AppConfig
from unchained.utils.module_loading import import_string

if t.TYPE_CHECKING:
    from unchained.core.applications import Unchained


class AppCenter:
    def __init__(self, unchained: "Unchained", installed_apps: t.Sequence[str]) -> None:
        self.unchained = unchained
        self.installed_apps = installed_apps

        self._ready = False
        self._loading = False
        self._lock = Lock()
        self._data: t.Mapping[str, AppConfig] = {}

    @property
    def info(self) -> t.Mapping[str, AppConfig]:
        if not self._ready:
            self.setup()

        return self._data

    def setup(self) -> None:
        if self._ready:
            return

        with self._lock:
            if self._ready:
                return

            if self._loading:
                raise RuntimeError("circular dependency detected")

            self._loading = True

            app_list: t.Sequence[AppConfig] = []
            for app_path in self.installed_apps:
                temp_app = self.load_app(app_path)
                app_list.append(temp_app)

            for app in app_list:
                self._data[app.name] = app

            self._ready = True

        return None

    def load_app(self, app_path: str) -> AppConfig:
        if not app_path.endswith(".AppConfig"):
            app_path += "apps.AppConfig"
        app: AppConfig = import_string(app_path)
        app.setup()

        return app
