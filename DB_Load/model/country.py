"""
This module defines the Country class.
"""

# Import packages and modules
from sqlalchemy import Column,Integer, String
from sqlalchemy.orm import relationship

from .sqlalchemyconfig import Base
from .association import movie_has_country_link


# Define Country table
class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(45))
    movies = relationship("Movie" , secondary=movie_has_country_link, back_populates="countries")