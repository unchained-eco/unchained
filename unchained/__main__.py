from unchained.core.applications import Unchained

if __name__ == "__main__":
    app = Unchained()
    app.setup_cli()

    app.execute_command_from_argv()
