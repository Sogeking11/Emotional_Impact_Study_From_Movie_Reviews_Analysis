import sys
import json

from model import Movie, Country, Genre, Keyword, Prod_Company, Role
from model.sqlalchemyconfig import *
from datas_object import *





if __name__ == '__main__':

     # Create the tables in the database
    Base.metadata.create_all(engine)

    #Opening JSON file
    with open('datas/test.json', 'r', encoding='utf-8') as openfile:

        # Reading from json file
        try:
            json_object = json.load(openfile,)
        except ValueError as e:
            logging.error('invalid json: %s' % e)

    # try with one film to start
    #OneFilm = json_object[0]
    i = 0
    for OneFilm in json_object:
        # needed for stdout info saying how many movies has been treated
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