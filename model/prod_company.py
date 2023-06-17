from .sqlalchemyconfig import *


# Define Country table
class Prod_Company(Base):
    __tablename__ = 'prod_company'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    movies = relationship("Movie" , secondary=prod_company_has_movie_link, back_populates="prod_companies")