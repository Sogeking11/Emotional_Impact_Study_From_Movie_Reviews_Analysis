from .sqlalchemyconfig import *


# Define Review table
class Source(Base):
    __tablename__ = 'source'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id'))
    name = Column(String(255))
    movie_key = Column(String(45))

    # make relation with table movie
    movie = relationship("Movie", back_populates="sources")