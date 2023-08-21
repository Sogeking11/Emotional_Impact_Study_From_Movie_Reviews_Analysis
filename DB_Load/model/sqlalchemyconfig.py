"""
This module contains the SQLAlchemy configuration to get a session.
get_session function is used to query the database.
"""

# Import the necessary libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from loadEnv import loadEnv


# Create the SQLAlchemy engine
engine = create_engine("mysql+mysqlconnector://" + loadEnv("DB_USER")
                                                + ":" + loadEnv("DB_PASSWORD")
                                                + "@" + loadEnv("DB_HOST")
                                                + ":" + loadEnv("DB_PORT") + "/"
                                                + loadEnv("DB_NAME")
                                                )



# Declare the base class for declarative models
Base = declarative_base()

def get_session() -> sessionmaker:
    """
    This function returns a session to query the database.
    :return: session
    """



    # Create the tables in the database if doesn't exist
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session