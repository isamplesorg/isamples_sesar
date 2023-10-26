from typing import Optional
from sqlmodel import Field
from .sesar_sqlmodel import SesarBase


class Nav_Type(SesarBase, table=True):
    nav_type_id: int = Field(
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
