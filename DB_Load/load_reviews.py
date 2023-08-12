"""
This module is used to load Reviews from json files to the database.
"""

# import modules and packages
import sys
import logging
from pathlib import Path
from datetime import date

from .model.sqlalchemyconfig import get_session
from .model import Movie, Review, Reviewer, Source
from .datas_object import fileToJson


# data dir path
data_dir = Path("datas")

# logger config
logger = logging.getLogger(__name__)

# creates Handlers
handler_1 = logging.FileHandler(filename="logs/" + __name__ + ".log", mode="w")
#handler_2 = logging.StreamHandler() # stdout handle the log
handler_3 = logging.FileHandler(filename="logs/errors/" + __name__ + ".log", mode="w")


# setting handlers
handler_1.setLevel(logging.DEBUG)
#handler_2.setLevel(logging.ERROR)
handler_3.setLevel(logging.ERROR)

# logger level
logger.setLevel(logging.DEBUG)

# formatters + adding them on handlers
formatter_1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#formatter_2 = logging.Formatter('%(levelname)s - %(message)s')
formatter_3 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler_1.setFormatter(formatter_1)
#handler_2.setFormatter(formatter_2)
handler_3.setFormatter(formatter_3)
logger.addHandler(handler_1)
#logger.addHandler(handler_2)
logger.addHandler(handler_3)



def push_review(review_dict, myMovie, session):
    """This function push a review and its metadata in db.

    Args:
        review_dict (dict): review object
        myMovie (Movie): movie object
    """

    # create review object
    # here we must define if it's from Dataset or from scrap
    if review_dict['url'] == "From_DataSet":

        # check if reviewer is already in db
        try:
            myReviewer = session.query(Reviewer).filter_by(username="AI_DataSet_Reviewer").first()
        except:
            logger.error(f"An Error occured on checking if reviewer {review_dict['username']} is already in db")
        
        if myReviewer is None:
            # Dataset reviewer must be created   
            myReviewer = Reviewer(username="AI_DataSet_Reviewer", url="From_DataSet")

        # datas Review object
        review_dict['source'] = "imdb"
        review_dict['date'] = date(2050,3,21) # printemps 2050


    else:
        # the review object is from scrapping
        # check if reviewer is already in db
        try:
            myReviewer = session.query(Reviewer).filter_by(username=review_dict['username']).first()
        except:
            logger.error(f"An Error occured on checking if reviewer {review_dict['username']} is already in db")

        if myReviewer is None:
            # Here to prepare reviewer
            myReviewer = Reviewer(username=review_dict['username'], url=review_dict['user_url'])

    # prepare review object to inject in db
    myReview = Review(
                        url=review_dict['url'],
                        text=review_dict['text'],
                        score=review_dict['score'],
                        source=review_dict['source'],
                        date=review_dict['date'],
                        reviewers=myReviewer,
                        movies=myMovie
                    )                

    # send reviewers and review object on db
    try:
        session.add(myReview)
        session.commit()
        logger.info(f'Review {myReview.url} sent to db \n')
    except:
        logger.error(f'got problem sending reviewers and review object : {review_dict["url"]}', exc_info=True)
        session.rollback()


def load_reviews(jsonReviewsFile):
    """
    Principal function to send reviews

    Args:
        jsonReviewsFile (str): path to the json file containing reviews
    """

    # get session to operate on db
    try:
        session = get_session()
    except:
        logger.error("Can't get session to load reviews")

    # test logger
    logger.info('\n================== Start loading reviews =====================')
    logger.info('Send reviews to DB')

    # get json object from file
    json_object = fileToJson(jsonReviewsFile)


    # needed for stdout info saying how many reviews have been treated
    cmpt = 1

    # go through each imdb movie ids in the dictionnary
    for imdb_id, review_list in json_object.items():

        # initialise myMovie
        myMovie = None

        # get the movie object
        #Start by getting source object to get movie object
        try:
            mySource = session.query(Source).filter_by(movie_key=imdb_id).first()
        except:
            logger.error(f"occured on getting source object for id_imdb {imdb_id}")
            continue
        # get movie object to help create Review object in case of review does not exist
        try:
            myMovie = session.query(Movie).filter_by(id=mySource.movie_id).first()
        except:
            logger.error(f'could not get the movie object with id {imdb_id}')

        # necessary condition to push the review in db
        # is that the movie attach to review must exist in db 
        if myMovie is None:
            logger.warning(f"No movie with id_imdb {imdb_id}")
            continue

        # go through each review
        for review_dict in review_list:
            try:
                review_in_db = session.query(Review).filter_by(url=review_dict['url']).first()
            except:
                logger.error(f"An Error occured on getting review object from db for url {review_dict['url']}")
                continue

            # push info in stdout
            sys.stdout.write('Review number : ' + str(cmpt) + ' from movie source : ' + imdb_id + ' in operation.\r')
            sys.stdout.flush()

            # test if review is already in db or not
            if review_in_db is None:
                # push review on db
                try:
                    push_review(review_dict, myMovie, session)
                except:
                    logger.error(f"An Error occured on pushing review object for url {review_dict['url']}")

            else:
                # care of url in db is From_Dataset
                if review_in_db.url == "From_DataSet":
                    push_review(review_dict, myMovie, session)
                else:
                    # if it's not from dataset do nothing except log message
                    logger.info(f'Review {review_dict["url"]} already in db')

            cmpt += 1
            # clean stdout
            sys.stdout.write('              '*10 + '\r')
            sys.stdout.flush()
            logger.info(f'Review number {cmpt-1} from url {review_dict["url"]} has been treated')