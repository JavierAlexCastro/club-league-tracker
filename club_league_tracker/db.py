import os

from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def create_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import club_league_tracker.models.db
    Base.metadata.create_all(bind=engine)

def isDev() -> bool:
    env = os.environ['ENV']
    return env == 'dev'

def create_db_engine():
    config_prefix = "db."
    db_config = {
        f"{config_prefix}url": os.environ['SQLALCHEMY_DATABASE_URI'],
        f"{config_prefix}pool_pre_ping": True,
        f"{config_prefix}pool_size": 10,
        f"{config_prefix}max_overflow": 2,
        f"{config_prefix}pool_recycle": 3600,
        f"{config_prefix}pool_use_lifo": True
    }

    return engine_from_config(db_config, prefix=config_prefix, echo=isDev())

engine = create_db_engine()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
