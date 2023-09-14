from sqlmodel import Field, SQLModel


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
