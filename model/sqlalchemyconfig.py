from sqlalchemy import create_engine, Column, SmallInteger,Integer, Float, String, BLOB, Date, ForeignKey, Table
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

# Define Rôle table
role_link_Table = Table('role', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('participant_id', Integer, ForeignKey('participant.id')),
    Column('name', String(45))
)