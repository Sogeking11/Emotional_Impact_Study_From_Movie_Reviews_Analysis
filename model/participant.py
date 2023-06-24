from .sqlalchemyconfig import *


# Define Country table
class Participant(Base):
    __tablename__ = 'participant'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    gender = Column(SmallInteger)
    roles = relationship("Role", back_populates="participants")