import addTitle as a

imdb_id = "tt0111161"
data_to_scrap = a.data_prop["title"]
data = a.getData(imdb_id, data_to_scrap)
print(data)

imdb_id = "tt0111161"
data_to_scrap = a.data_prop["imdb_rating"]
data = a.getData(imdb_id, data_to_scrap)
print(data)

imdb_id = "tt0111161"
data_to_scrap = a.data_prop["release_year"]
data = a.getData(imdb_id, data_to_scrap)
print(data)