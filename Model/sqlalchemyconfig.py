from sqlalchemy import create_engine, Column, Integer, String, BLOB, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base



engine = create_engine("mysql+mysqlconnector://db_lm:131272@51.254.205.197:3306/CINEMOTION")

Base = declarative_base()


Session = sessionmaker(bind=engine)
session = Session()