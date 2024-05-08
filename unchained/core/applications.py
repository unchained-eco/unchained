import typing as t
from importlib import import_module
from threading import Lock

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import BaseRoute

from unchained.apps.registry import AppCenter
from unchained.command import CommandCenter
from unchained.conf import BaseSettings
from unchained.middleware.base import MiddleWareCenter


class Unchained(Starlette):
    version = "0.0.1"

    def __init__(
        self,
        debug: bool = False,
        routes: t.Sequence[BaseRoute] | None = None,
        middleware: t.Sequence[Middleware] | None = None,
    ) -> None:
        self._ready = False
        self._settings: BaseSettings = None
        self._app_center: AppCenter = None
        self._command_center: CommandCenter = None
        super().__init__(debug=debug, routes=routes, middleware=middleware)

    @property
    def settings(self) -> BaseSettings:
        if not self._settings:
            self._settings = BaseSettings.setup()

        return self._settings

    def setup(self) -> None:
        """
        steps to setup the application
            1. load the settings
            2. load all apps
            3. loop through all apps and call the setup method
            4. add internal command and apps' command
        """

        if self._ready:
            return
        with Lock():
            if self._ready:
                return

            # load settings
            self.settings

            # load apps
            self._app_center = AppCenter(self, self.settings.INSTALLED_APPS)
            self._app_center.setup()

            # load commands
            command_mapping: t.Mapping[str, str] = {}
            for app_name, app_config in self._app_center.info.items():
                for command in app_config.commands:
                    if command.name in command_mapping:
                        raise ValueError(
                            f"Command {command.name} is already defined in {command_mapping[command.name]}"
                        )
                    command_mapping[command.name] = command.import_path

            self._command_center = CommandCenter(
                unchained=self, command_mapping=command_mapping
            )
            self._command_center.setup()

            # load middlewares
            middleware_center = MiddleWareCenter(self.settings.MIDDLEWARE)
            middleware_center.setup()

            for m in middleware_center.middlewares:
                self.add_middleware(m)

            # add routes from settings.ROOT_URLCONF
            root_url_module = import_module(self.settings.ROOT_URLCONF)

            if not hasattr(root_url_module, "urlpatterns"):
                raise ValueError("ROOT_URLCONF should have urlpatterns defined")

            for route in root_url_module.urlpatterns:
                self.router.routes.append(route)

            self._ready = True

    def setup_cli(self):
        self._command_center = CommandCenter(unchained=self)
        self._command_center.setup_cli()

    def execute_command_from_argv(self):
        self._command_center.main()
