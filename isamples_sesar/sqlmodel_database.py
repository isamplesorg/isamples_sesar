from typing import Any, Optional

from sqlmodel import create_engine, Session, select
from sqlalchemy import text
from isamples_sesar.sample import Sample
# from isamples_sesar.classification import Classification
# from isamples_sesar.country import Country
# from isamples_sesar.launch_type import Launch_Type
# from isamples_sesar.nav_type import Nav_Type
# from isamples_sesar.sample_additional_name import Sample_Additional_Name
# from isamples_sesar.sample_type import Sample_Type
# from isamples_sesar.sesar_user import Sesar_User


class SQLModelDAO:
    def __init__(self, db_url: str, echo: bool = False):
        self._connect_sqlmodel(db_url, echo)

    def _connect_sqlmodel(self, db_url: str, echo: bool = False):
        self.engine = create_engine(db_url, echo=echo)
        # SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return Session(self.engine)


def get_sample_rows(session: Session) -> Any:
    sql = text("select * from sample limit 1")
    sample_rows = session.execute(sql).fetchall()
    return sample_rows


def get_sample_with_id(session: Session, sample_id: int) -> Optional[Sample]:
    statement = (
        select(Sample).filter(Sample.sample_id == sample_id)
    )
    result = session.exec(statement).first()
    return result


def get_sample_with_igsn(session: Session, igsn: str) -> Optional[Sample]:
    statement = (
        select(Sample).filter(Sample.igsn == igsn)
    )
    result = session.exec(statement).first()
    return result
