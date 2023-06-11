from .sqlalchemyconfig import *


# Define Review table
class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id'))
    reviewer_id = Column(Integer, ForeignKey('reviewer.id'))
    date = Column(Date)
    score = Column(Integer)
    url = Column(String(500))
    source = Column(String(255))
    text = Column(BLOB)

    # make relation with table movie on the hand and reviewer on the other hand
    movie = relationship("Movie", back_populates="reviews")
    reviewer = relationship("Reviewer", back_populates="reviews")
   