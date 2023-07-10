import inspect
import sys
import json
import logging

from model import Movie, Country, Genre, Keyword, Prod_Company, Role, Review, Reviewer
from datas_object import *


# logger config
logger = logging.getLogger(__name__)
handler = logging.FileHandler(__name__ + ".log")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def load_movies(jsonMovieFile: str):
    """This function loads movies and all them
    datas on to db.

    Args:
        jsonMovieFile (str): path of json movies file
    """

    #Opening JSON file
    with open(jsonMovieFile, 'r', encoding='utf-8') as openfile:

        # Reading from json file
        try:
            json_object = json.load(openfile)
        except ValueError as e:
            logging.error('invalid json: %s' % e)

    # needed for stdout info saying how many movies has been treated
    i = 0
    # go through each movie
    for OneFilm in json_object:
        
        i+=1

        # Table movie
        if movie_instance(OneFilm) is not None:
            myFilm = movie_instance(OneFilm)
            if session.query(Movie).filter_by(title=myFilm.title).first() is not None:
                myFilm = session.query(Movie).filter_by(title=myFilm.title).first()
        
        # push info in stdout
        sys.stdout.write('Film ' + str(i) + ': ' + myFilm.title + ' : Traitement\r')
        sys.stdout.flush()

        # Table source, just 2 sources possible
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
                # test to check if the country is already in the database
                if session.query(Country).filter_by(name=country.name).first() is not None: 
                    # get that country object
                    country = session.query(Country).filter_by(name=country.name).first()

                # add to the list of countries    
                myFilm.countries.append(country)

                session.add(country)

        # Table prod_company
        if makeORM_instance(OneFilm, 'production_companies') is not None:
            prod_companies_list = makeORM_instance(OneFilm, 'production_companies')
            for prod_company in prod_companies_list:
                # test to check if the production company is already in the database
                if session.query(Prod_Company).filter_by(name=prod_company.name).first() is not None: 
                    # get that production company object
                    prod_company = session.query(Prod_Company).filter_by(name=prod_company.name).first()
                myFilm.prod_companies.append(prod_company)
                session.add(prod_company)

        # Table keyword
        if makeORM_instance(OneFilm, 'keywords') is not None:
            keywords_list = makeORM_instance(OneFilm, 'keywords')
            for keyword in keywords_list:
                # test to check if the keyword is already in the database
                if session.query(Keyword).filter_by(name=keyword.name).first() is not None: 
                    # get that keyword object
                    keyword = session.query(Keyword).filter_by(name=keyword.name).first()
                myFilm.keywords.append(keyword)
                session.add(keyword)

        # Table genre
        if makeORM_instance(OneFilm, 'genres') is not None:
            genres_list = makeORM_instance(OneFilm, 'genres')
            for genre in genres_list:
                # test to check if the genre is already in the database
                if session.query(Genre).filter_by(name=genre.name).first() is not None: 
                    # get that genre object
                    genre = session.query(Genre).filter_by(name=genre.name).first()
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

        # clean stdout
        sys.stdout.write('              '*10 + '\r')
        sys.stdout.flush()


def load_reviews(file_name):
    """This function will load on db reviews as they are
    well structured.
    It start by search if the movie exist and if it exist so 
    it will send on db review and the reviewers of the review if they
    don't exist.

    Args:
        file_name (str): the path to the json reviews restructured file
    """

    #Opening JSON file
    with open(file_name, 'r', encoding='utf-8') as openfile:

        # Reading from json file
        try:
            json_object = json.load(openfile,)
        except ValueError as e:
            logger.exception('invalid json: ')


    # needed for stdout info saying how many reviews have been treated
    cmpt = 1
    # go through each movie
    for movie_key in json_object:

        # go through each review
        for aReview in json_object[movie_key]:

            # push info in stdout
            sys.stdout.write('Review number : ' + str(cmpt) + ' from movie source : ' + movie_key + ' in operation.\r')
            sys.stdout.flush()

            # check if movie exist in the database
            if session.query(Source).filter_by(movie_key=movie_key).first() is not None:
                mySource = session.query(Source).filter_by(movie_key=movie_key).first()

                # get movie object to help create Review object in case of review does not exist
                try:
                    myMovie = session.query(Movie).filter_by(id=mySource.movie_id).first()
                except Exception as e:
                    logger.exception('invalid movie')

                # check if the review exist by using its url
                if session.query(Review).filter_by(url=aReview['url']).first() is None:
                    # check if the reviewer exist by using its username
                    if session.query(Reviewer).filter_by(username=aReview['username']).first() is None:
                        # create a new reviewer
                        try:
                            myReviewer = Reviewer(username=aReview['username'], url=aReview['user_url'])
                        except Exception as e:
                            logger.error('could not create new reviewer')
                    else:
                        # get the reviewer id
                        try:
                            myReviewer = session.query(Reviewer).filter_by(username=aReview['username']).first()
                        except Exception as e:
                            logger.exception('could not get the Reviewer object')

                    # create a new review
                    myReview = Review(
                                        url=aReview['url'],
                                        text=aReview['text'],
                                        score=aReview['score'],
                                        source=aReview['source'],
                                        date=aReview['date'],
                                        reviewers=myReviewer,
                                        movies=myMovie
                                    )
                    
                    # add the review to the database
                    session.add(myReview)
                    session.commit()

            else:
                logger.error(f'Source movie not found : {movie_key}', exc_info=True)
            
            # one more review has been treated
            cmpt += 1
            # clean stdout
            sys.stdout.write('              '*10 + '\r')
            sys.stdout.flush()