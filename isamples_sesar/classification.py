from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class Classification(SQLModel, table=True):
    classification_id: int = Field(
        primary_key=True,
        nullable=False,
        description=""
    )
    parent_classification_id: Optional[int] = Field(
        default=None,
        nullable=True,
        description="",
        foreign_key="classification.classification_id"
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
    parent_classification: Optional["Classification"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs=dict(
            remote_side="Classification.classification_id"
        )
    )
    children: Optional[List["Classification"]] = Relationship(
        back_populates="parent_classification"
    )
