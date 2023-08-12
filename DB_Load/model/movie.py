"""
This module defines the Movie class.
"""

# Import packages and modules
from sqlalchemy import Column,Integer, String, BIGINT, Float, Date
from sqlalchemy.orm import relationship

from .sqlalchemyconfig import Base


from .association import movie_has_country_link, movie_has_keyword_link, genre_has_movie_link, prod_company_has_movie_link

# Define Movie table
class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(100))
    certification = Column(String(10))
    revenue = Column(BIGINT)
    budget = Column(Integer)
    review_score = Column(Float)
    release_date = Column(Date)
    popularity = Column(Float)
    runtime = Column(Integer)
    synopsis = Column(String(1000))

    # relationships
    sources = relationship("Source", back_populates="movie")
    reviews = relationship("Review", back_populates="movies")
    roles = relationship("Role", back_populates="movies")
    countries = relationship("Country", secondary=movie_has_country_link, back_populates="movies")
    keywords = relationship("Keyword", secondary=movie_has_keyword_link, back_populates="movies")
    genres = relationship("Genre", secondary=genre_has_movie_link, back_populates="movies")
    production_companies = relationship("Prod_Company", secondary=prod_company_has_movie_link, back_populates="movies")