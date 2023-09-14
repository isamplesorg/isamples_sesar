import click
from isamples_sesar.sqlmodel_database import SQLModelDAO, get_sample_with_id


@click.command()
@click.option(
    "-d",
    "--db_url",
    default=None,
    help="SQLAlchemy database URL for storage",
    show_default=True,
)
def main(db_url: str):
    """
    Connects to the SESAR database and converts records to iSamples JSON
    """
    dao = SQLModelDAO(db_url)
    session = dao.get_session()
    # print(f"session is {session}")
    # rows = get_sample_rows(session)
    rows = get_sample_with_id(session, 4942381)
    print(f"rows are {rows}")

    session.close()


"""
Stub main python script, ready to go
"""
if __name__ == "__main__":
    main()
