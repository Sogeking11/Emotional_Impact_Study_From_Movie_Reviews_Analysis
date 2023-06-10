from sqlalchemy import create_engine, Column, Integer, String, BLOB, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import dataset_extract_stock.mySecrets as s



engine = create_engine("mysql+mysqlconnector://" + s.DATABASE_USER
                                                 + ":" + s.DATABASE_PASSWORD
                                                 + "@" + s.DATABASE_HOST
                                                 + ":" + s.DATABASE_PORT + "/"
                                                 + "CINEMOTION"
                                                 )



Base = declarative_base()


Session = sessionmaker(bind=engine)
session = Session()