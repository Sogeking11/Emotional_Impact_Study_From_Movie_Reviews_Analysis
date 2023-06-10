myBlob1 = b'Il etait une fois..'
myBlob2 = b"C'est alors qu'il voulurent, comme d'un pacte..."


movie = Movie(
                    id_imdb='tt88888',
                    title='V for Vendetta',
                    production_company='Earth wind and Fire',
                    pegi='30',
                    sysnopsis=myBlob1,
                    keywords=myBlob2,
                    revenue=4,
                    budget=750000,
                    review_score=8,
                    release_date=2022
                )

review1 = Review(text=b"Exceptionnelle", movie=movie)
review2 = Review(text=b"Pas terrible...", movie=movie)


session.add(movie)
session.add(review1)
session.add(review2)
session.commit()