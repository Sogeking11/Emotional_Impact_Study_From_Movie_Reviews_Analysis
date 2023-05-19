from dataset_extract_stock import scrap_data as scrap

# test scraping module
imdb_id = "tt0111161"
data_to_scrap = scrap.data_prop["title"]
data = scrap.getData(imdb_id, data_to_scrap)
print(data)

imdb_id = "tt0111161"
data_to_scrap = scrap.data_prop["imdb_rating"]
data = scrap.getData(imdb_id, data_to_scrap)
print(data)

imdb_id = "tt0111161"
data_to_scrap = scrap.data_prop["release_year"]
data = scrap.getData(imdb_id, data_to_scrap)
print(data)