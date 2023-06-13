from .sqlalchemyconfig import *


# Define Keyword table
class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    movies = relationship("Movie" , secondary=movie_has_keyword_link, back_populates="keywords")