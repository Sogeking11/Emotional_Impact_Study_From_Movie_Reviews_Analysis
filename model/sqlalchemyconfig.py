from sqlalchemy import create_engine, Column, SmallInteger,Integer, BIGINT, Float, String, TEXT, BLOB, Date, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from dataset_extract_stock import loadEnv


# Create the SQLAlchemy engine and session
engine = create_engine("mysql+mysqlconnector://" + loadEnv("DB_USER")
                                                 + ":" + loadEnv("DB_PASSWORD")
                                                 + "@" + loadEnv("DB_HOST")
                                                 + ":" + loadEnv("DB_PORT") + "/"
                                                 + loadEnv("DB_NAME")
                                                 )
Session = sessionmaker(bind=engine)
session = Session()



# Declare the base class for declarative models
Base = declarative_base()

##############################
# Define associations tables #
##############################

# here between movie and country tables
movie_has_country_link = Table('movie_has_country', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('country_id', Integer, ForeignKey('country.id'))
)

# here between movie and keyword tables
movie_has_keyword_link = Table('movie_has_keyword', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('keyword_id', Integer, ForeignKey('keyword.id'))
)

# here between genre and movie tables
genre_has_movie_link = Table('genre_has_movie', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('genre_id', Integer, ForeignKey('genre.id'))
)

# here between company and movie tables
prod_company_has_movie_link = Table('prod_company_has_movie', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('prod_company_id', Integer, ForeignKey('prod_company.id'))
)