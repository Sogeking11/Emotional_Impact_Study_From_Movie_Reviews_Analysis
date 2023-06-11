from sqlalchemy import create_engine, Column, Integer, Float, String, BLOB, Date, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import dataset_extract_stock.mySecrets as s


# Create the SQLAlchemy engine and session
engine = create_engine("mysql+mysqlconnector://" + s.DATABASE_USER
                                                 + ":" + s.DATABASE_PASSWORD
                                                 + "@" + s.DATABASE_HOST
                                                 + ":" + s.DATABASE_PORT + "/"
                                                 + "CINEMOTION"
                                                 )
Session = sessionmaker(bind=engine)
session = Session()



# Declare the base class for declarative models
Base = declarative_base()


# Define association table
movie_has_country_ass = Table('movie_has_country', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('country_id', Integer, ForeignKey('country.id'))
)