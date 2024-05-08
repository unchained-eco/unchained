from unchained.apps import AppConfig as _AppConfig


class AppConfig(_AppConfig):
    def ready(self) -> None:
        pass
