import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from isamples_sesar.sample import Sample
from isamples_sesar.classification import Classification
from isamples_sesar.country import Country
from isamples_sesar.launch_type import Launch_Type
from isamples_sesar.nav_type import Nav_Type
from isamples_sesar.sample_additional_name import Sample_Additional_Name
from isamples_sesar.sample_type import Sample_Type
from isamples_sesar.sesar_user import Sesar_User
from isamples_sesar.sqlmodel_database import (
    get_sample_with_id,
    get_sample_with_igsn
)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True
    )
    SQLModel.metadata.create_all(engine)
    sample = Sample(
            sample_id=1,
            origin_sample_id=2,
            sample_type_id=1,
            igsn="10.58052/IE123TEST",
            igsn_prefix="IE123",
            name="Test Sample",
            classification_id=1,
            top_level_classification_id=2,
            country_id=1,
            nav_type_id=1,
            launch_type_id=1,
            cur_registrant_id=1,
            orig_owner_id=1,
            cur_owner_id=1
        )
    parent_sample = Sample(
            sample_id=2,
            sample_type_id=1,
            igsn="10.58052/IE123PARENT",
            igsn_prefix="IE123",
            name="Parent Sample"
        )
    sample_type = Sample_Type(
        sample_type_id=1,
        name="Test Sample Type",
        parent_sample_type_id=2
    )
    parent_sample_type = Sample_Type(
        sample_type_id=2,
        name="Test Parent Sample Type"
    )
    sample_additional_name = Sample_Additional_Name(
        sample_additional_name_id=1,
        sample_id=1,
        name="Another name"
    )
    nav_type = Nav_Type(
        nav_type_id=1,
        name="Test Nav Type",
        description="A type of navigation"
    )
    launch_type = Launch_Type(
        launch_type_id=1,
        name="Test Launch Type",
        description="A type of launch"
    )
    country = Country(
        country_id=1,
        name="Wakanda"
    )
    classification = Classification(
        classification_id=1,
        parent_classification_id=2,
        name="Child classification"
    )
    parent_classification = Classification(
        classification_id=2,
        name="Parent classification"
    )
    sample_owner = Sesar_User(
        sesar_user_id=1,
        fname="Owner",
        lname="Owner"
    )
    with Session(engine) as session:
        session.add(sample)
        session.add(parent_sample)
        session.add(sample_type)
        session.add(parent_sample_type)
        session.add(sample_additional_name)
        session.add(nav_type)
        session.add(launch_type)
        session.add(country)
        session.add(classification)
        session.add(parent_classification)
        session.add(sample_owner)
        session.commit()
        yield session


def test_get_sample_with_id_sample(session: Session):
    test_id = 1

    shouldnt_be_none = get_sample_with_id(session, test_id)
    assert shouldnt_be_none is not None
    assert shouldnt_be_none.sample_id is not None
    assert test_id == shouldnt_be_none.sample_id


def test_get_sample_with_igsn_sample(session: Session):
    test_igsn = "10.58052/IE123TEST"

    shouldnt_be_none = get_sample_with_igsn(session, test_igsn)
    assert shouldnt_be_none is not None
    assert shouldnt_be_none.igsn is not None
    assert test_igsn == shouldnt_be_none.igsn


def test_sample_relationships(session: Session):
    sample = get_sample_with_id(session, 1)
    parent_sample = get_sample_with_id(session, 2)

    if sample:
        if sample.parent:
            assert sample.parent.name == "Parent Sample"
        if parent_sample and parent_sample.children:
            assert parent_sample.children[0].name == "Test Sample"
        if sample.country:
            assert sample.country.name == "Wakanda"
        if sample.sample_type:
            assert sample.sample_type.name == "Test Sample Type"
            if sample.sample_type.parent_sample_type:
                assert sample.sample_type.parent_sample_type.name == "Test Parent Sample Type"
        if sample.classification:
            assert sample.classification.name == "Child classification"
            if sample.classification.parent_classification:
                assert sample.classification.parent_classification.name == "Parent classification"
        if sample.top_level_classification:
            assert sample.top_level_classification.name == "Parent classification"
        if sample.cur_owner:
            assert sample.cur_owner.fname == "Owner"
        if sample.nav_type:
            assert sample.nav_type.name == "Test Nav Type"
        if sample.launch_type:
            assert sample.launch_type.name == "Test Launch Type"
        if sample.additional_names:
            assert sample.additional_names[0].name == "Another name"
