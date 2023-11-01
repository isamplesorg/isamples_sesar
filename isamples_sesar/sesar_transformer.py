import typing
from typing import Optional
import logging
from .sample import Sample

from .mapper import (
    AbstractCategoryMapper,
    StringPairedCategoryMapper,
    StringOrderedCategoryMapper,
    StringEqualityCategoryMapper,
    StringEndsWithCategoryMapper,
    AbstractCategoryMetaMapper,
)


class Transformer():

    NOT_PROVIDED = "Not Provided"

    FEET_PER_METER = 3.28084

    def __init__(self, sample: Sample):
        self.sample = sample
        self._material_prediction_results: Optional[list] = None

    def transform(self) -> typing.Dict:
        """Do the actual work of transforming a Sesar record into an iSamples record.

        Arguments:
            sample -- The Sesar record to be transformed
        Return value:
            The Sesar record transformed into an iSamples record
        """
        context_categories = self.has_context_categories()
        material_categories = self.has_material_categories()
        specimen_categories = self.has_specimen_categories()
        transformed_record = {
            "$schema": "iSamplesSchemaCore1.0.json",
            "@id": self.id_string(),
            "label": self.sample_label(),
            "sampleidentifier": self.sample_identifier_string(),
            "description": self.sample_description(),
            "hasContextCategory": context_categories,
            # "hasContextCategoryConfidence": self.has_context_category_confidences(context_categories),
            "hasMaterialCategory": material_categories,
            # "hasMaterialCategoryConfidence": self.has_material_category_confidences(material_categories),
            "hasSpecimenCategory": specimen_categories,
            # "hasSpecimenCategoryConfidence": self.has_specimen_category_confidences(specimen_categories),
            "informalClassification": self.informal_classification(),
            "keywords": self.keywords(),
            "producedBy": {
                "@id": self.produced_by_id_string(),
                "label": self.produced_by_label(),
                "description": self.produced_by_description(),
                "hasFeatureOfInterest": self.produced_by_feature_of_interest(),
                "responsibility": self.produced_by_responsibilities(),
                "resultTime": self.produced_by_result_time(),
                "samplingSite": {
                    "description": self.sampling_site_description(),
                    "label": self.sampling_site_label(),
                    "location": {
                        "elevation": self.sampling_site_elevation(),
                        "latitude": self.sampling_site_latitude(),
                        "longitude": self.sampling_site_longitude(),
                    },
                    "placeName": self.sampling_site_place_names(),
                },
            },
            "registrant": self.sample_registrant(),
            "samplingPurpose": self.sample_sampling_purpose(),
            "curation": {
                "label": self.curation_label(),
                "description": self.curation_description(),
                "accessConstraints": self.curation_access_constraints(),
                "curationLocation": self.curation_location(),
                "responsibility": self.curation_responsibility(),
            },
            "relatedResource": self.related_resources(),
            "authorizedBy": self.authorized_by(),
            "compliesWith": self.complies_with(),
        }
        return transformed_record

    def has_context_categories(self) -> typing.List[str]:
        material_type = self._material_type()
        primary_location_type = self.sample.primary_location_type
        return ContextCategoryMetaMapper.categories(
            material_type, primary_location_type
        )

    # def has_material_categories(self) -> typing.List[str]:
    #     material = self._material_type()
    #     return MaterialCategoryMetaMapper.categories(material)
    #
    # def has_material_category_confidences(self, material_categories: list[str]) -> Optional[typing.List[float]]:
    #     return None

    # Disabled pending resolution of https://github.com/isamplesorg/isamples_inabox/issues/255
    def has_material_categories(self) -> typing.List[str]:
        material = self._material_type()
        # TODO: implement predictions
        # if not material:
        #     prediction_results = self._compute_material_prediction_results()
        #     if prediction_results is not None:
        #         return [prediction.value for prediction in prediction_results]
        #     else:
        #         return []
        return MaterialCategoryMetaMapper.categories(material)

    def has_specimen_categories(self) -> typing.List[str]:
        sample_type = self.sample.sample_type.name
        return SpecimenCategoryMetaMapper.categories(sample_type)

    def id_string(self) -> str:
        return f"https://data.isamples.org/digitalsample/igsn/{self.sample.igsn}"

    def _material_type(self) -> str:
        if self.sample.classification and self.sample.top_level_classification:
            return f"{self.sample.classification.name}>{self.sample.top_level_classification.name}"
        elif self.sample.classification:
            return self.sample.classification.name
        elif self.sample.top_level_classification:
            return self.sample.top_level_classification.name
        return ""

    @staticmethod
    def _logger():
        return logging.getLogger("isamples_metadata.SESARTransformer")

    def sample_label(self) -> str:
        return self.sample.name

    def sample_identifier_string(self) -> str:
        return f"igsn:{self.sample.igsn}"

    def sample_description(self) -> str:
        description_arr = []

        classification = self._material_type()
        if classification:
            description_arr.append(classification)

        if self.sample.collection_method:
            description_arr.append(self.sample.collection_method)

        if self.sample.description:
            description_arr.append(self.sample.description)

        if description_arr:
            description = ". ".join(description_arr)
            return description
        return Transformer.NOT_PROVIDED

    def informal_classification(self) -> typing.List[str]:
        """Not currently used for SESAR"""
        return [Transformer.NOT_PROVIDED]

    def keywords(self) -> typing.List:
        # TODO: add more keywords
        keyword_arr = []
        sample_type = self.sample.sample_type
        if sample_type:
            parent_sample_type = self.sample.sample_type.parent_sample_type
            if parent_sample_type:
                sample_type_str = f"{parent_sample_type.name}>{sample_type.name}"
            else:
                sample_type_str = sample_type.name
            keyword_arr.append({
                "keyword": sample_type_str,
                "scheme_name": "SESAR: Sample Type"
            })

        if self.sample.field_name:
            keyword_arr.append({
                "keyword": self.sample.field_name,
                "scheme_name": "taxon: species"
            })

        if keyword_arr:
            return keyword_arr

        return [Transformer.NOT_PROVIDED]

    def produced_by_id_string(self) -> str:
        if self.sample.parent is not None:
            return f"igsn:{self.sample.parent.igsn}"
        return ""

    def produced_by_label(self) -> str:
        if self.sample.collection_method and self.sample.cruise_field_prgrm:
            return f"{self.sample.collection_method}, {self.sample.cruise_field_prgrm}"
        elif self.sample.collection_method:
            return self.sample.collection_method
        elif self.sample.cruise_field_prgrm:
            return self.sample.cruise_field_prgrm
        else:
            return Transformer.NOT_PROVIDED

    def produced_by_description(self) -> str:  # noqa: C901 -- need to examine computational complexity
        description_components = list()

        if self.sample.cruise_field_prgrm:
            description_components.append(
                "cruiseFieldPrgrm:{0}".format(
                    self.sample.cruise_field_prgrm
                )
            )
        if self.sample.launch_platform_name:
            description_components.append(
                "launchPlatformName:{0}".format(
                    self.sample.launch_platform_name
                )
            )

        if self.sample.collection_method:
            description_components.append(
                "Collection method:{0}".format(
                    self.sample.collection_method
                ))
        if self.sample.description:
            description_components.append(self.sample.description)

        launch_type_str = ""
        if self.sample.launch_type:
            launch_type_str += "launch type:{0}, ".format(
                self.sample.launch_type.name
            )
        if self.sample.nav_type:
            launch_type_str += "navigation type:{0}".format(
                self.sample.nav_type.name
            )
        if len(launch_type_str) > 0:
            description_components.append(launch_type_str)

        if description_components:
            return ". ".join(description_components)
        else:
            return Transformer.NOT_PROVIDED

    def produced_by_feature_of_interest(self) -> str:
        if self.sample.primary_location_type:
            return self.sample.primary_location_type
        return Transformer.NOT_PROVIDED

    def produced_by_result_time(self) -> str:
        if self.sample.collection_start_date:
            return self.sample.collection_start_date.strftime('%Y-%m-%d')
        elif self.sample.registration_date:
            return self.sample.registration_date.strftime('%Y-%m-%d')
        return Transformer.NOT_PROVIDED

    def produced_by_responsibilities(self) -> list[dict]:
        responsibilities = list()
        if self.sample.collector and self.sample.collector.lower() != 'curator':
            collector = {
                "role": "collector",
                "name": self.sample.collector
            }
            responsibilities.append(collector)

        # if self.sample.orig_owner:
        #     if self.sample.orig_owner.fname.lower() == 'curator':
        #         sample_owner_name = self.sample.orig_owner.lname
        #     else:
        #         sample_owner_name = f"{self.sample.orig_owner.fname} {self.sample.orig_owner.lname}"
        #     if sample_owner_name:
        #         sample_owner = {
        #             "role": "sample owner",
        #             "name": sample_owner_name
        #         }
        #         responsibilities.append(sample_owner)

        if self.sample.cruise_field_prgrm:
            cruise_field_prgrm = {
                "role": "sponsor",
                "name": self.sample.cruise_field_prgrm
            }
            responsibilities.append(cruise_field_prgrm)

        return responsibilities

    def sampling_site_description(self) -> str:
        if self.sample.locality_description and self.sample.location_description:
            return f"{self.sample.locality_description}; {self.sample.location_description}"
        if self.sample.locality_description:
            return self.sample.locality_description
        if self.sample.location_description:
            return self.sample.location_description
        return Transformer.NOT_PROVIDED

    def sampling_site_label(self) -> str:
        if self.sample.locality:
            return self.sample.locality
        return Transformer.NOT_PROVIDED

    def sampling_site_elevation(self) -> str:
        if self.sample.elevation:
            elevation_value = str(self.sample.elevation)
            elevation_unit = self.sample.elevation_unit or "meters"
            return self.elevation_str(elevation_value, elevation_unit)
        return Transformer.NOT_PROVIDED

    def elevation_str(
        self, elevation_value: str, elevation_unit: str
    ) -> str:
        elevation_unit_abbreviation = ""
        if elevation_unit is not None:
            elevation_unit = elevation_unit.lower().strip()
            if elevation_unit == "feet":
                # target elevation for core metadata will always be meters, so convert here
                elevation_value = str(float(elevation_value) / Transformer.FEET_PER_METER)
                elevation_unit_abbreviation = "m"
            elif elevation_unit == "meters":
                elevation_unit_abbreviation = "m"
            else:
                self._logger().error(
                    "Received elevation in unexpected unit: ", elevation_unit
                )
        elevation_str = str(elevation_value)
        if len(elevation_unit_abbreviation) > 0:
            elevation_str += " " + elevation_unit_abbreviation
        return elevation_str

    def sampling_site_latitude(self) -> Optional[typing.SupportsFloat]:
        return self.sample.latitude

    def sampling_site_longitude(self) -> Optional[typing.SupportsFloat]:
        return self.sample.longitude

    def sampling_site_place_names(self) -> typing.List:
        place_names = list()
        if self.sample.primary_location_name:
            primary_location_name = self.sample.primary_location_name
            place_names.extend(primary_location_name.split("; "))
        if self.sample.province:
            place_names.append(self.sample.province)
        if self.sample.county:
            place_names.append(self.sample.county)
        if self.sample.city:
            place_names.append(self.sample.city)
        return place_names

    def sample_registrant(self) -> str:
        if self.sample.cur_registrant:
            if self.sample.cur_registrant.fname.lower() == 'curator':
                return self.sample.cur_registrant.lname
            else:
                return f"{self.sample.cur_registrant.fname} {self.sample.cur_registrant.lname}"
        return Transformer.NOT_PROVIDED

    def sample_sampling_purpose(self) -> str:
        if self.sample.purpose:
            return self.sample.purpose
        else:
            return Transformer.NOT_PROVIDED

    def related_resources(self) -> typing.List[str]:
        # Don't have this information
        return []

    def authorized_by(self) -> typing.List[str]:
        # Don't have this information
        return []

    def complies_with(self) -> typing.List[str]:
        # Don't have this information
        return []

    def curation_label(self) -> str:
        return Transformer.NOT_PROVIDED

    def curation_description(self) -> str:
        return Transformer.NOT_PROVIDED

    def curation_access_constraints(self) -> str:
        return Transformer.NOT_PROVIDED

    def curation_location(self) -> str:
        if self.sample.current_archive:
            return self.sample.current_archive
        return Transformer.NOT_PROVIDED

    def curation_responsibility(self) -> list[dict]:
        responsibility: list[dict] = []
        if self.sample.cur_owner:
            if self.sample.cur_owner.fname.lower() == 'curator':
                sample_owner_name = self.sample.cur_owner.lname
                sample_curator = {
                    "role": "curator",
                    "name": sample_owner_name
                }
                responsibility.append(sample_curator)
            else:
                sample_owner_name = f"{self.sample.cur_owner.fname} {self.sample.cur_owner.lname}"
            sample_owner = {
                "role": "sample owner",
                "name": sample_owner_name,
                "contact_information": self.sample.cur_owner.email
            }
            responsibility.append(sample_owner)

        metadata_publisher = {
            "role": "metadata publisher",
            "contact_information": "info@geosamples.org; url: https://www.geosamples.org/contact/"
        }
        responsibility.append(metadata_publisher)
        return responsibility


class MaterialCategoryMetaMapper(AbstractCategoryMetaMapper):
    _endsWithRockMapper = StringEndsWithCategoryMapper("Rock", "Rock")
    _endsWithMineralMapper = StringEndsWithCategoryMapper("Mineral", "Mineral")
    _endsWithAqueousMapper = StringEndsWithCategoryMapper("aqueous", "Liquid water")
    _endsWithSedimentMapper = StringEndsWithCategoryMapper("Sediment", "Sediment")
    _endsWithSoilMapper = StringEndsWithCategoryMapper("Soil", "Soil")
    _endsWithParticulateMapper = StringEndsWithCategoryMapper(
        "Particulate", "Particulate"
    )
    _endsWithBiologyMapper = StringEndsWithCategoryMapper("Biology", "Organic material")
    _endsWithSyntheticMapper = StringEndsWithCategoryMapper(
        "Synthetic", "Anthropogenic material"
    )
    _equalsRockMapper = StringEqualityCategoryMapper(
        [
            "Glass>Other",
            "Igneous>Other",
            "Igneous>Volcanic>Felsic>NotApplicable",
            "Igneous>Volcanic>Other",
            "Metamorphic>Other",
            "Sedimentary>Other",
            "Xenolithic>Other",
        ],
        "Rock",
    )
    _equalsSedimentMapper = StringEqualityCategoryMapper(["Tephra"], "Sediment")
    _equalsOrganicMaterialMapper = StringEqualityCategoryMapper(
        ["Siderite>Mineral", "Macrobiology>Other", "Organic Material"],
        "Organic material",
    )
    _equalsNonAqueousLiquidMaterialMapper = StringEqualityCategoryMapper(
        ["Liquid>organic"], "Non-aqueous liquid material"
    )
    _equalsMineralMapper = StringEqualityCategoryMapper(
        [
            "Ore>Other",
            "FeldsparGroup>Other",
            "Epidote>Other",
            "Enstatite>Other",
            "Betpakdalite>Other",
            "Aurichalcite>Other",
            "Augite>Other",
            "Aragonite>Biology",
            "AmphiboleGroup>Other",
            "Actinolite>Other",
        ],
        "Mineral",
    )
    _equalsIceMapper = StringEqualityCategoryMapper(["Ice"], "Ice")
    _equalsGasMapper = StringEqualityCategoryMapper(["Gas"], "Gaseous material")
    _equalsBiogenicMapper = StringEqualityCategoryMapper(
        ["Macrobiology>Coral>Biology", "Coral>Biology"], "Biogenic non-organic material"
    )
    _equalsNaturalSolidMapper = StringEqualityCategoryMapper(
        ["Natural Solid Material"], "Natural Solid Material"
    )
    _equalsMixedMapper = StringEqualityCategoryMapper(
        ["Mixed soil, sediment, rock"], "Mixed soil, sediment, rock"
    )
    _equalsMaterialMapper = StringEqualityCategoryMapper(
        ["Material"], "Material"
    )

    @classmethod
    def categories_mappers(cls) -> typing.List[AbstractCategoryMapper]:
        return [
            cls._endsWithRockMapper,
            cls._endsWithMineralMapper,
            cls._endsWithAqueousMapper,
            cls._endsWithSedimentMapper,
            cls._endsWithSoilMapper,
            cls._endsWithParticulateMapper,
            cls._endsWithBiologyMapper,
            cls._endsWithSyntheticMapper,
            cls._equalsRockMapper,
            cls._equalsSedimentMapper,
            cls._equalsIceMapper,
            cls._equalsOrganicMaterialMapper,
            cls._equalsNonAqueousLiquidMaterialMapper,
            cls._equalsMineralMapper,
            cls._equalsIceMapper,
            cls._equalsGasMapper,
            cls._equalsBiogenicMapper,
            cls._equalsNaturalSolidMapper,
            cls._equalsMixedMapper,
            cls._equalsMaterialMapper
        ]


class SpecimenCategoryMetaMapper(AbstractCategoryMetaMapper):
    _otherSolidObjectsMapper = StringEqualityCategoryMapper(
        [
            "Core",
            "Core Half Round",
            "Core Piece",
            "Core Quarter Round",
            "Core Section",
            "Core Section Half",
            "Core Sub-Piece",
            "Core Whole Round",
            "Grab",
            "Individual Sample",
            "Individual Sample>Cube",
            "Individual Sample>Cylinder",
            "Individual Sample>Slab",
            "Individual Sample>Specimen",
            "Oriented Core",
        ],
        "Other solid object",
    )
    _containersWithFluidMapper = StringEqualityCategoryMapper(
        [
            "CTD",
            "Individual Sample>Gas",
            "Individual Sample>Liquid",
        ],
        "Fluid in container",
    )
    _experimentalProductsMapper = StringEqualityCategoryMapper(
        ["Experimental Specimen"], "Experiment product"
    )
    _biomeAggregationsMapper = StringEqualityCategoryMapper(
        ["Trawl"], "Biome aggregation"
    )
    _analyticalPreparationsMapper = StringEqualityCategoryMapper(
        [
            "Individual Sample>Bead",
            "Individual Sample>Chemical Fraction",
            "Individual Sample>Culture",
            "Individual Sample>Mechanical Fraction",
            "Individual Sample>Powder",
            "Individual Sample>Smear",
            "Individual Sample>Thin Section",
            "Individual Sample>Toothpick",
            "Individual Sample>U-Channel",
            "Rock Powder",
        ],
        "Analytical preparation",
    )
    _aggregationsMapper = StringEqualityCategoryMapper(
        ["Cuttings", "Dredge"], "Aggregation"
    )

    @classmethod
    def categories_mappers(cls) -> typing.List[AbstractCategoryMapper]:
        return [
            cls._otherSolidObjectsMapper,
            cls._containersWithFluidMapper,
            cls._experimentalProductsMapper,
            cls._biomeAggregationsMapper,
            cls._analyticalPreparationsMapper,
            cls._aggregationsMapper,
        ]


class ContextCategoryMetaMapper(AbstractCategoryMetaMapper):
    _endsWithRockMapper = StringEndsWithCategoryMapper("Rock", "Earth interior")
    _endsWithMineralMapper = StringEndsWithCategoryMapper("Mineral", "Earth interior")
    _equalsGasMapper = StringEqualityCategoryMapper(
        ["Gas"], "Subsurface fluid reservoir"
    )
    # This one is actually incorrect as written, we need to use the combo of material and primaryLocationType
    _endsWithSoilMapper = StringEndsWithCategoryMapper(
        "Soil", "Subaerial surface environment"
    )
    _soilFloodplainMapper = StringPairedCategoryMapper(
        "Microbiology>Soil", "floodplain", "Subaerial terrestrial biome"
    )
    _soilMapper = StringOrderedCategoryMapper(
        # Order matters here, the generic one needs to be last
        [_soilFloodplainMapper, _endsWithSoilMapper]
    )
    _seaSedimentMapper = StringPairedCategoryMapper(
        "Sediment", "sea", "Marine water body bottom"
    )
    _lakeSedimentMapper = StringPairedCategoryMapper(
        "Sediment", "lake", "Lake, river or stream bottom"
    )
    _sedimentMapper = StringOrderedCategoryMapper(
        [_seaSedimentMapper, _lakeSedimentMapper]
    )
    _lakeMapper = StringPairedCategoryMapper("", "lake", "Terrestrial water body")
    _mountainLiquidMapper = StringPairedCategoryMapper(
        "Liquid>aqueous", "Mountain", "Terrestrial water body"
    )
    _seaMapper = StringPairedCategoryMapper(
        "Liquid>aqueous", "Sea", "Marine water body"
    )
    _ventBiologyMapper = StringPairedCategoryMapper("Biology", "Vent", "Marine biome")
    _ventLiquidMapper = StringPairedCategoryMapper(
        "Liquid>aqueous", "Vent", "Subsurface fluid reservoir"
    )
    _floodplainAquiferMapper = StringPairedCategoryMapper(
        "Liquid>aqueous", "floodplain, aquifer", "Subsurface fluid reservoir"  # noqa: W605
    )
    _creekBankMapper = StringPairedCategoryMapper(
        "Sedimentary>GlacialAndOrPaleosol>Rock",
        "Creek bank",
        "Subaerial surface environment",
    )
    # Note that this represents the combos down to row 109 of
    # https://docs.google.com/spreadsheets/d/1QitBRkWH6YySZnNO-uR7D2rTaQ826WPT_xow9lPdJDM/edit#gid=1251732948
    # Need to continue on from there…

    @classmethod
    def categories_mappers(cls) -> typing.List[AbstractCategoryMapper]:
        return [
            cls._endsWithRockMapper,
            cls._endsWithMineralMapper,
            cls._equalsGasMapper,
            cls._soilMapper,
            cls._sedimentMapper,
            cls._lakeMapper,
            cls._mountainLiquidMapper,
            cls._seaMapper,
            cls._ventBiologyMapper,
            cls._ventLiquidMapper,
            cls._floodplainAquiferMapper,
            cls._creekBankMapper,
        ]
