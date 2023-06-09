from sqlalchemy import create_engine, Column, Integer, String, BLOB, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine("mysql+mysqlconnector://db_lm:131272@51.254.205.197:3306/CINEMOTION")


Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movie'

    id_movie = Column(Integer, primary_key=True)
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


class Review(Base):
    __tablename__ = 'review'

    id_review = Column(Integer, primary_key=True)
    movie_id_movie = Column(Integer, ForeignKey('movie.id_movie'))
    text = Column(BLOB)
    movie = relationship("Movie", back_populates="review")

Movie.review = relationship("Review", order_by = Review.id_review, back_populates = "movie")

myBlob1 = b'Il etait une fois..'
myBlob2 = b"Marechaux, villipendie, restroctirazion"


movie1 = Movie(
                    id_imdb='tt34535',
                    title='Vorch',
                    production_company='Warner Bross',
                    pegi='18',
                    sysnopsis=myBlob1,
                    keywords=myBlob2,
                    revenue=8,
                    budget=75,
                    review_score=5,
                    release_date=2002
                )

review1 = Review(text=b"Hello de Lu", movie=movie1)
review2 = Review(text=b"congratulation...", movie=movie1)


session.add(movie1)
session.add(review1)
session.add(review2)
session.commit()