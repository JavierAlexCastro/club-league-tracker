import os

from sqlalchemy import engine_from_config

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
        f"{config_prefix}pool_recycle": 300,
        f"{config_prefix}pool_use_lifo": True
    }

    return engine_from_config(db_config, prefix=config_prefix, echo=isDev())

engine = create_db_engine()
