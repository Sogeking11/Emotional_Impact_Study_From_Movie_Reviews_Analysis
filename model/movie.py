from .sqlalchemyconfig import *

# Define Movie table
class Movie(Base):
    __tablename__ = 'movie'#

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    certification = Column(String(10))
    revenue = Column(Integer)
    budget = Column(Integer)
    review_score = Column(Float)
    release_date = Column(Date)
    popularity = Column(Float)
    runtime = Column(Integer)
    synopsis = Column(BLOB)
    reviews = relationship("Review", back_populates="movie")# here movie refer to parameter movie on class Review
    countries = relationship("Country", secondary=movie_has_country_ass, back_populates="movies")
