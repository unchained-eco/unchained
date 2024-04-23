"""
run module for jasmine
"""

import os
import sys
import warnings


def main() -> None:
    os.environ.setdefault("UNCHAINED_SETTINGS_MODULE", "jasmine.settings")
    try:
        from unchained.core.applications import Unchained

        unchained = Unchained()
        unchained.setup()
    except ImportError:
        warnings.warn("Could not import unchained. Did you forget to install it?")
        sys.exit(1)

    except Exception as e:
        warnings.warn(f"An error occurred: {e}")
        sys.exit(1)

    unchained.execute_command_from_argv()


if __name__ == "__main__":
    main()
