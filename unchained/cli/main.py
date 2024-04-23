import click


@click.command()
def start_project():
    print("start_project")


@click.group()
def main():
    pass


main.add_command(start_project)


if __name__ == "__main__":
    main()
