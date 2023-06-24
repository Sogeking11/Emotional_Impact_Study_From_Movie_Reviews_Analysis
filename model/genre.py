from .sqlalchemyconfig import *


# Define Country table
class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(45))
    movies = relationship("Movie" , secondary=genre_has_movie_link, back_populates="genres")