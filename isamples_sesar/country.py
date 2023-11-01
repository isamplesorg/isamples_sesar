from sqlmodel import Field
from .sesar_sqlmodel import SesarBase


class Country(SesarBase, table=True):
    country_id: int = Field(
        primary_key=True,
        nullable=False,
        description=""
    )
    name: str = Field(
        default=None,
        nullable=True,
        description=""
    )
