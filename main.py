import click


@click.command()
@click.option(
    "-v",
    "--verbosity",
    default="DEBUG",
    help="Specify logging level",
    show_default=True,
)
def main(verbosity: str):
    """
    Updates existing OpenContext records in a Things db to have their id column stripped of the n2t prefix.
    """
    print(f"Hello World, verbosity is {verbosity}")


"""
Stub main python script, ready to go
"""
if __name__ == "__main__":
    main()
