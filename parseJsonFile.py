from datetime import date
import pandas as pd
import json
import logging

from model import Movie, Review, Country, Reviewer, Genre, Keyword, Prod_Company, Source, Participant, Role
from model.sqlalchemyconfig import *

## Define logging
logging.basicConfig(level=logging.INFO,
                    filename="log.log",
                    filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

def data_exist(object):
    if object is None:
        return False
    else:
        return True

def movie_instance(json_object):
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
        logging.info("Movie object is empty")
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
    # Test if the object is empty
    if data_exist(json_object['id_'+ src]):
        movie_key = json_object['id_'+ src]
        source_obj = Source(name=src, movie_key=movie_key)
        return source_obj
    else:
        return None
    
def which_Entity(content: str, data:str):
    if content == 'countries':
        return Country(name=data)
    elif content == 'genres':
        return Genre(name=data)
    elif content == 'keywords':
        return Keyword(name=data)
    elif content == 'production_companies':
        return Prod_Company(name=data)
    
    return None

# care of Country, Genre, Keyword, Prod_Company entities
def makeORM_instance(json_object, tableContent: str):
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
    # Test if the object is empty
    role_list = []
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
            if data_exist(role['name']):
                name = role['name']
            if data_exist(role['gender']):
                gender = role['gender']
            if data_exist(role['popularity']):
                popularity = role['popularity']
            # create object datas to send them as return function
            participant_obj = Participant(name=name, gender=gender, popularity=popularity)
            dataRole = {'role': that_role, 'participant': participant_obj}
            role_list.append(dataRole)
        return role_list      

    else:
        return None


if __name__ == '__main__':

     # Create the tables in the database
    Base.metadata.create_all(engine)

    #Opening JSON file
    with open('datas/test.json', 'r', encoding='utf-8') as openfile:

        # Reading from json file
        try:
            json_object = json.load(openfile,)
        except ValueError as e:
            print('invalid json: %s' % e)

    # try with one film to start
    OneFilm = json_object[0]

    # Table movie
    if movie_instance(OneFilm) is not None:
        myFilm = movie_instance(OneFilm)

    # Table source
    if source_instance(OneFilm, 'imdb') is not None:
        mySource1 = source_instance(OneFilm, 'imdb')
        myFilm.sources.append(mySource1)
        session.add(mySource1)

    if source_instance(OneFilm,'tmdb') is not None:
        mySource2 = source_instance(OneFilm,'tmdb')
        myFilm.sources.append(mySource2)
        session.add(mySource2)

    # Table country
    if makeORM_instance(OneFilm, 'countries') is not None:
        countries_list = makeORM_instance(OneFilm, 'countries')
        for country in countries_list:
            myFilm.countries.append(country)
            session.add(country)

    # Table prod_company
    if makeORM_instance(OneFilm, 'production_companies') is not None:
        prod_companies_list = makeORM_instance(OneFilm, 'production_companies')
        for prod_company in prod_companies_list:
            myFilm.prod_companies.append(prod_company)
            session.add(prod_company)

    # Table keyword
    if makeORM_instance(OneFilm, 'keywords') is not None:
        keywords_list = makeORM_instance(OneFilm, 'keywords')
        for keyword in keywords_list:
            myFilm.keywords.append(keyword)
            session.add(keyword)

    # Table genre
    if makeORM_instance(OneFilm, 'genres') is not None:
        genres_list = makeORM_instance(OneFilm, 'genres')
        for genre in genres_list:
            myFilm.genres.append(genre)
            session.add(genre)
    
    # Tables participant and role
    if role_instance(OneFilm) is not None:
        for role in role_instance(OneFilm):
            myRole = Role(movies=myFilm, name=role['role'], participants=role['participant'])
            session.add(myRole)

    # Add to database
    session.add(myFilm)
    session.commit()
    
