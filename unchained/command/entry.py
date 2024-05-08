import typing as t
from pathlib import Path

from click import Group

import unchained
from unchained.utils.module_loading import import_string

if t.TYPE_CHECKING:
    from unchained.core.applications import Unchained


class CommandCenter(Group):
    def __init__(
        self,
        unchained: "Unchained",
        name: str | None = None,
        command_mapping: t.Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(name, None)
        self._command_mapping = command_mapping
        self.unchained = unchained
        self._ready = False

    def add_base_commands(self, include: t.Sequence[str] | None = None) -> None:
        enable_include = include is not None
        include = include or []
        internal_command_dir = Path(unchained.__path__[0] + "/command/internal")
        for command_file in internal_command_dir.glob("*.py"):
            command_name = command_file.stem
            if command_name == "__init__":
                continue
            if enable_include and command_name not in include:
                continue
            command_kls = import_string(
                f"unchained.command.internal.{command_name}.Command"
            )

            escaped = command_name.replace("_", "-")
            self.add_command(command_kls(unchained=self.unchained, name=escaped))

    def setup(self):
        if self._ready:
            return

        for command_name, command_path in self._command_mapping.items():
            command_kls = import_string(command_path)
            self.add_command(command_kls(unchained=self.unchained, name=command_name))
        self.add_base_commands()

        self._ready = True
        return None

    def setup_cli(self):
        self.add_base_commands(include=["startproject"])
