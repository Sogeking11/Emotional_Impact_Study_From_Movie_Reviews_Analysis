from pathlib import Path

from DB_Load import load_movies, load_reviews


if __name__ == '__main__':

    # data dir path
    data_dir = Path("datas")

    filesToLoad = {
        'test_movies.json': 'test_reviews_restructured.json',
        'test-urls_neg_dataset.json': 'test-urls_neg_Reviews_dataset.json',
        'test-urls_pos_dataset.json': 'test-urls_pos_Reviews_dataset.json',
        'train-urls_neg_dataset.json': 'train-urls_neg_Reviews_dataset.json',
        'train-urls_pos_dataset.json': 'train-urls_pos_Reviews_dataset.json',
        'train-urls_unsup_dataset.json': 'train-urls_unsup_Reviews_dataset.json',
        'data_full.json':'full_reviews_restructured.json'
    }

    for jsonMoviesFile, jsonReviewsFile in filesToLoad.items():

        # files paths
        movieFile = data_dir / jsonMoviesFile
        reviewFile = data_dir / jsonReviewsFile

        # Load the movies
        load_movies(movieFile)

        # load_reviews
        load_reviews(reviewFile)