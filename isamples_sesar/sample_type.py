from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class Sample_Type(SQLModel, table=True):
    sample_type_id: int = Field(
        primary_key=True,
        nullable=False,
        description="sample type id"
    )
    name: str = Field(
        default=None,
        nullable=True,
        description="sample type name"
    )
    parent_sample_type_id: Optional[int] = Field(
        default=None,
        nullable=True,
        description="parent sample type id",
        foreign_key="sample_type.sample_type_id"
    )
    parent_sample_type: Optional["Sample_Type"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs=dict(
            remote_side="Sample_Type.sample_type_id"
        )
    )
    children: Optional[List["Sample_Type"]] = Relationship(
        back_populates="parent_sample_type"
    )
