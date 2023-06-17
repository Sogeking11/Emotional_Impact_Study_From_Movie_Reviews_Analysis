from model.movie import Movie
from model.review import Review
from model.country import Country
from model.reviewer import Reviewer
from model.genre import Genre
from model.keyword import Keyword
from model.prod_company import Prod_Company
from model.source import Source
from model.participant import Participant

from model.sqlalchemyconfig import *





if __name__ == "__main__":

    pass
    # Create the tables in the database
    Base.metadata.create_all(engine)

    # myBlob1 = b'Il etait encore une fois..'
    # myBlob2 = b"C'est alors qu'il ne voulurent pas, comme si..."


    # movie1 = Movie(
    #                     title='L\'homme qui tombe à pic',
    #                      certification='Cert A3',
    #                     revenue=456546,
    #                     budget=750000,
    #                     review_score= 8.5,
    #                     release_date="1985-08-15",
    #                     popularity= 9.2,
    #                     runtime=150,
    #                     synopsis=myBlob1
    #                 )
    
    # movie2 = Movie(
    #                     title='L\'Amour du risque',
    #                     certification='ISO 9002',
    #                     revenue=563876,
    #                     budget=75676,
    #                     review_score= 5.5,
    #                     release_date="1972-08-15",
    #                     popularity= 4.2,
    #                     runtime= 90,
    #                     synopsis=myBlob2
    #                 )
    

    # # countries
    # country1 = Country(name="Dzaïr")
    # country2 = Country(name="Holland")

    # movie1.countries.append(country1)
    # movie1.countries.append(country2)
    # movie2.countries.append(country2)

    # session.add(movie1)
    # session.add(movie2)
    # session.add(country1)
    # session.add(country2)
    # session.commit()

    #review1 = Review(text=b"Exceptionnelle, maisje sais pas !", movie=movie)
    #review2 = Review(text=b"Pas terrible, mais impressionnant...", movie=movie)
    #session.add(movie)
    #session.add(review1)
    #session.add(review2)
    #session.commit()