from sqlmodel import Field
from .sesar_sqlmodel import SesarBase


class Sample_Additional_Name(SesarBase, table=True):
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
