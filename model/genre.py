from .sqlalchemyconfig import *


# Define Country table
class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    movies = relationship("Movie" , secondary=movie_has_country_link, back_populates="genres")