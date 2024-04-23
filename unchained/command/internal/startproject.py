from pathlib import Path

import unchained
from unchained.command import BaseCommandWithTemplate


class Command(BaseCommandWithTemplate):
    help_text = "Create a new project with template"
    template = Path(unchained.__path__[0], "template/project")
