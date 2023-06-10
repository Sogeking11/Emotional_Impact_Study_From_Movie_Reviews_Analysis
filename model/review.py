from .sqlalchemyconfig import *



class Review(Base):
    __tablename__ = 'reviews'

    id_review = Column(Integer, primary_key=True)
    text = Column(BLOB)
    Movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship("Movie", back_populates="reviews")
   