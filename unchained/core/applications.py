import typing as t
from importlib import import_module
from threading import Lock

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import BaseRoute

from unchained.app.registry import AppCenter
from unchained.command import CommandCenter
from unchained.conf import BaseSettings
from unchained.middleware.base import MiddleWareCenter
from unchained.orm.registry import ModelsCenter


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
        self._models_center: ModelsCenter = None
        super().__init__(debug=debug, routes=routes, middleware=middleware)

    @property
    def settings(self) -> BaseSettings:
        if not self._settings:
            self.setup_settings()

        return self._settings

    @property
    def app_center(self) -> AppCenter:
        if not self._app_center:
            self.setup_app()

        return self._app_center

    @property
    def command_center(self) -> CommandCenter:
        if not self._command_center:
            self.setup_commands()

        return self._command_center

    @property
    def models_center(self) -> ModelsCenter:
        if not self._models_center:
            self.setup_models()

        return self._models_center

    def setup_settings(self) -> None:
        self._settings = BaseSettings.setup()

    def setup_app(self):
        self._app_center = AppCenter(self, self.settings.INSTALLED_APPS)
        self._app_center.setup()

    def setup_commands(self):
        self._command_center = CommandCenter(
            unchained=self,
            name=self.settings.PROJECT_NAME,
            commands=self.app_center.commands,
        )
        self._command_center.setup()

    def setup_models(self):
        self._models_center = ModelsCenter(
            unchained=self,
            models=self.app_center.models,
        )

    def setup_middlewares(self):
        # load middlewares
        middleware_center = MiddleWareCenter(self.settings.MIDDLEWARE)
        middleware_center.setup()

        for m in middleware_center.middlewares:
            self.add_middleware(m)

    def setup_routes(self):
        # add routes from settings.ROOT_URLCONF
        root_url_module = import_module(self.settings.ROOT_URLCONF)

        if not hasattr(root_url_module, "urlpatterns"):
            raise ValueError("ROOT_URLCONF should have urlpatterns defined")

        for route in root_url_module.urlpatterns:
            # TODO
            # check if route is a valid route
            # check if route app is installed
            self.router.routes.append(route)

    def setup(self) -> None:
        """
        steps to setup the application
        """

        if self._ready:
            return
        with Lock():
            if self._ready:
                return

            self.setup_settings()
            self.setup_app()

            self.setup_commands()
            self.setup_models()

            self.setup_middlewares()
            self.setup_routes()

            self._ready = True

    def setup_cli(self):
        self._command_center = CommandCenter(unchained=self)
        self._command_center.setup_cli()

    def execute_command_from_argv(self):
        self._command_center.main()
