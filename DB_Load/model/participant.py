"""
This module defines the Participant class.
"""

# Import packages and modules
from sqlalchemy import Column,Integer, String, SmallInteger, Float
from sqlalchemy.orm import relationship

from .sqlalchemyconfig import Base


# Define Participant table
class Participant(Base):
    __tablename__ = 'participant'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(45))
    gender = Column(SmallInteger)
    popularity = Column(Float)

    # Back reference to Role table
    roles = relationship("Role", back_populates="participants")