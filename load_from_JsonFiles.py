import sys
import json
import logging
from pathlib import Path

from model import Movie, Country, Genre, Keyword, Prod_Company, Role, Review, Reviewer
from datas_object import *

# data dir path
data_dir = Path("datas")

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
        logger.error(f"the file {filePath} does not exist.")
        sys.exit(0)
        
    except Exception as e:
        logger.error("An Error occured", str(e))
        sys.exit(0)
    else:
        return json_object
    


def load_movies(jsonMovieFile: Path):
    """This function loads movies and all their
    datas into db.

    Args:
        jsonMovieFile (str): path of json movies file
    """

    #Opening JSON file

    # test logger
    logger.info('Send Movies to DB')

    # get json object from file
    json_object = fileToJson(jsonMovieFile)

    # needed for stdout info saying how many movies has been treated
    i = 0
    # go through each movie
    for OneFilm in json_object:
        
        i+=1

        # Table movie
        myFilm = movie_instance(OneFilm)

        # check if movie exist on db passing by source table
        try:
            mySource = session.query(Source).filter_by(movie_key=OneFilm['id_imdb']).first()
        except:
            logger.warning('No source for this film', OneFilm['id_imdb'])
            continue

        if mySource is not None:
            # get movie object to use it
            myFilm = session.query(Movie).filter_by(id=mySource.movie_id).first()


        
        # push info in stdout
        sys.stdout.write('Film ' + str(i) + '\\' + str(len(json_object)) + ': ' + str(OneFilm['title']) + ' : Traitement\r')
        sys.stdout.flush()

        # Table source, just 2 sources possible
        try:
            if source_instance(OneFilm, 'imdb') is not None:
                mySource1 = source_instance(OneFilm, 'imdb')
                myFilm.sources.append(mySource1)
                session.add(mySource1)
        except:
            logging.warning('No imdb source for this film')


        try:
            if source_instance(OneFilm,'tmdb') is not None:
                mySource2 = source_instance(OneFilm,'tmdb')
                myFilm.sources.append(mySource2)
                session.add(mySource2)
        except:
            logging.warning('No tmdb source for this film')

        # Table country
        try:
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
        except:
            logging.warning('No countries for this film')


        # Table prod_company
        try:
            if makeORM_instance(OneFilm, 'production_companies') is not None:
                prod_companies_list = makeORM_instance(OneFilm, 'production_companies')
                for prod_company in prod_companies_list:
                    # test to check if the production company is already in the database
                    if session.query(Prod_Company).filter_by(name=prod_company.name).first() is not None: 
                        # get that production company object
                        prod_company = session.query(Prod_Company).filter_by(name=prod_company.name).first()
                    myFilm.prod_companies.append(prod_company)
                    session.add(prod_company)
        except:
            logging.warning('No production companies for this film')

        # Table keyword
        try:
            if makeORM_instance(OneFilm, 'keywords') is not None:
                keywords_list = makeORM_instance(OneFilm, 'keywords')
                for keyword in keywords_list:
                    # test to check if the keyword is already in the database
                    if session.query(Keyword).filter_by(name=keyword.name).first() is not None: 
                        # get that keyword object
                        keyword = session.query(Keyword).filter_by(name=keyword.name).first()
                    myFilm.keywords.append(keyword)
                    session.add(keyword)
        except:
            logging.warning('No keywords for this film')

        # Table genre
        try:
            if makeORM_instance(OneFilm, 'genres') is not None:
                genres_list = makeORM_instance(OneFilm, 'genres')
                for genre in genres_list:
                    # test to check if the genre is already in the database
                    if session.query(Genre).filter_by(name=genre.name).first() is not None: 
                        # get that genre object
                        genre = session.query(Genre).filter_by(name=genre.name).first()
                    myFilm.genres.append(genre)
                    session.add(genre)
        except:
            logging.warning('No genres for this film')
        
        # Tables participant and role
        try:
            if role_instance(OneFilm) is not None:
                for role in role_instance(OneFilm):
                    myRole = Role(movies=myFilm, name=role['role'], participants=role['participant'])
                    session.add(myRole)
        except:
            logging.warning('No participants for this film')

        # Add to database
        try:
            session.add(myFilm)
            session.commit()
        except:
            logger.exception('invalid movie', OneFilm['id_imdb'])
            logger.info('invalid movie', OneFilm['id_imdb'])

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

            # check if movie exist in the database if not do nothing
            if session.query(Source).filter_by(movie_key=movie_key).first() is not None:
                mySource = session.query(Source).filter_by(movie_key=movie_key).first()

                # get movie object to help create Review object in case of review does not exist
                try:
                    myMovie = session.query(Movie).filter_by(id=mySource.movie_id).first()
                except Exception as e:
                    logger.exception('invalid movie')

                # check if the review exist in db by using its url
                try:
                    if session.query(Review).filter_by(url=aReview['url']).first() is None:

                        # here we must define if it's from Dataset or from scrap
                        if aReview['url'] == "From_DataSet":

                            # need to get the fake reviewer if exist (cf: dataset)
                            if session.query(Reviewer).filter_by(url="From_DataSet").first() is not None:

                                # Here to prepare reviewer from dataset reviewer and review datas objects
                                try:
                                    myReviewer = session.query(Reviewer).filter_by(url="From_DataSet").first()
                                except Exception as e:
                                    logger.error('could not get Dataset Reviewer object')
                                
                                # preparing review datas that are not in json object

                            else:
                                # Dataset reviewer must be created   
                                myReviewer = Reviewer(username="XXXXXXXXXXXX", url="From_DataSet")

                            # datas Review object
                            aReview['url'] = "From_DataSet"
                            aReview['username'] = "From_DataSet"
                            aReview['user_url'] = "From_DataSet"
                            aReview['source'] = "imdb"
                            aReview['date'] = date(2050,1,1)


                        else:
                            # Here to prepare reviewer and review datas objects 
                            try:
                                myReviewer = Reviewer(username=aReview['username'], url=aReview['user_url'])
                            except Exception as e:
                                logger.exception('could not create new reviewer')

                    else:

                        # here we must define if it's from Dataset or from scrap
                        if aReview['url'] == "From_DataSet":

                            # need to get the fake reviewer if exist (cf: dataset)
                            if session.query(Reviewer).filter_by(url="From_DataSet").first() is not None:

                                # Here to prepare reviewer from dataset reviewer and review datas objects
                                try:
                                    myReviewer = session.query(Reviewer).filter_by(url="From_DataSet").first()
                                except Exception as e:
                                    logger.error('could not get Dataset Reviewer object')
                                
                                # preparing review datas that are not in json object

                            else:
                                # Dataset reviewer must be created   
                                myReviewer = Reviewer(username="XXXXXXXXXXXX", url="From_DataSet")

                            # datas Review object
                            aReview['url'] = "From_DataSet"
                            aReview['username'] = "From_DataSet"
                            aReview['user_url'] = "From_DataSet"
                            aReview['source'] = "imdb"
                            aReview['date'] = date(2050,1,1)
                            aReview['date'] = date(2050,1,1)

                        else:

                            # escape, don't need to insert any datas on db   
                            logger.warning('Review url already exist, and its not from dataset')
                            continue


                except Exception as e:
                    logger.error(f'got problem with url testing : {aReview["url"]}, and prepares datas', exc_info=True)

                # prepare review object to inject in db
                myReview = Review(
                                    url=aReview['url'],
                                    text=aReview['text'],
                                    score=aReview['score'],
                                    source=aReview['source'],
                                    date=aReview['date'],
                                    reviewers=myReviewer,
                                    movies=myMovie
                                )                

                # send reviewers and review object on db
                try:
                    session.add(myReview)
                    session.commit()
                except Exception as e:
                    logger.error(f'got problem sending reviewers and review object : {aReview["url"]}, and prepares datas', exc_info=True)

            else:
                # movie doesn't exist on db so, no movies no reviews
                logger.error(f'Source movie not found : {movie_key}', exc_info=True)
            
            # one more review has been treated
            cmpt += 1
            # clean stdout
            sys.stdout.write('              '*10 + '\r')
            sys.stdout.flush()



if __name__ == "__main__":
     
    # Create the tables in the database
    Base.metadata.create_all(engine)

    # Load the data from the json test file
    file_test = data_dir / "test_movies.json"
    load_movies(file_test)
    # logging.info("Load movies from test_movies.json")
    # # load_reviews
    # load_reviews("datas/test_reviews_restructured.json")
    # logging.info("Load reviews from test_reviews_restructured.json")