from typing import Optional, List
from sqlmodel import Field, Relationship
from datetime import datetime

from .sesar_sqlmodel import SesarBase
from .classification import Classification
from .country import Country
from .launch_type import Launch_Type
from .nav_type import Nav_Type
from .sample_additional_name import Sample_Additional_Name
from .sample_type import Sample_Type
from .sesar_user import Sesar_User


class Sample(SesarBase, table=True):
    sample_id: int = Field(
        primary_key=True,
        nullable=False,
        description="identifier scheme:value, globally unique"
    )
    origin_sample_id: Optional[int] = Field(
        default=None,
        nullable=True,
        description="parent sample id",
        foreign_key="sample.sample_id"
    )
    external_parent_sample_type_id: Optional[int] = Field(
        default=None,
        nullable=True,
        description="",
        foreign_key="sample_type.sample_type_id"
    )
    external_parent_name: Optional[str] = Field(
        default=None,
        nullable=True,
        description="parent sample external name",
    )
    sample_type_id: int = Field(
        nullable=False,
        description="sample type id",
        foreign_key="sample_type.sample_type_id"
    )
    igsn: str = Field(
        nullable=False
    )
    igsn_prefix: str = Field(
        nullable=False,
        description="sesar internal igsn user code"
    )
    external_sample_id: Optional[str] = Field(
        default=None,
        nullable=True,
        description="sample identifier from external source"
    )
    publish_date: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="date data is published and publically visible",
    )
    archive_date: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="date a sample was deactivated",
    )
    registration_date: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="date a sample was registered",
    )
    name: str = Field(
        nullable=False,
        description="sample name"
    )
    current_archive: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    current_archive_contact: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    original_archive: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    original_archive_contact: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    collection_method: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    collection_method_descr: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    size: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    size_unit: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    classification_id: Optional[int] = Field(
        default=None,
        nullable=True,
        description="",
        foreign_key="classification.classification_id"
    )
    classification_comment: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    top_level_classification_id: Optional[int] = Field(
        default=None,
        nullable=True,
        description="",
        foreign_key="classification.classification_id"
    )
    description: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    sample_comment: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    depth_min: Optional[float] = Field(
        default=None,
        nullable=True,
        description=""
    )
    depth_max: Optional[float] = Field(
        default=None,
        nullable=True,
        description=""
    )
    depth_scale: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    age_min: Optional[float] = Field(
        default=None,
        nullable=True,
        description=""
    )
    age_max: Optional[float] = Field(
        default=None,
        nullable=True,
        description=""
    )
    age_unit: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    geological_age: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    geological_unit: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    latitude: Optional[float] = Field(
        default=None,
        nullable=True,
        description=""
    )
    latitude_end: Optional[float] = Field(
        default=None,
        nullable=True,
        description=""
    )
    longitude: Optional[float] = Field(
        default=None,
        nullable=True,
        description=""
    )
    longitude_end: Optional[float] = Field(
        default=None,
        nullable=True,
        description=""
    )
    elevation: Optional[float] = Field(
        default=None,
        nullable=True,
        description=""
    )
    elevation_end: Optional[float] = Field(
        default=None,
        nullable=True,
        description=""
    )
    elevation_unit: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    primary_location_type: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    primary_location_name: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    location_description: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    locality: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    locality_description: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    country_id: Optional[int] = Field(
        default=None,
        nullable=True,
        description="",
        foreign_key="country.country_id"
    )
    field_name: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    province: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    county: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    city: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    cruise_field_prgrm: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    platform_type: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    platform_name: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    platform_descr: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    collector: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    collector_detail: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    collection_start_date: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="",
    )
    collection_end_date: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="",
    )
    collection_date_precision: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    nav_type_id: Optional[int] = Field(
        default=None,
        nullable=True,
        description="",
        foreign_key="nav_type.nav_type_id"
    )
    launch_platform_name: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    launch_type_id: Optional[int] = Field(
        default=None,
        nullable=True,
        description="",
        foreign_key="launch_type.launch_type_id"
    )
    launch_id: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    purpose: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    easting: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    northing: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    zone: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    vertical_datum: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    cur_registrant_id: Optional[int] = Field(
        default=None,
        nullable=True,
        description="",
        foreign_key="sesar_user.sesar_user_id"
    )
    orig_owner_id: Optional[int] = Field(
        default=None,
        nullable=True,
        description="",
        foreign_key="sesar_user.sesar_user_id"
    )
    cur_owner_id: Optional[int] = Field(
        default=None,
        nullable=True,
        description="",
        foreign_key="sesar_user.sesar_user_id"
    )
    metadata_store_status: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    parent: Optional["Sample"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs=dict(
            remote_side="Sample.sample_id"
        )
    )
    children: Optional[List["Sample"]] = Relationship(
        back_populates="parent"
    )
    country: Optional["Country"] = Relationship()
    classification: Optional["Classification"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin":
                "Sample.classification_id==Classification.classification_id"
        }
    )
    top_level_classification: Optional["Classification"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin":
                "Sample.top_level_classification_id==Classification.classification_id"
        }
    )
    launch_type: Optional["Launch_Type"] = Relationship()
    nav_type: Optional["Nav_Type"] = Relationship()
    additional_names: Optional[List["Sample_Additional_Name"]] = Relationship()
    sample_type: "Sample_Type" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin":
                "Sample.sample_type_id==Sample_Type.sample_type_id"
        }
    )
    external_parent_sample_type: Optional["Sample_Type"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin":
                "Sample.external_parent_sample_type_id==Sample_Type.sample_type_id"
        }
    )
    cur_registrant: Optional["Sesar_User"] = Relationship(
        back_populates="cur_registrant_samples",
        sa_relationship_kwargs={
            "primaryjoin": "Sample.cur_registrant_id==Sesar_User.sesar_user_id"
        }
    )
    cur_owner: Optional["Sesar_User"] = Relationship(
        back_populates="cur_owner_samples",
        sa_relationship_kwargs={
            "primaryjoin": "Sample.cur_owner_id==Sesar_User.sesar_user_id"
        }
    )
    orig_owner: Optional["Sesar_User"] = Relationship(
        back_populates="orig_owner_samples",
        sa_relationship_kwargs={
            "primaryjoin": "Sample.orig_owner_id==Sesar_User.sesar_user_id"
        }
    )
