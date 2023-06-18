from .sqlalchemyconfig import *

# Define Movie table
class Movie(Base):
    __tablename__ = 'movie'#

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(100))
    certification = Column(String(10))
    revenue = Column(Integer)
    budget = Column(Integer)
    review_score = Column(Float)
    release_date = Column(Date)
    popularity = Column(Float)
    runtime = Column(Integer)
    synopsis = Column(BLOB)

    # relationships
    sources = relationship("Source", back_populates="movie")
    #reviews = relationship("Review", back_populates="movie")# here movie refer to parameter movie on class Review
    reviewers = relationship("Reviewer", secondary='review', back_populates="movies")
    countries = relationship("Country", secondary=movie_has_country_link, back_populates="movies")
    keywords = relationship("Keyword", secondary=movie_has_keyword_link, back_populates="movies")
    genres = relationship("Genre", secondary=genre_has_movie_link, back_populates="movies")
    prod_companies = relationship("Prod_Company", secondary=prod_company_has_movie_link, back_populates="movies")
    participants = relationship("Participant", secondary=role_link_Table, back_populates="movies")