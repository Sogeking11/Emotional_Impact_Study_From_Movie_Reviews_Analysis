"""
This module contains the functions to create the objects from the json files.
It is used by functions load-Movies() and load_reviews() in load_from_JsonFiles module.
"""

# import modules
from datetime import date
import logging
import sys
import json

from DB_Load.model import Movie, Country, Genre, Keyword, Prod_Company,Participant


# logger config
logger = logging.getLogger(__name__)

# creates Handlers
handler_1 = logging.FileHandler("logs/" + __name__ + ".log")
handler_2 = logging.StreamHandler() # stdout handle the log
handler_3 = logging.FileHandler("logs/errors/" + __name__ + ".log")


# setting handlers
handler_1.setLevel(logging.DEBUG)
handler_2.setLevel(logging.ERROR)
handler_3.setLevel(logging.ERROR)

# logger level
logger.setLevel(logging.DEBUG)

# formatters + adding them on handlers
formatter_1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter_2 = logging.Formatter('%(levelname)s - %(message)s')
formatter_3 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler_1.setFormatter(formatter_1)
handler_2.setFormatter(formatter_2)
handler_3.setFormatter(formatter_3)
logger.addHandler(handler_1)
logger.addHandler(handler_2)
logger.addHandler(handler_3)


def fileToJson(filePath):
    """
    This function loads a json file and returns the json object.

    Args:
        filePath (str): path of json file

    Returns:
        json_object (dict): json object of the file
    
    """
    try:

        with open(filePath, 'r', encoding='utf-8') as openfile:

            # get json object from json file
            json_object = json.load(openfile)
                
    except FileNotFoundError:
        logger.error(f"the source file {filePath} does not exist.")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"An Error occured when opening source file:\n {e}")
        sys.exit(0)
    else:
        return json_object


def movie_instance(json_object):
    """Create a Movie object from a json object

    Args:
        json_object (json): comming from json file containing movies list

    Returns:
        Movie object from sqlamlchemy mapping: image of the Movie table on DB
    """

    # parameters list init
    param_dict = {  'title': "None",
                    'certification': "None",
                    'revenue': 0,
                    'budget': 0,
                    'review_score': 0.0,
                    'popularity': 0.0,
                    'runtime': 0,
                    'synopsis': "None"
                        }
    
    for parameter in param_dict.keys():

        # In case the parameter do not exist
        value = key_exist_or_not(json_object, parameter)

        if value is not None:
            param_dict[parameter] = value


    # same treatment as above except the case on date is ''    
    myDate = key_exist_or_not(json_object, 'release_date')

    if myDate is not None and myDate != '':
        release_date = json_object['release_date']



    # Table movie
    movie_obj = Movie(title=param_dict["title"],
                      certification=param_dict["certification"],
                      revenue=param_dict["revenue"],
                      budget=param_dict["budget"],
                      review_score=param_dict["review_score"],
                      release_date=release_date,
                      popularity=param_dict["popularity"],
                      runtime=param_dict["runtime"],
                      synopsis=param_dict["synopsis"]
                      )
    
    return movie_obj

    
def which_Entity(content: str, data:str):
    """Because several table got the same structured
    this function will help makeORM_instanceList function
    to determine wich table as to be treated

    Args:
        content (str): content of the the table concerned
                        exemple "countries" for country table
        data (str):  the country

    Returns:
        object: object from sqlamlchemy mapping
    """

    # Test if the object is empty
    if data is None:
        logger.info(f"No {content} for a movie")
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


def makeORM_instanceList(json_object, tableContent: str):
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
    entity_object = key_exist_or_not(json_object, tableContent)

    # Test if the object is empty
    if entity_object is not None and len(entity_object) > 0:
        tableContent_list = entity_object
        ORMInstance_list = []
        for content in tableContent_list:
            content_obj = which_Entity(tableContent, content)
            ORMInstance_list.append(content_obj)

        return ORMInstance_list
    else:
        return None


def key_exist_or_not(object, key):
    """Care of KeyError exception.
    In this case, we assign None to parameter.
    """
    try:
        value = object[key]
    except KeyError:
        value = None
    return value

  
def role_instance(json_object, session): 
    """Create a list of Role object from a json object

    Args:
        json_object (json): comming from json file containing movies list

    Returns:
        list: list of object from sqlamlchemy mapping
    """
    role_list = []

    role_object = key_exist_or_not(json_object, 'role')

    # Test if the object is empty
    if role_object is not None:
        for role in json_object['role']:

            # init parameters before to assign them
            that_role = 'None'
            name = 'None'
            gender = 0
            popularity = 0.0

            # assign parameters
            if role['role'] is not None:
                that_role = role['role']
            if role['gender'] is not None:
                gender = role['gender']
            if role['popularity'] is not None:
                popularity = role['popularity']
            if role['name'] is not None:
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