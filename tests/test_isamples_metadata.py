import pytest
import json
from sqlmodel import Session, create_engine

from isamples_sesar.sesar_transformer import Transformer
from isamples_sesar.sqlmodel_database import (
    get_sample_with_igsn
)


@pytest.fixture
def db_url(request):
    return request.config.getoption("--db-url")


@pytest.fixture(name="session")
def session_fixture(db_url):
    engine = create_engine(
        db_url,
        echo=False
    )
    with Session(engine) as session:
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
    json_file = open("examples/"+igsn_suffix+".json")
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
