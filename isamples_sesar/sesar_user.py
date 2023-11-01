from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship
from .sesar_sqlmodel import SesarBase

if TYPE_CHECKING:
    from .sample import Sample


class Sesar_User(SesarBase, table=True):
    sesar_user_id: int = Field(
        primary_key=True,
        nullable=False,
        description=""
    )
    fname: str = Field(
        default=None,
        nullable=True,
        description=""
    )
    lname: str = Field(
        default=None,
        nullable=True,
        description=""
    )
    email: Optional[str] = Field(
        default=None,
        nullable=True,
        description=""
    )
    cur_registrant_samples: Optional[List["Sample"]] = Relationship(
        back_populates="cur_registrant",
        sa_relationship_kwargs={
            "primaryjoin": "Sesar_User.sesar_user_id==Sample.cur_registrant_id"
        }
    )
    cur_owner_samples: Optional[List["Sample"]] = Relationship(
        back_populates="cur_owner",
        sa_relationship_kwargs={
            "primaryjoin": "Sesar_User.sesar_user_id==Sample.cur_owner_id"
        }
    )
    orig_owner_samples: Optional[List["Sample"]] = Relationship(
        back_populates="orig_owner",
        sa_relationship_kwargs={
            "primaryjoin": "Sesar_User.sesar_user_id==Sample.orig_owner_id"
        }
    )
