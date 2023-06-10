from .sqlalchemyconfig import *



class Review(Base):
    __tablename__ = 'review'

    id_review = Column(Integer, primary_key=True)
    text = Column(BLOB)
    Movie_id = Column(Integer, ForeignKey('movie.id'))
    movie = relationship("Movie", back_populates="reviews")
   