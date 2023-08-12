"""
This module defines the Genre class.
"""

# Import packages and modules
from sqlalchemy import Column,Integer, String
from sqlalchemy.orm import relationship

from .sqlalchemyconfig import Base
from .association import genre_has_movie_link


# Define Genre table
class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(45))
    movies = relationship("Movie" , secondary=genre_has_movie_link, back_populates="genres")