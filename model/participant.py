from .sqlalchemyconfig import *


# Define Country table
class Participant(Base):
    __tablename__ = 'participant'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(45))
    gender = Column(SmallInteger)
    popularity = Column(Float)

    # Back reference to Role table
    roles = relationship("Role", back_populates="participants")