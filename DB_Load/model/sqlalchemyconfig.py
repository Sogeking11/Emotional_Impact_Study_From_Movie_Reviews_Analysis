"""
This module contains the SQLAlchemy configuration to get a session.
get_session function is used to query the database.
"""

# Import the necessary libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from loadEnv import loadEnv

from google.cloud.sql.connector import Connector

# Init google connector
connector = Connector()


# Declare the base class for declarative models
Base = declarative_base()

# credentials defined in google cloud
def getconn():
    """It helps to get connection from db

    Returns:
        db connection: connection from GCP Cloud sql
    """
    conn = connector.connect(
        loadEnv("INSTANCE_CONNECTION_NAME"),
        "pymysql",
        user=loadEnv("DB_USER"),
        password=loadEnv("DB_PASS"),
        db=loadEnv("DB_NAME")

    )
    return conn

# Create the SQLAlchemy engine with pymysql as google example
engine = create_engine("mysql+pymysql://", 
                       creator = getconn,
)

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