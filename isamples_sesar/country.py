from sqlmodel import Field, SQLModel


class Country(SQLModel, table=True):
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
