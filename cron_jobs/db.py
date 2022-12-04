import os

from sqlalchemy import engine_from_config

def isDev() -> bool:
    env = os.environ['ENV']
    return env == 'dev'

def create_db_engine():
    db_config = {
        "sqlalchemy.url": os.environ['SQLALCHEMY_DATABASE_URI'],
        "sqlalchemy.pool_pre_ping": True,
        "sqlalchemy.pool_size": 10,
        "sqlalchemy.max_overflow": 2,
        "sqlalchemy.pool_recycle": 300,
        "sqlalchemy.pool_use_lifo": True
    }

    return engine_from_config(db_config, prefix="sqlalchemy", echo=isDev())

engine = create_db_engine()
