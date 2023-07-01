from datetime import date
import logging


from model import Movie, Review, Country, Reviewer, Genre, Keyword, Prod_Company, Source, Participant, Role
from model.sqlalchemyconfig import *



def data_exist(object):
    """Check if a data is not None

    Args:
        object (json): data to check

    Returns:
        bool: True if data is not None, False otherwise
    """
    
    if object is None:
        return False
    else:
        return True

def movie_instance(json_object):
    """Create a Movie object from a json object

    Args:
        json_object (json): comming from json file containing movies list

    Returns:
        Movie object from sqlamlchemy mapping: image of the Movie table on DB
    """
    # parameters initialization
    title = 'None'
    certification = 'None'
    revenue = 0
    budget = 0
    review_score = 0.0
    release_date = date(2001, 1, 1)
    popularity = 0.0
    runtime = 0
    synopsis = 'None'
    # assign parameters if possible
    if data_exist(json_object['title']):
        title = json_object['title']
        if data_exist(json_object['certification']):
            certification = json_object['certification']
        if data_exist(json_object['revenue']):
            revenue = json_object['revenue']
        if data_exist(json_object['budget']):
            budget = json_object['budget']
        if data_exist(json_object['review_score']):
            review_score = json_object['review_score']
        if data_exist(json_object['release_date']):
            release_date = json_object['release_date']
        if data_exist(json_object['popularity']):
            popularity = json_object['popularity']
        if data_exist(json_object['runtime']):
            runtime = json_object['runtime']
        if data_exist(json_object['synopsis']):
            synopsis = json_object['synopsis']
    else:
        return None

    # Table movie
    movie_obj = Movie(title=title,
                      certification=certification,
                      revenue=revenue,
                      budget=budget,
                      review_score=review_score,
                      release_date=release_date,
                      popularity=popularity,
                      runtime=runtime,
                      synopsis=synopsis
                      )
    
    return movie_obj


def source_instance(json_object, src: str):
    """Create a Source object from a json object

    Args:
        json_object (json): comming from json file containing movies list
        src (str): source name

    Returns:
        Source object from sqlamlchemy mapping: image of the Source table on DB
    """

    # parameters initialization
    movie_key = 'None'
    # assign parameters if possible
    if data_exist(json_object['id_'+ src]):
        movie_key = json_object['id_'+ src]
        source_obj = Source(name=src, movie_key=movie_key)
        # test if the movie_key is already in the database
        if session.query(Source).filter_by(movie_key=movie_key).first() is not None:
            source_obj = session.query(Source).filter_by(movie_key=movie_key).first()
        return source_obj
    else:
        return None

    
    
def which_Entity(content: str, data:str):
    """Because several table got the same strucutred
    this function will help makeORM_instance function
    to determine wich table as to be treated

    Args:
        content (str): content of the the table concerned
                        exemple "countries" for country table
        data (str):  the country

    Returns:
        object: object from sqlamlchemy mapping
    """

    # Test if the object is empty
    if data_exist(data):
        data = data
    else:
        logging.info("Object is empty")
        return None
    
    # Create object from sqlamlchemy mapping
    
    if content == 'countries':
        return Country(name=data)
    elif content == 'genres':
        return Genre(name=data)
    elif content == 'keywords':
        return Keyword(name=data)
    elif content == 'production_companies':
        return Prod_Company(name=data)
    
    return None

def makeORM_instance(json_object, tableContent: str):
    """Create a list of ORM object from a json object
    that function is designed to care of Country, Genre, 
    Keyword, Prod_Company entities.

    Args:
        json_object (json): comming from json file containing movies list
        tableContent (str): content of the the table concerned
                        exemple "countries" for country table

    Returns:
        list: list of object from sqlamlchemy mapping
    
    """
    # Test if the object is empty
    if data_exist(json_object[tableContent]):
        tableContent_list = json_object[tableContent]
        ORMInstance_list = []
        for content in tableContent_list:
            content_obj = which_Entity(tableContent, content)
            ORMInstance_list.append(content_obj)

        return ORMInstance_list
    else:
        return None
    
def role_instance(json_object): 
    """Create a list of Role object from a json object

    Args:
        json_object (json): comming from json file containing movies list

    Returns:
        list: list of object from sqlamlchemy mapping
    """
    role_list = []

    # Test if the object is empty
    if data_exist(json_object['role']):
        for role in json_object['role']:
            # init parameters before to assign them
            that_role = 'None'
            name = 'None'
            gender = 0
            popularity = 0.0
            # assign parameters
            if data_exist(role['role']):
                that_role = role['role']
            if data_exist(role['gender']):
                gender = role['gender']
            if data_exist(role['popularity']):
                popularity = role['popularity']
            if data_exist(role['name']):
                name = role['name']
            # create object datas to send them as return function
            participant_obj = Participant(name=name, gender=gender, popularity=popularity)
            if session.query(Participant).filter_by(name=name).first() is not None:
                participant_obj = session.query(Participant).filter_by(name=name).first()
            dataRole = {'role': that_role, 'participant': participant_obj}
            role_list.append(dataRole)
        return role_list      

    else:
        return None