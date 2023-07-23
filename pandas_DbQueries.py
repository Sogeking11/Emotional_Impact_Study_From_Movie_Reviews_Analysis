######################
# Pandas QueriesonDB #
######################
import pandas as pd

from model.sqlalchemyconfig import *  # noqa: F403
from model import Review, Source
import json







if __name__ == '__main__':

    # Create the tables in the database
    Base.metadata.create_all(engine)  # noqa: F405
    
    # try : SELECT * FROM CINEMOTION.movie;
    df = pd.read_sql(
                            session.query(Review).\
                            filter(Review.url == "From_DataSet").\
                                statement,session.bind)
    
    movie_list = df['movie_id'].unique()
    
    df_source = pd.read_sql(session.query(Source).\
                            filter(Source.name == "imdb").\
                                statement, session.bind)

    
    df_dataset_source_movies = df_source[df_source['movie_id'].isin(movie_list)]
    list_movie_key = df_dataset_source_movies["movie_key"].to_list()
    json_list = json.dumps(list_movie_key)

    file_path = "imdb_id_from_Dataset_To_Scrap.txt"

    with open(file_path, 'w') as f:
        f.write(json_list)
    