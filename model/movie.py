from .sqlalchemyconfig import *

# Define the parent table
class Movie(Base):
    __tablename__ = 'movies'#

    id = Column(Integer, primary_key=True)
    id_imdb = Column(String(10))
    title = Column(String(100))
    production_company = Column(String(45))
    pegi = Column(Integer)
    sysnopsis = Column(BLOB)
    keywords = Column(BLOB)
    revenue = Column(Integer)
    budget = Column(Integer)
    review_score = Column(Integer)
    release_date = Column(Integer)
    reviews = relationship("Review", back_populates="movie")
