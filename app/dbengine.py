from sqlmodel import SQLModel, Session, create_engine
#from sqlalchemy.pool import NullPool

import settings


engine = create_engine(settings.get_database_url(), echo=False, future=True, pool_size=10, max_overflow=20)
#engine = create_engine(settings.get_database_url(), echo=False, future=True, poolclass=NullPool)


def get_session():
    with Session(engine) as session:
        return session
