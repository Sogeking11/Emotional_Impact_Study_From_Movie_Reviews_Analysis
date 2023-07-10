from .sqlalchemyconfig import *

# Define Rôle table
class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, autoincrement=True, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id'), primary_key=True)
    participant_id = Column(Integer, ForeignKey('participant.id'), primary_key=True)
    name = Column(String(45))

    # Back reference to Movie and Participant tables
    movies = relationship('Movie', back_populates='roles')
    participants = relationship('Participant', back_populates='roles')

    def __repr__(self):
        return f'{self.movies} {self.participants}'