from datetime import date
import pandas as pd
import json

from model import Movie, Review, Country, Reviewer, Genre, Keyword, Prod_Company, Source, Participant, Role
from model.sqlalchemyconfig import *

def movieEntity(json_object):
    # Table movie
    movie{
        "title"=json_object['title'],
        original_title=json_object['original_title'],
        original_language=json_object['original_language'],
        overview=json_object['overview'],
        popularity=json_object['popularity'],
        release_date=json_object['release_date'],
        poster_path=json_object['poster_path'],
        adult=json_object['adult'],
        backdrop_path=json_object['backdrop_path'],
        vote_average=json_object['vote_average'],
        vote_count=json_object['vote_count'],
        budget=json_object['budget'],
        revenue=json_object['revenue'],
        runtime=json_object['runtime'],
        status=json_object['status'],
        tagline=json_object['tagline'],
        imdb_id=json_object['imdb_id'],
        imdb_score=json_object['imdb_score']
    }



if __name__ == '__main__':
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
    myFilm = movieEntity(OneFilm)
