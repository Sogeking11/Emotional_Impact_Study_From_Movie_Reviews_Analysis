from .sqlalchemyconfig import *


# Define Reviewer table
class Reviewer(Base):
    __tablename__ = 'reviewer'

    id = Column(Integer, primary_key=True)
    url = Column(String(500))
    username = Column(String(45))
    reviews = relationship("Review", back_populates="reviewer")
    