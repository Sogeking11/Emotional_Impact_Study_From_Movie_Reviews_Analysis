"""
This module defines the Reviewer class.
"""

# Import packages and modules
from sqlalchemy import Column,Integer, String
from sqlalchemy.orm import relationship

from .sqlalchemyconfig import Base


# Define Reviewer table
class Reviewer(Base):
    __tablename__ = 'reviewer'

    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String(500))
    username = Column(String(45))

    # Back reference to Review table
    reviews = relationship("Review", back_populates="reviewers")



    