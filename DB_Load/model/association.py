"""
This module defines the association tables between different tables
"""

# Import packages and modules
from sqlalchemy import Column, Integer, ForeignKey, Table

from .sqlalchemyconfig import Base



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