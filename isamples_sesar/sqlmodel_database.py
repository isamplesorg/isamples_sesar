from typing import Any

from sqlmodel import create_engine, SQLModel, Session


class SQLModelDAO:
    def __init__(self, db_url: str, echo: bool = False):
        self._connect_sqlmodel(db_url, echo)

    def _connect_sqlmodel(self, db_url: str, echo: bool = False):
        self.engine = create_engine(db_url, echo=echo)
        SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return Session(self.engine)


def get_sample_rows(session: Session) -> Any:
    sql = "select * from sample limit 1"
    sample_rows = session.execute(sql).fetchall()
    return sample_rows
