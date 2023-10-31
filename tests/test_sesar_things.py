from sqlmodel import Session
from isamples_sesar.sesar_adapter import SESARItem
from scripts.sesar_things import load_sesar_entries
from isb_web.sqlmodel_database import all_thing_primary_keys  # type: ignore


def test_sesar_things_saved(sesar_session: Session, isb_session: Session):
    # first check that the isb thing table is empty
    no_keys_yet = all_thing_primary_keys(isb_session, SESARItem.AUTHORITY_ID)
    assert no_keys_yet == {}

    expected_keys = {
        '10.60471/ODP01LAMY': 1,
        '10.60471/ODP02Q1IZ': 2,
        '10.58052/EOI00002H': 3,
        '10.58052/IEDUT103B': 4,
        '10.58052/IEJEN0040': 5,
        '10.58052/IERVTNTEZ': 6,
        '10.58052/IERVTL1I7': 7,
        '10.58052/IEEJR000M': 8
    }
    # add sesar things to isb
    load_sesar_entries(sesar_session, isb_session)
    # check things exist
    test_keys = all_thing_primary_keys(isb_session, SESARItem.AUTHORITY_ID)
    assert test_keys == expected_keys
