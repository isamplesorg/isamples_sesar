import click
from isamples_sesar.sqlmodel_database import SQLModelDAO, get_sample_with_igsn
from isamples_sesar.sesar_transformer import Transformer
import json


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

    sample = get_sample_with_igsn(session, "10.58052/EOI00002H")
    sample = get_sample_with_igsn(session, "10.58052/IEDUT103B")
    sample = get_sample_with_igsn(session, "10.58052/IEEJR000M")
    sample = get_sample_with_igsn(session, "10.58052/IEJEN0040")
    sample = get_sample_with_igsn(session, "10.58052/IERVTL1I7")
    sample = get_sample_with_igsn(session, "10.60471/ODP02Q1IZ")
    if sample:
        content = Transformer(sample).transform()
        print(json.dumps(content, indent=4, sort_keys=True, default=str))

    session.close()


"""
Stub main python script, ready to go
"""
if __name__ == "__main__":
    main()
