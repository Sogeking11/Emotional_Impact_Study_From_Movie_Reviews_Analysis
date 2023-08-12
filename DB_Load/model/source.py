"""
This module defines the Source class.
"""

# Import packages and modules
from sqlalchemy import Column,Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .sqlalchemyconfig import Base


# Define Source table
class Source(Base):
    __tablename__ = 'source'

    id = Column(Integer, autoincrement=True, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id'))
    name = Column(String(45))
    movie_key = Column(String(45))

    # make relation with table movie
    movie = relationship("Movie", back_populates="sources")