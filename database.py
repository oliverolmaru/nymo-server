from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = """postgres:///postgres
#   ?host=/cloudsql/nymo-server:europe-central2:nymo-server-db
#   &user=postgres
#   &password=dqkEfgBoCkxNd7wk
#   &sslmode=disable"""
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://d100646_arendaja:SWdvDdgQF5wQ5A0f@d100646.mysql.zonevs.eu/d100646_asv?use_unicode=1&charset=utf8"
#SQLALCHEMY_DATABASE_URL = "postgres://postgres:dqkEfgBoCkxNd7wk@34.118.97.115"
#SQLALCHEMY_DATABASE_URL = "postgres://postgres:nymoserver@localhost"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()