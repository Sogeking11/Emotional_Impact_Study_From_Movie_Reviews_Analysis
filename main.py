import logging
from model.sqlalchemyconfig import *
from load_from_JsonFiles import load_movies, load_reviews
from restruct_reviewsJsonFile import restruct_redaJsonFile


# configure logging
logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")



if __name__ == '__main__':

     # Create the tables in the database
    Base.metadata.create_all(engine)

    # Load the data from the json file
    # load_movies('datas/test.json')

    # Reviews data restructuring
    #filename = restruct_redaJsonFile('datas/test_reviews.json')

    # Load the reviews from the json file
    filename = 'datas/test_reviews_restructured.json'
    load_reviews(filename)