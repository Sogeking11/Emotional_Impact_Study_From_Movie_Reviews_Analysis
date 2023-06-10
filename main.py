from model.movie import Movie
from model.review import Review
from model.sqlalchemyconfig import *




if __name__ == "__main__":

    # Create the tables in the database
    #Base.metadata.create_all(engine)

    myBlob1 = b'Il etait encore une fois..'
    myBlob2 = b"C'est alors qu'il ne voulurent pas, comme si..."


    movie = Movie(
                        id_imdb='tt7777777',
                        title='L\'homme qui tombe à pic',
                        production_company='could you be loved',
                        pegi='60',
                        sysnopsis=myBlob1,
                        keywords=myBlob2,
                        revenue=4,
                        budget=750000,
                        review_score=8,
                        release_date=2022
                    )

    review1 = Review(text=b"Exceptionnelle, maisje sais pas !", movie=movie)
    review2 = Review(text=b"Pas terrible, mais impressionnant...", movie=movie)


    session.add(movie)
    session.add(review1)
    session.add(review2)
    session.commit()