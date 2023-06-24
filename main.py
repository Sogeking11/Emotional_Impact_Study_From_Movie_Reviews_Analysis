from unidecode import unidecode
from datetime import date

from model import Movie, Review, Country, Reviewer, Genre, Keyword, Prod_Company, Source, Participant, Role
from model.sqlalchemyconfig import *
import csvfile_to_dict as source



if __name__ == "__main__":

    # Create the tables in the database
    Base.metadata.create_all(engine)

    for i in range(10):

        # Create datas
        # myBlob1 = "Mais je dois vous expliquer comment est née toute cette idée erronée de dénoncer un plaisir et de louer la douleur et je vais vous donner un compte rendu complet du système, "\
        # "et exposer les enseignements réels du grand explorateur de la vérité, le maître- constructeur du bonheur humain. "\
        # "Personne ne rejette, n'aime pas ou n'évite le plaisir lui-même, "\
        # "parce que c'est du plaisir, mais parce que ceux qui ne savent pas rechercher rationnellement le plaisir rencontrent des conséquences extrêmement douloureuses. "\
        # "Il n'y a plus non plus personne qui aime ou recherche ou désire obtenir la douleur par lui-même, "\
        # "parce que c'est de la douleur, mais il arrive parfois des circonstances dans lesquelles le travail et la douleur "\
        # "peuvent lui procurer un grand plaisir. Pour prendre un exemple trivial, "\
        # "lequel de nous entreprend jamais un exercice physique laborieux, sinon pour en tirer quelque profit ? "\
        # "Mais qui a le droit de critiquer un homme qui choisit de jouir d'un plaisir qui n'a pas de conséquences fâcheuses, "\
        # "ou celui qui évite une douleur qui ne produit aucun plaisir résultant ?"

        #myBlob1 = bytes(unidecode(myBlob1))
        myBlob = b"Hello"
        myDate = date(1985, 8, 15)
        myFloat = 9.2
        myString = "L\'homme qui tombe à pic"
        myInteger = 7
        mySmallint = 2

        # Create Object Entities
        a_movie = Movie(
                            title='L\'homme qui tombe à pic',
                            certification='Cert A3',
                            revenue=456546,
                            budget=750000,
                            review_score= 8.5,
                            release_date="1985-08-15",
                            popularity= 9.2,
                            runtime=150,
                            synopsis=myBlob
                        )
        
        a_source = Source(name=myString, movie_key=myString)
        a_prod_company = Prod_Company(name=myString)
        a_country = Country(name=myString)
        a_genre = Genre(name=myString)
        a_keyword = Keyword(name=myString)

        # participant case
        a_paticipant = Participant(name=myString, gender=2)
        a_role = Role(
                        movies=a_movie,
                        participants=a_paticipant,
                        name=myString
                      )

        # review case
        a_reviewer = Reviewer(url=myString, username=myString)
        a_review = Review(movies=a_movie,
                          reviewers=a_reviewer,
                          text=myBlob,
                          source=myString,
                          score=myInteger,
                          date=myDate,
                          url=myString
                          )
        
        a_movie.sources.append(a_source)
        a_movie.countries.append(a_country)
        a_movie.keywords.append(a_keyword)
        a_movie.genres.append(a_genre)
        a_movie.prod_companies.append(a_prod_company)

        # add in DB
        session.add_all([a_movie, 
                         a_source,  
                         a_prod_company, 
                         a_country, 
                         a_genre, 
                         a_keyword,
                         a_review,
                         a_role])
        
        session.commit()