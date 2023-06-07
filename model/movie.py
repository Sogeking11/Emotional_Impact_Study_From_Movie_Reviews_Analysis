from sqlalchemy import create_engine, Column, Integer, String, BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine("mysql+mysqlconnector://db_lm:131272@51.254.205.197:3306/CINEMOTION")


"""
metadata = db.MetaData() # extracting the metadata
review = db.Table('movie', metadata, autoload=True, autoload_with=engine)

print(repr(metadata.tables['movie']))
"""

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

session.add(movie1)
session.commit()