from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_wrapper import SQLAlchemy
from environs import Env

env = Env()
env.read_env()
db = SQLAlchemy(uri=env("SQLALCHEMY_DATABASE_URI"))
Base = declarative_base()
