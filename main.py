import sys
import json
import logging

from model import Movie, Source, Review, Reviewer
from model.sqlalchemyconfig import *
from load_from_JsonMovies import load_movies
from restruct_redaJsonFile import restruct_redaJsonFile








if __name__ == '__main__':

     # Create the tables in the database
    Base.metadata.create_all(engine)

    # Load the data from the json file
    #load_movies('datas/test.json')

    # Reviews data restructuring
    #restruct_redaJsonFile('datas/test_reviews.json')

    #Opening JSON file
    with open('datas/test_reviews_restructured.json', 'r', encoding='utf-8') as openfile:

        # Reading from json file
        try:
            json_object = json.load(openfile,)
        except ValueError as e:
            logging.error('invalid json: %s' % e)

    # go through each movie
    # for movie in json_object:
    movieOne = json_object['tt5433140']
    reviewOne = movieOne[0]

    if session.query(Source).filter_by(movie_key='tt5433140').first() is not None:
        mySource = session.query(Source).filter_by(movie_key='tt5433140').first()
        # get movie id for the review
        movie_id = mySource.movie_id

        # check if the review exist by using its url
        if session.query(Review).filter_by(url=reviewOne['url']).first() is None:
            # create a new review
            myReview = Review(movie_id=movie_id, url=reviewOne['url'],
                              text=reviewOne['text'], rating=reviewOne['rating'])
            # add the review to the database
            session.add(myReview)
            session.commit()


    