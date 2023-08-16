"""
This module defines the Keyword class.
"""

# Import packages and modules
from sqlalchemy import Column,Integer, String
from sqlalchemy.orm import relationship

from .sqlalchemyconfig import Base
from .association import movie_has_keyword_link

# Define Keyword table
class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    movies = relationship("Movie" , secondary=movie_has_keyword_link, back_populates="keywords")