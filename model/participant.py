from .sqlalchemyconfig import *


# Define Country table
class Participant(Base):
    __tablename__ = 'participant'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    gender = Column(SmallInteger)
    movies = relationship("Movie" , secondary=role_link_Table, back_populates="participants")