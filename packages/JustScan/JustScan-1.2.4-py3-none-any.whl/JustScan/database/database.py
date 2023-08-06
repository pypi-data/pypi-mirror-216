from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from JustScan.config.config_db import SettingLocal, SettingDev

setting = SettingDev()

SQLALCHEMY_DATABASE_URL = URL.create(
    "postgresql",
    username=setting.USERNAME_,
    password=setting.PASSWORD,
    host=setting.HOST,
    database=setting.DATABASE,
    port=setting.PORT
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
Session = sessionmaker(bind=engine)

Base = declarative_base()
