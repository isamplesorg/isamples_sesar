import sys
import json
from typing import TYPE_CHECKING, Optional
import typing
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
import sqlalchemy

if TYPE_CHECKING:
    from .sample import Sample

class Sample_Additional_Name(SQLModel, table=True):
    sample_additional_name_id: int = Field(
        primary_key=True,
        nullable=False,
        description=""
    )
    sample_id: int = Field(
        primary_key=True,
        nullable=True,
        description="",
        foreign_key="sample.sample_id"
    )
    name: str = Field(
        default=None,
        nullable=True,
        description=""
    )