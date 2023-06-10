from sqlalchemy import create_engine, Column, Integer, String, BLOB, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Create the SDLAlchemy engine and session
engine = create_engine("mysql+mysqlconnector://db_lm:131272@51.254.205.197:3306/CINEMOTION")
Session = sessionmaker(bind=engine)
session = Session()

# Declare the base class for declarative models
Base = declarative_base()

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

# Define the child table
class Review(Base):
    __tablename__ = 'reviews'#

    id_review = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    text = Column(BLOB)
    movie = relationship("Movie", back_populates="reviews")#


Base.metadata.create_all(engine)

#Movie.reviews = relationship("Review", order_by = Review.id_review, back_populates = "movie")

myBlob1 = b'Il etait une fois..'
myBlob2 = b"Marechaux, villipendie, restroctirazion"


movie = Movie(
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

review1 = Review(text=b"Hello de Lu", movie=movie)
review2 = Review(text=b"congratulation...", movie=movie)


session.add(movie)
session.add(review1)
session.add(review2)
session.commit()