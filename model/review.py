from .sqlalchemyconfig import *


# Define Review table
class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, autoincrement=True, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id'), primary_key=True)
    reviewer_id = Column(Integer, ForeignKey('reviewer.id'), primary_key=True)
    date = Column(Date)
    score = Column(Integer)
    url = Column(String(500))
    source = Column(String(45))
    text = Column(String(2500))

    #  4. Back reference to Reviewer and movie tables
    movies = relationship('Movie', back_populates='reviews')
    reviewers = relationship('Reviewer', back_populates='reviews')
    
    def __repr__(self):
        return f'{self.movies} {self.reviewers}'
   