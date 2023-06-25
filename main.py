from datetime import date
import pandas as pd

from model import Movie, Review, Country, Reviewer, Genre, Keyword, Prod_Company, Source, Participant, Role
from model.sqlalchemyconfig import *
import csvfile_to_dict as source



if __name__ == "__main__":

    # Create the tables in the database
    Base.metadata.create_all(engine)

    # get dictionnary source
    source_dict = source.csvToDictFile('testapi100.csv')

    # here we test for one movie to ckeck
    row = source_dict[0]

    # insert source
    #for row in source_dict.values():
    print(row['movie']['title'] + "\n")
    # movie part
    title = str(row['movie'].get('title'))
    certification = str(row['movie'].get('certification'))
    revenue = int(row['movie'].get('revenue'))
    budget = int(row['movie'].get('budget'))
    review_score = float(row['movie'].get('review_score'))
    release_date = row['movie'].get('release_date')
    popularity = float(row['movie'].get('popularity'))
    runtime = int(row['movie'].get('runtime'))
    synopsis = str(row['movie'].get('synopsis'))
    # create movie object from model
    movie = Movie(title=title,
                certification=certification,
                revenue=revenue,
                budget=budget,
                review_score=review_score,
                release_date=release_date,
                popularity=popularity,
                runtime=runtime,
                synopsis=synopsis
    )   
    # source part
    imdb_src = str(row['sources'].get('imdb'))
    tmdb_src = str(row['sources'].get('tmdb'))
    # create source object from model
    source1 = Source(name = 'imdb', movie_key=imdb_src)
    source2 = Source(name = 'tmdb', movie_key=tmdb_src)
    movie.sources.append(source1)
    movie.sources.append(source2)
    session.add(source1, source2)   
    # country part
    country_list = row['countries']
    for country in country_list:
        # create country object from model
        country_obj = Country(name=country)
        movie.countries.append(country_obj)
        session.add(country_obj)    
    # prod_company part
    prod_company_list = row['production_companies']
    for prod_company in prod_company_list:
        # create prod_company object from model
        prod_company_obj = Prod_Company(name=prod_company)
        movie.prod_companies.append(prod_company_obj)
        session.add(prod_company_obj)   
    # genre part
    genre_list = row['genres']
    for genre in genre_list:
        # create genre object from model
        genre_obj = Genre(name=genre)
        movie.genres.append(genre_obj)
        session.add(genre_obj)  
    # keyword part
    keyword_list = row['keywords']
    for keyword in keyword_list:
        # create keyword object from model
        keyword_obj = Keyword(name=keyword)
        movie.keywords.append(keyword_obj)
        session.add(keyword_obj)    
    # role part
    for member in row['role'].values():
        participant = Participant(name=str(member['name']), gender=int(member['gender'][0]))
        role = Role(
                    movies=movie,
                    participants=participant,
                    name=str(member['role'])
                )
        session.add(role)   
    # insert datas  
    session.add(movie)
    session.commit()