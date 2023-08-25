import logging
from pathlib import Path

import os
from flask import Flask, render_template

from loadEnv import loadEnv
from DB_Load import load_movies, load_reviews

# logging configuration
logger = logging.getLogger(__name__)
# creates Handlers
handler_1 = logging.FileHandler(filename="logs/" + __name__ + ".log", mode="w")
# setting handler
handler_1.setLevel(logging.DEBUG)
# logger level
logger.setLevel(logging.INFO)
# formatters + adding them on handlers
formatter_1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler_1.setFormatter(formatter_1)
logger.addHandler(handler_1)

# for GCP to lesson as a web server
app = Flask(__name__)

# route /
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "Hello my Friend, it's running!"
    return render_template('index.html',message=message,)


def load():
    # data dir path
    data_dir = Path(loadEnv("DATAPATH"))

    filesToLoad = {
        'test_movies.json': 'test_reviews_restructured.json',
     #    'test-urls_neg_dataset.json': 'test-urls_neg_Reviews_dataset.json',
     #    'test-urls_pos_dataset.json': 'test-urls_pos_Reviews_dataset.json',
     #    'train-urls_neg_dataset.json': 'train-urls_neg_Reviews_dataset.json',
     #    'train-urls_pos_dataset.json': 'train-urls_pos_Reviews_dataset.json',
     #    'train-urls_unsup_dataset.json': 'train-urls_unsup_Reviews_dataset.json',
     #    'data_full.json':'full_reviews_restructured.json'
    }

    for jsonMoviesFile, jsonReviewsFile in filesToLoad.items():

        # files paths
        movieFile = data_dir / jsonMoviesFile
        reviewFile = data_dir / jsonReviewsFile

        # Load the movies
        logger.info(f"Loading {movieFile}")
        load_movies(movieFile)

        # load_reviews
        logger.info(f"Loading {reviewFile}")
        load_reviews(reviewFile)



if __name__ == '__main__':

    # load()

    # check
    print("Hello World !")
    # lesson on port
    # GCP image mandatory
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')