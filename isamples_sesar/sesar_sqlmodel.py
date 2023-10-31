from sqlalchemy.orm import registry
from sqlmodel import SQLModel


class SesarBase(SQLModel, registry=registry()):
    pass
