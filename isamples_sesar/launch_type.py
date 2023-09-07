import sys
import json
from typing import TYPE_CHECKING, Optional, List
import typing
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
import sqlalchemy

if TYPE_CHECKING:
    from .sample import Sample

class Launch_Type(SQLModel, table=True):
    launch_type_id: int = Field(
        primary_key=True,
        nullable=False,
        description=""
    )
    name: str = Field(
        default=None,
        nullable=True,
        description=""
    )
    description: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )