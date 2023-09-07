from typing import Optional
from sqlmodel import Field, SQLModel


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
