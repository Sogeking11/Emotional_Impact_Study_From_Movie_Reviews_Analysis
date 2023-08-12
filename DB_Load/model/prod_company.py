"""
This module defines the Prod_Company class.
"""

# Import packages and modules
from sqlalchemy import Column,Integer, String
from sqlalchemy.orm import relationship

from .sqlalchemyconfig import Base
from .association import prod_company_has_movie_link


# Define Prod_Company table
class Prod_Company(Base):
    __tablename__ = 'prod_company'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    movies = relationship("Movie" , secondary=prod_company_has_movie_link, back_populates="production_companies")