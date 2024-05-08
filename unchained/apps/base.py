import typing as t
import warnings
from pathlib import Path

from unchained.types import AppCommand
from unchained.utils.module_loading import import_string


class AppConfigProtocol(t.Protocol):
    name: str
    commands: t.Sequence[AppCommand]

    def ready(self) -> None: ...


class AppConfig(AppConfigProtocol):
    def __init__(self):
        self._ready = False

    def setup(self) -> None:
        if self._ready:
            return

        # collect commands
        # list all files in the app/commands
        command_file_list = Path(__file__).parent.joinpath("commands").glob("*.py")

        commands = []
        for command_file in command_file_list:
            # check if BaseCommand is in the file
            path = f"{self.name}.commands.{command_file.stem}"
            try:
                import_string(path)
            except Exception as e:
                warnings.warn(
                    f"Command {command_file.stem} is not a valid command: err {e}"
                )
                continue

            commands.append(AppCommand(name=command_file.stem, import_path=path))

        self.commands = commands

        # TODO
        # collect models/url/admin

        # exec ready method
        self.ready()

        self._ready = True

        return None
