from typing import Any, Optional
from datetime import datetime

from sqlmodel import create_engine, Session, select
from isamples_sesar.sample import Sample


class SQLModelDAO:
    def __init__(self, db_url: str, echo: bool = False):
        self._connect_sqlmodel(db_url, echo)

    def _connect_sqlmodel(self, db_url: str, echo: bool = False):
        self.engine = create_engine(db_url, echo=echo)
        # SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return Session(self.engine)


def get_sample_rows(session: Session, offset: int = 0, limit: int = 1000, last_update_date: Optional[datetime] = None) -> Any:
    if last_update_date is not None:
        statement = (
            select(Sample).filter(Sample.last_update_date >= last_update_date).order_by(Sample.sample_id).offset(offset).limit(limit)
        )
    else:
        statement = (
            select(Sample).order_by(Sample.sample_id).offset(offset).limit(limit)
        )
    results = session.exec(statement).all()
    return results


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
