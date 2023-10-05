import pytest
import json
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from isamples_sesar.sesar_transformer import Transformer
from isamples_sesar.sqlmodel_database import (
    get_sample_with_igsn
)


from isamples_sesar.sample import Sample
from isamples_sesar.classification import Classification
from isamples_sesar.country import Country
from isamples_sesar.launch_type import Launch_Type
from isamples_sesar.nav_type import Nav_Type
from isamples_sesar.sample_additional_name import Sample_Additional_Name
from isamples_sesar.sample_type import Sample_Type
from isamples_sesar.sesar_user import Sesar_User


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True
    )
    SQLModel.metadata.create_all(engine)
    sample_1 = Sample(
        sample_id=3661220,
        sample_type_id=15,
        igsn="10.58052/EOI00002H",
        igsn_prefix="EOI",
        external_sample_id="J730-GTHFS-16",
        publish_date="2014-02-14 00:00:00",
        registration_date="2014-02-18 09:32:01.588863",
        name="J730-GTHFS-16",
        current_archive_contact="Lupton_John",
        collection_method="Sampler:Fluid:GTHFS",
        collection_method_descr="GTHFS",
        top_level_classification_id=4251,
        description="HFS gastight. Red-center-9. T=250C",
        latitude=45.946265,
        longitude=-129.983725,
        elevation=-1520,
        elevation_unit="meters",
        primary_location_type="volcano",
        primary_location_name="Axial Seamount",
        location_description="Trevi:Jason Tmax=257.9 C. In the direct flow at this small anhydrite mound (anhydrite knocked over).",
        cruise_field_prgrm="TN300",
        collector="Evans_Leigh",
        collection_start_date="2013-09-14 01:30:00+00:00",
        collection_date_precision="time",
        nav_type_id=6,
        launch_platform_name="Jason II",
        launch_type_id=2,
        cur_registrant_id=318,
        orig_owner_id=318,
        cur_owner_id=318
    )
    sample_2 = Sample(
        sample_id=4280974,
        sample_type_id=21,
        igsn="10.58052/IEDUT103B",
        igsn_prefix="IEDUT",
        external_sample_id="JAM42",
        publish_date="2020-01-01 00:00:00",
        registration_date="2017-09-05 10:07:20.280349",
        name="JAM42",
        current_archive="University of Florida Department of Geological Sciences",
        current_archive_contact="adutton@ufl.edu",
        original_archive="University of Florida Department of Geological Sciences",
        original_archive_contact="adutton@ufl.edu",
        collection_method="Coring>HandHeldCorer",
        classification_id=4262,
        top_level_classification_id=4252,
        description="piece of short core",
        geological_age="Quaternary: MIS 5.5",
        geological_unit="Falmouth Formation",
        latitude=17.88451,
        longitude=-77.77107,
        elevation=1.626,
        elevation_unit="meters",
        primary_location_type="Reef",
        primary_location_name="Limestone Falmouth Formation ",
        locality="Treasure Beach",
        locality_description="Between Buccaneer Villa, Treasure Beach, and Great Bay",
        country_id=107,
        field_name="Pseudodiploria strigosa",
        province="Saint Elizabeth",
        county="Cornwall",
        city="Treasure Beach",
        cruise_field_prgrm="UF Jamaica 2015 Fieldwork",
        collector="Andrea Dutton",
        collector_detail="University of Florida Department of Geological Sciences; adutton@ufl.edu",
        collection_start_date="2015-06-19 00:00:00-04",
        collection_date_precision="day",
        purpose="Paleosea-level",
        vertical_datum="MSL",
        cur_registrant_id=396,
        orig_owner_id=396,
        cur_owner_id=396
    )
    sample_3 = Sample(
        sample_id=4580055,
        sample_type_id=15,
        igsn="10.58052/IEEJR000M",
        igsn_prefix="IEEJRc",
        external_sample_id="16ER6F3",
        publish_date="2021-01-19 16:32:44.894867",
        registration_date="2021-01-19 16:32:44.894867",
        name="16ER6F3",
        current_archive="The University of Texas at Austin",
        current_archive_contact="jdbarnes@jsg.utexas.edu",
        collection_method="Manual>Hammer",
        classification_id=62,
        top_level_classification_id=1,
        latitude=36.461666,
        longitude=-118.583888,
        primary_location_type="Metamorphic aureole",
        primary_location_name="Mineral King; Sequoia National Forest",
        country_id=228,
        field_name="Marble",
        province="California",
        county="Tulare",
        city="Silver City",
        collector="Jade Star Lackey",
        cur_registrant_id=1182,
        orig_owner_id=1182,
        cur_owner_id=1182
    )
    sample_4 = Sample(
        sample_id=4312677,
        sample_type_id=1,
        igsn="10.58052/IEJEN0040",
        igsn_prefix="IEJEN",
        external_sample_id="Goldfin ~20 m moss from 30 cm hummock",
        publish_date="2020-03-09 00:00:00",
        registration_date="2018-03-09 16:17:25.687707",
        name="Goldfin ~20 m moss from 30 cm hummock",
        current_archive="Lamont-Doherty Earth Observatory",
        current_archive_contact="Jonathan E. Nichols",
        top_level_classification_id=4252,
        sample_comment="  small pool near stream 3 ~20 m from stream",
        latitude=60.25455,
        longitude=-149.35756666667,
        primary_location_type="peatland",
        primary_location_name="Gold Fin",
        collector="Miriam Jones",
        collection_start_date="2017-09-01 00:00:00-04",
        collection_date_precision="day",
        cur_registrant_id=520,
        orig_owner_id=520,
        cur_owner_id=520
    )
    sample_5 = Sample(
        sample_id=4369455,
        origin_sample_id=4359908,
        sample_type_id=15,
        igsn="10.58052/IERVTL1I7",
        igsn_prefix="IERVT",
        external_sample_id="0744",
        publish_date="2019-07-11 14:14:54.547176",
        registration_date="2019-07-11 14:14:54.547176",
        name="0744",
        collection_method="Headspace equilibration method",
        top_level_classification_id=4251,
        depth_min=150,
        depth_max=150,
        depth_scale="cm",
        latitude=42.988396,
        longitude=-108.400284,
        primary_location_type="floodplain, aquifer",
        cruise_field_prgrm="SLAC-SFA",
        collector="Zach Perzan",
        collector_detail="zperzan@stanford.edu; Stanford University, Stanford, CA",
        collection_start_date="2019-05-24 00:00:00-04",
        purpose="2018 inundation tracer tests",
        cur_registrant_id=909,
        orig_owner_id=909,
        cur_owner_id=1633
    )
    sample_6 = Sample(
        sample_id=2989112,
        origin_sample_id=1088023,
        sample_type_id=15,
        igsn="10.60471/ODP02Q1IZ",
        igsn_prefix="ODP",
        external_sample_id="Sample 178-1098B-1H-3 (26-27 cm.)",
        publish_date="2010-12-10 20:04:02.866786",
        registration_date="2006-08-11 00:00:00",
        name="Sample 178-1098B-1H-3 (26-27 cm.)",
        current_archive="Integrated Ocean Drilling Program (IODP)",
        current_archive_contact="Curator",
        original_archive="Texas A&M University, Integrated Ocean Drilling Program, College Station, TX, 77845, USA",
        original_archive_contact="Curator",
        description="Janus sample_id: 63151",
        latitude=-64.86194,
        longitude=-64.20799,
        elevation=-1010.6,
        elevation_unit="meters",
        cruise_field_prgrm="ODP Leg 178",
        platform_type="Ship",
        platform_name="Joides Resolution",
        collector="Curator",
        collector_detail="Texas A&M University, Integrated Ocean Drilling Program, College Station, TX, 77845, USA",
        cur_registrant_id=18,
        orig_owner_id=18,
        cur_owner_id=18
    )
    # parent samples, don't need full metadata for tests
    sample_7 = Sample(
        sample_id=4359908,
        sample_type_id=15,
        igsn="10.58052/IERVTNTEZ",
        igsn_prefix="IERVT",
        name="0184"
    )
    sample_8 = Sample(
        sample_id=1088023,
        sample_type_id=5,
        igsn="10.60471/ODP01LAMY",
        igsn_prefix="ODP",
        name="Section 178-1098B-1H-3"
    )
    sample_type_1 = Sample_Type(
        sample_type_id=15,
        name="Individual Sample"
    )
    sample_type_2 = Sample_Type(
        sample_type_id=21,
        name="Cylinder",
        parent_sample_type_id=15
    )
    sample_type_3 = Sample_Type(
        sample_type_id=1,
        name="Grab"
    )
    sample_type_4 = Sample_Type(
        sample_type_id=5,
        name="Core Section"
    )
    sample_additional_name_1 = Sample_Additional_Name(
        sample_additional_name_id=742864,
        sample_id=4369455,
        name="Gas_NTC1-140cm_20190524-H"
    )
    nav_type_1 = Nav_Type(
        nav_type_id=6,
        name="USBL",
        description="Ultra-Short Baseline"
    )
    nav_type_2 = Nav_Type(
        nav_type_id=13,
        name="GPS",
        description="Global Positioning System"
    )
    launch_type_1 = Launch_Type(
        launch_type_id=2,
        name="ROV",
        description="Remotely-Operated Vehicle"
    )
    country_1 = Country(
        country_id=107,
        name="Jamaica"
    )
    country_2 = Country(
        country_id=228,
        name="United States"
    )
    classification_1 = Classification(
        classification_id=4262,
        parent_classification_id=4252,
        name="Macrobiology>Coral",
        description="Macrobiology>Coral"
    )
    classification_2 = Classification(
        classification_id=4252,
        name="Biology",
        description="biology"
    )
    classification_3 = Classification(
        classification_id=4251,
        name="Gas",
        description="gas"
    )
    classification_4 = Classification(
        classification_id=62,
        parent_classification_id=1,
        name="Metamorphic>Meta-Carbonate",
        description="Metamorphic>Meta-Carbonate"
    )
    classification_5 = Classification(
        classification_id=1,
        name="Rock",
        description="Rock Classification"
    )
    sample_owner_1 = Sesar_User(
        sesar_user_id=909,
        fname="SLAC",
        lname="SFA",
        email="zperzan@slac.stanford.edu"
    )
    sample_owner_2 = Sesar_User(
        sesar_user_id=396,
        fname="Andrea",
        lname="Dutton",
        email="dutton3@wisc.edu"
    )
    sample_owner_3 = Sesar_User(
        sesar_user_id=318,
        fname="Andra",
        lname="Bobbitt",
        email="andra.bobbitt@noaa.gov"
    )
    sample_owner_4 = Sesar_User(
        sesar_user_id=520,
        fname="Jonathan",
        lname="Nichols",
        email="jnichols@ldeo.columbia.edu"
    )
    sample_owner_5 = Sesar_User(
        sesar_user_id=18,
        fname="Curator",
        lname="Integrated Ocean Drilling Program (TAMU)",
        email="information@iodp.tamu.edu"
    )
    sample_owner_6 = Sesar_User(
        sesar_user_id=1633,
        fname="Watershed Function SFA",
        lname="Data Team",
        email="wfsfa-data@lbl.gov"
    )
    sample_owner_7 = Sesar_User(
        sesar_user_id=1182,
        fname="Evan",
        lname="Ramos",
        email="ejramos@utexas.edu"
    )
    with Session(engine) as session:
        session.add(sample_1)
        session.add(sample_2)
        session.add(sample_3)
        session.add(sample_4)
        session.add(sample_5)
        session.add(sample_6)
        session.add(sample_7)
        session.add(sample_8)
        session.add(sample_type_1)
        session.add(sample_type_2)
        session.add(sample_type_3)
        session.add(sample_type_4)
        session.add(sample_additional_name_1)
        session.add(nav_type_1)
        session.add(nav_type_2)
        session.add(launch_type_1)
        session.add(country_1)
        session.add(country_2)
        session.add(classification_1)
        session.add(classification_2)
        session.add(classification_3)
        session.add(classification_4)
        session.add(classification_5)
        session.add(sample_owner_1)
        session.add(sample_owner_2)
        session.add(sample_owner_3)
        session.add(sample_owner_4)
        session.add(sample_owner_5)
        session.add(sample_owner_6)
        session.add(sample_owner_7)
        session.commit()
        yield session


@pytest.mark.parametrize("igsn", ["10.58052/EOI00002H",
                                  "10.58052/IEDUT103B",
                                  "10.58052/IEEJR000M",
                                  "10.58052/IEJEN0040",
                                  "10.58052/IERVTL1I7",
                                  "10.60471/ODP02Q1IZ"])
def test_example(session: Session, igsn):
    # get sample and transform it
    sample = get_sample_with_igsn(session, igsn)
    assert sample is not None
    transformed_test_data = Transformer(sample).transform()

    igsn_suffix = igsn.split("/")[1]
    json_file = open("examples/" + igsn_suffix + ".json")
    expected_data = json.load(json_file)
    json_file.close()

    check_id(transformed_test_data, expected_data)
    check_label(transformed_test_data, expected_data)
    check_sample_identifier(transformed_test_data, expected_data)
    check_description(transformed_test_data, expected_data)
    check_context_category(transformed_test_data, expected_data)
    check_material_category(transformed_test_data, expected_data)
    check_specimen_category(transformed_test_data, expected_data)
    check_informal_classification(transformed_test_data, expected_data)
    check_keywords(transformed_test_data, expected_data)
    check_produced_by_id(transformed_test_data, expected_data)
    check_produced_by_label(transformed_test_data, expected_data)
    check_produced_by_description(transformed_test_data, expected_data)
    check_produced_by_feature(transformed_test_data, expected_data)
    check_produced_by_responsibility(transformed_test_data, expected_data)
    check_produced_by_time(transformed_test_data, expected_data)
    check_sampling_site_description(transformed_test_data, expected_data)
    check_sampling_site_label(transformed_test_data, expected_data)
    check_sampling_site_place_name(transformed_test_data, expected_data)
    check_sampling_site_elevation(transformed_test_data, expected_data)
    check_sampling_site_latitude(transformed_test_data, expected_data)
    check_sampling_site_longitude(transformed_test_data, expected_data)
    check_registrant(transformed_test_data, expected_data)
    check_sampling_purpose(transformed_test_data, expected_data)
    check_curation_label(transformed_test_data, expected_data)
    check_curation_description(transformed_test_data, expected_data)
    check_curation_access_constraints(transformed_test_data, expected_data)
    check_curation_location(transformed_test_data, expected_data)
    check_curation_responsibility(transformed_test_data, expected_data)
    check_related_resource(transformed_test_data, expected_data)
    check_authorized_by(transformed_test_data, expected_data)
    check_complies_with(transformed_test_data, expected_data)


def check_id(test_data, expected_data):
    assert test_data["@id"] == expected_data["@id"]


def check_label(test_data, expected_data):
    assert test_data["label"] == expected_data["label"]


def check_sample_identifier(test_data, expected_data):
    assert test_data["sampleidentifier"] == expected_data["sampleidentifier"]


def check_description(test_data, expected_data):
    assert test_data["description"] == expected_data["description"]


def check_context_category(test_data, expected_data):
    assert test_data["hasContextCategory"] == expected_data["hasContextCategory"]
    # assert test_data["hasContextCategoryConfidence"] == expected_data["hasContextCategoryConfidence"]


def check_material_category(test_data, expected_data):
    assert test_data["hasMaterialCategory"] == expected_data["hasMaterialCategory"]
    # assert test_data["hasMaterialCategoryConfidence"] == expected_data["hasMaterialCategoryConfidence"]


def check_specimen_category(test_data, expected_data):
    assert test_data["hasSpecimenCategory"] == expected_data["hasSpecimenCategory"]
    # assert test_data["hasSpecimenCategoryConfidence"] == expected_data["hasSpecimenCategoryConfidence"]


def check_informal_classification(test_data, expected_data):
    assert test_data["informalClassification"] == expected_data["informalClassification"]


def check_keywords(test_data, expected_data):
    assert test_data["keywords"] == expected_data["keywords"]


def check_produced_by_id(test_data, expected_data):
    assert test_data["producedBy"]["@id"] == expected_data["producedBy"]["@id"]


def check_produced_by_label(test_data, expected_data):
    assert test_data["producedBy"]["label"] == expected_data["producedBy"]["label"]


def check_produced_by_description(test_data, expected_data):
    assert test_data["producedBy"]["description"] == expected_data["producedBy"]["description"]


def check_produced_by_feature(test_data, expected_data):
    assert test_data["producedBy"]["hasFeatureOfInterest"] == expected_data["producedBy"]["hasFeatureOfInterest"]


def check_produced_by_responsibility(test_data, expected_data):
    assert test_data["producedBy"]["responsibility"] == expected_data["producedBy"]["responsibility"]


def check_produced_by_time(test_data, expected_data):
    assert test_data["producedBy"]["resultTime"] == expected_data["producedBy"]["resultTime"]


def check_sampling_site_description(test_data, expected_data):
    assert test_data["producedBy"]["samplingSite"]["description"] == \
        expected_data["producedBy"]["samplingSite"]["description"]


def check_sampling_site_label(test_data, expected_data):
    assert test_data["producedBy"]["samplingSite"]["label"] == \
        expected_data["producedBy"]["samplingSite"]["label"]


def check_sampling_site_place_name(test_data, expected_data):
    assert test_data["producedBy"]["samplingSite"]["placeName"] == \
        expected_data["producedBy"]["samplingSite"]["placeName"]


def check_sampling_site_elevation(test_data, expected_data):
    assert test_data["producedBy"]["samplingSite"]["location"]["elevation"] == \
        expected_data["producedBy"]["samplingSite"]["location"]["elevation"]


def check_sampling_site_latitude(test_data, expected_data):
    assert test_data["producedBy"]["samplingSite"]["location"]["latitude"] == \
        expected_data["producedBy"]["samplingSite"]["location"]["latitude"]


def check_sampling_site_longitude(test_data, expected_data):
    assert test_data["producedBy"]["samplingSite"]["location"]["longitude"] == \
        expected_data["producedBy"]["samplingSite"]["location"]["longitude"]


def check_registrant(test_data, expected_data):
    assert test_data["registrant"] == expected_data["registrant"]


def check_sampling_purpose(test_data, expected_data):
    assert test_data["samplingPurpose"] == expected_data["samplingPurpose"]


def check_curation_label(test_data, expected_data):
    assert test_data["curation"]["label"] == expected_data["curation"]["label"]


def check_curation_description(test_data, expected_data):
    assert test_data["curation"]["description"] == expected_data["curation"]["description"]


def check_curation_access_constraints(test_data, expected_data):
    assert test_data["curation"]["accessConstraints"] == expected_data["curation"]["accessConstraints"]


def check_curation_location(test_data, expected_data):
    assert test_data["curation"]["curationLocation"] == expected_data["curation"]["curationLocation"]


def check_curation_responsibility(test_data, expected_data):
    assert test_data["curation"]["responsibility"] == expected_data["curation"]["responsibility"]


def check_related_resource(test_data, expected_data):
    assert test_data["relatedResource"] == expected_data["relatedResource"]


def check_authorized_by(test_data, expected_data):
    assert test_data["authorizedBy"] == expected_data["authorizedBy"]


def check_complies_with(test_data, expected_data):
    assert test_data["compliesWith"] == expected_data["compliesWith"]
