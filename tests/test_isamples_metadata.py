import pytest
import json

from isamples_api.metadata_constants import METADATA_SAMPLE_IDENTIFIER, METADATA_DESCRIPTION, \
    METADATA_HAS_CONTEXT_CATEGORY, METADATA_HAS_SAMPLE_OBJECT_TYPE, METADATA_INFORMAL_CLASSIFICATION, METADATA_KEYWORDS, \
    METADATA_PRODUCED_BY, METADATA_AT_ID, METADATA_LABEL, METADATA_HAS_FEATURE_OF_INTEREST, METADATA_RESPONSIBILITY, \
    METADATA_HAS_MATERIAL_CATEGORY, METADATA_RESULT_TIME, METADATA_SAMPLING_SITE, METADATA_PLACE_NAME, \
    METADATA_LOCATION, METADATA_ELEVATION, METADATA_LATITUDE, METADATA_LONGITUDE, METADATA_REGISTRANT, \
    METADATA_SAMPLING_PURPOSE, METADATA_CURATION, METADATA_ACCESS_CONSTRAINTS, METADATA_CURATION_LOCATION, \
    METADATA_RELATED_RESOURCE, METADATA_AUTHORIZED_BY, METADATA_COMPLIES_WITH, METADATA_SAMPLE_LOCATION
from sqlmodel import Session
from isamples_sesar.sesar_transformer import Transformer
from isamples_sesar.sqlmodel_database import (
    get_sample_with_igsn
)


@pytest.mark.parametrize("igsn", ["10.58052/EOI00002H",
                                  "10.58052/IEDUT103B",
                                  "10.58052/IEEJR000M",
                                  "10.58052/IEJEN0040",
                                  "10.58052/IERVTL1I7",
                                  "10.60471/ODP02Q1IZ"])
def test_example(sesar_session: Session, igsn):
    # get sample and transform it
    sample = get_sample_with_igsn(sesar_session, igsn)
    assert sample is not None
    transformed_test_data = Transformer(sample).transform()

    igsn_suffix = igsn.split("/")[1]
    file_path = "examples/" + igsn_suffix + ".json"
    with open(file_path, "r", encoding="UTF-8") as f:
        expected_data = json.load(f)

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
    assert test_data[METADATA_SAMPLE_IDENTIFIER] == expected_data[METADATA_SAMPLE_IDENTIFIER]


def check_description(test_data, expected_data):
    assert test_data[METADATA_DESCRIPTION] == expected_data[METADATA_DESCRIPTION]


def check_context_category(test_data, expected_data):
    assert test_data[METADATA_HAS_CONTEXT_CATEGORY] == expected_data[METADATA_HAS_CONTEXT_CATEGORY]
    # assert test_data["hasContextCategoryConfidence"] == expected_data["hasContextCategoryConfidence"]


def check_material_category(test_data, expected_data):
    assert test_data[METADATA_HAS_MATERIAL_CATEGORY] == expected_data[METADATA_HAS_MATERIAL_CATEGORY]
    # assert test_data["hasMaterialCategoryConfidence"] == expected_data["hasMaterialCategoryConfidence"]


def check_specimen_category(test_data, expected_data):
    assert test_data[METADATA_HAS_SAMPLE_OBJECT_TYPE] == expected_data[METADATA_HAS_SAMPLE_OBJECT_TYPE]
    # assert test_data["hasSpecimenCategoryConfidence"] == expected_data["hasSpecimenCategoryConfidence"]


def check_informal_classification(test_data, expected_data):
    assert test_data[METADATA_INFORMAL_CLASSIFICATION] == expected_data[METADATA_INFORMAL_CLASSIFICATION]


def check_keywords(test_data, expected_data):
    assert test_data[METADATA_KEYWORDS] == expected_data[METADATA_KEYWORDS]


def check_produced_by_id(test_data, expected_data):
    assert test_data[METADATA_PRODUCED_BY][METADATA_AT_ID] == expected_data[METADATA_PRODUCED_BY][METADATA_AT_ID]


def check_produced_by_label(test_data, expected_data):
    assert test_data[METADATA_PRODUCED_BY][METADATA_LABEL] == expected_data[METADATA_PRODUCED_BY][METADATA_LABEL]


def check_produced_by_description(test_data, expected_data):
    assert test_data[METADATA_PRODUCED_BY][METADATA_DESCRIPTION] == expected_data[METADATA_PRODUCED_BY][METADATA_DESCRIPTION]


def check_produced_by_feature(test_data, expected_data):
    assert test_data[METADATA_PRODUCED_BY][METADATA_HAS_FEATURE_OF_INTEREST] == expected_data[METADATA_PRODUCED_BY][METADATA_HAS_FEATURE_OF_INTEREST]


def check_produced_by_responsibility(test_data, expected_data):
    assert test_data[METADATA_PRODUCED_BY][METADATA_RESPONSIBILITY] == expected_data[METADATA_PRODUCED_BY][METADATA_RESPONSIBILITY]


def check_produced_by_time(test_data, expected_data):
    assert test_data[METADATA_PRODUCED_BY][METADATA_RESULT_TIME] == expected_data[METADATA_PRODUCED_BY][METADATA_RESULT_TIME]


def check_sampling_site_description(test_data, expected_data):
    assert test_data[METADATA_PRODUCED_BY][METADATA_SAMPLING_SITE][METADATA_DESCRIPTION] == \
        expected_data[METADATA_PRODUCED_BY][METADATA_SAMPLING_SITE][METADATA_DESCRIPTION]


def check_sampling_site_label(test_data, expected_data):
    assert test_data[METADATA_PRODUCED_BY][METADATA_SAMPLING_SITE][METADATA_LABEL] == \
        expected_data[METADATA_PRODUCED_BY][METADATA_SAMPLING_SITE][METADATA_LABEL]


def check_sampling_site_place_name(test_data, expected_data):
    assert test_data[METADATA_PRODUCED_BY][METADATA_SAMPLING_SITE][METADATA_PLACE_NAME] == \
        expected_data[METADATA_PRODUCED_BY][METADATA_SAMPLING_SITE][METADATA_PLACE_NAME]


def check_sampling_site_elevation(test_data, expected_data):
    assert test_data[METADATA_PRODUCED_BY][METADATA_SAMPLING_SITE][METADATA_SAMPLE_LOCATION][METADATA_ELEVATION] == \
        expected_data[METADATA_PRODUCED_BY][METADATA_SAMPLING_SITE][METADATA_SAMPLE_LOCATION][METADATA_ELEVATION]


def check_sampling_site_latitude(test_data, expected_data):
    assert test_data[METADATA_PRODUCED_BY][METADATA_SAMPLING_SITE][METADATA_SAMPLE_LOCATION][METADATA_LATITUDE] == \
        expected_data[METADATA_PRODUCED_BY][METADATA_SAMPLING_SITE][METADATA_SAMPLE_LOCATION][METADATA_LATITUDE]


def check_sampling_site_longitude(test_data, expected_data):
    assert test_data[METADATA_PRODUCED_BY][METADATA_SAMPLING_SITE][METADATA_SAMPLE_LOCATION][METADATA_LONGITUDE] == \
        expected_data[METADATA_PRODUCED_BY][METADATA_SAMPLING_SITE][METADATA_SAMPLE_LOCATION][METADATA_LONGITUDE]


def check_registrant(test_data, expected_data):
    assert test_data[METADATA_REGISTRANT] == expected_data[METADATA_REGISTRANT]


def check_sampling_purpose(test_data, expected_data):
    assert test_data[METADATA_SAMPLING_PURPOSE] == expected_data[METADATA_SAMPLING_PURPOSE]


def check_curation_label(test_data, expected_data):
    assert test_data[METADATA_CURATION][METADATA_LABEL] == expected_data[METADATA_CURATION][METADATA_LABEL]


def check_curation_description(test_data, expected_data):
    assert test_data[METADATA_CURATION][METADATA_DESCRIPTION] == expected_data[METADATA_CURATION][METADATA_DESCRIPTION]


def check_curation_access_constraints(test_data, expected_data):
    assert test_data[METADATA_CURATION][METADATA_ACCESS_CONSTRAINTS] == expected_data[METADATA_CURATION][METADATA_ACCESS_CONSTRAINTS]


def check_curation_location(test_data, expected_data):
    assert test_data[METADATA_CURATION][METADATA_CURATION_LOCATION] == expected_data[METADATA_CURATION][METADATA_CURATION_LOCATION]


def check_curation_responsibility(test_data, expected_data):
    assert test_data[METADATA_CURATION][METADATA_RESPONSIBILITY] == expected_data[METADATA_CURATION][METADATA_RESPONSIBILITY]


def check_related_resource(test_data, expected_data):
    assert test_data[METADATA_RELATED_RESOURCE] == expected_data[METADATA_RELATED_RESOURCE]


def check_authorized_by(test_data, expected_data):
    assert test_data[METADATA_AUTHORIZED_BY] == expected_data[METADATA_AUTHORIZED_BY]


def check_complies_with(test_data, expected_data):
    assert test_data[METADATA_COMPLIES_WITH] == expected_data[METADATA_COMPLIES_WITH]
