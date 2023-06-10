from .sqlalchemyconfig import *


Base = declarative_base()


class Review(Base):
    __tablename__ = 'review'

    id_review = Column(Integer, primary_key=True)
    id_imdb = Column(String(10))
    text = Column(BLOB)
   