import logging
from model.sqlalchemyconfig import *    # noqa: F403
from load_from_JsonFiles import load_movies, load_reviews
#from restruct_reviewsJsonFile import restruct_redaJsonFile

from testfile import openfile


# configure logging
logging.basicConfig(level=logging.DEBUG, filename="logs/log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")



if __name__ == '__main__':
    
    # test pour log
    jsonObj = openfile("datas/test_movies")
    print(jsonObj)

     # # Create the tables in the database
     # Base.metadata.create_all(engine)  # noqa: F405

     # # # Reviews data restructuring
     # # #filename = restruct_redaJsonFile('datas/test_reviews.json')
     

     # # dataset test

     # # Load the data from the json file
     # load_movies('datas/test-urls_neg_dataset.json')
     # logging.info("Load movies from test-urls_neg_dataset.json")
     # # load_reviews
     # load_reviews("datas/test-urls_neg_Reviews_dataset.json")
     # logging.info("Load reviews from test-urls_neg_Reviews_dataset.json")

     # # Load the data from the json file
     # load_movies('datas/test-urls_pos_dataset.json')
     # logging.info("Load movies from test-urls_pos_dataset.json")
     # # load_reviews
     # load_reviews("datas/test-urls_pos_Reviews_dataset.json")
     # logging.info("Load reviews from test-urls_pos_Reviews_dataset.json")


     # # dataset train

     # # Load the data from the json file
     # load_movies('datas/train-urls_neg_dataset.json')
     # logging.info("Load movies from train-urls_neg_dataset.json")
     # # load_reviews
     # load_reviews("datas/train-urls_neg_Reviews_dataset.json")
     # logging.info("Load reviews from train-urls_neg_Reviews_dataset.json")

     # # Load the data from the json file
     # load_movies('datas/train-urls_pos_dataset.json')
     # logging.info("Load movies from train-urls_pos_dataset.json")
     # # load_reviews
     # load_reviews("datas/train-urls_pos_Reviews_dataset.json")
     # logging.info("Load reviews from train-urls_pos_Reviews_dataset.json")

     # # Load the data from the json file
     # load_movies('datas/train-urls_unsup_dataset.json')
     # logging.info("Load movies from train-urls_unsup_dataset.json")
     # # load_reviews
     # load_reviews("datas/train-urls_unsup_Reviews_dataset.json")
     # logging.info("Load movies from train-urls_unsup_dataset.json")



     # # from scrapingTest

     # # Load the data from the json file
     # load_movies('datas/test_movies.json')
     # logging.info("Load movies from test_movies.json")
     # # load_reviews
     # load_reviews("datas/test_reviews_restructured.json")
     # logging.info("Load reviews from test_reviews_restructured.json")


