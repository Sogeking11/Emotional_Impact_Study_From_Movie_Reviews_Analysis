import requests
import pandas as pd
import api_keys

# https://www.educative.io/answers/what-is-astliteralevalnodeorstring-in-python

# save to jason format

# Votre clé API TMDB
api_key_tmdb = api_keys.TMDB
api_key_omdb = api_keys.OMDB

def get_the_most_popular_movies_id(api_key):
    """_summary_ : This function returns the list of the most popular movies id from the TMDB API

    Returns:
        list_of_popular_movies_id: List of the most popular movies id from the TMDB API
    """

    # Number of pages of results, there is 20 movies per page
    total_pages = 1
    list_of_popular_movies_id = []
    for page in range(1,total_pages+1):

        url = 'https://api.themoviedb.org/3/movie/popular'
        params = {'api_key': api_key, 'page': page}
        response = requests.get(url, params=params)
        data = response.json()
        total_pages = data['total_pages']
        #print(data.keys())
        for popular_film in data['results']:
            list_of_popular_movies_id.append(popular_film['id'])
        
    return list_of_popular_movies_id


def get_movie_actors(api_key,id):
    """_summary_ : This function returns the list of the most popular movies id from the TMDB API

    Returns:
        list_of_popular_movies_id: List of the most popular movies id from the TMDB API
    """
    url = f'https://api.themoviedb.org/3/movie/{id}/credits?language=en-US'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    print('Request participants done')
    data = response.json()
    movie_people_list = []
    for cast in data['cast']:
        data_to_save =  {'name': cast['name'],
                        'gender': cast['gender'], 
                        'popularity': cast['popularity'],
                        'role': cast['known_for_department']}
        movie_people_list.append(data_to_save)
    for crewmate in data['crew']:
        if crewmate['job'] in ['Executive Producer', 'Director', 'Screenplay']:
            data_to_save = {'name': crewmate['name'],
                        'gender': crewmate['gender'], 
                        'popularity': crewmate['popularity'],
                        'role': crewmate['job']}
    # delete duplicates in the list
    movie_people_list = [dict(t) for t in {tuple(d.items()) for d in movie_people_list}] # https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python
    movie_people_list.append(data_to_save)
        
    return movie_people_list

# def get_RT_id_from_imdb_id(omdb_apikey,imdb_id):
#     """_summary_ : This function returns the Rotten Tomatoes unique ID from the websites movie url from the TMDB API whith the IMDB unique movie ID
#     Returns:
#         RT_id: Rotten Tomatoes unique ID 
#     """
#     url = f"http://www.omdbapi.com/?apikey={omdb_apikey}&tomatoes=true&i={imdb_id}"
#     headers = {"accept": "application/json"}
#     response = requests.get(url, headers=headers)
#     print('Request RT_id done')
#     try :
#         data = response.json()
#         if data['tomatoURL'] == "N/A" :
#             RT_id = "N/A"
#         else : RT_id = data['tomatoURL'].split('/')[-1]
#     except: 
#         RT_id = "N/A"
#     return RT_id

def get_the_movie_key_words(api_key,id):
    """_summary_ : This function returns the list of keywords of the movie
    Returns:
        list_of_keywords: List of the keywords by movie id
    """

    url = f"https://api.themoviedb.org/3/movie/{id}/keywords"
    params = {'api_key': api_key}
    headers = {"accept": "application/json"}
    response = requests.get(url, params=params, headers = headers)
    print('Request key_words done')
    try:
        data = response.json()
        data['keywords'] = [keyword['name'] for keyword in data['keywords']]
    except:
        data['keywords'] = 'N/A'

    return data['keywords']

def get_certification(api_key,id):
    """_summary_ : This function returns the PEGI of the movie
    Returns:
        certification: age certification of the movie
    """
    url = f'https://api.themoviedb.org/3/movie/{id}/release_dates'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    print('Request certification done')
    data = response.json()
    certification = 'N/A'
    try:
        for country in data['results']:
            if country['iso_3166_1'] == 'US':
                for certification in country['release_dates']:
                    if certification['certification'] != '':
                        certification = certification['certification']
                    elif certification['certification'] == '':
                        certification = 'N/A'
                        break
    except:
        certification = 'N/A'

    return certification

def extract_movie_data_from_imdb_id(api_key_tmdb, api_key_omdb, id_list):
    """_summary_ : This function extracts the movie components from the differents apis (TMDB, OMDB) to feed our database
    Returns:
        df: Pandas Dataframe of the movie table and its close relations 
    """
    movie_data_list = []
    index=0
    for id in id_list:
        index+=1
        print(index, "id", id)
        url = f'https://api.themoviedb.org/3/movie/{id}'
        params = {'api_key': api_key_tmdb}
        response = requests.get(url, params=params)
        print('Request movie done')
        try:
            data = response.json()
            print('title', data['title'])
            data['genres'] = [genre['name'] for genre in data['genres']]
            # get the name of the production companies and countries
            data['production_companies'] = [company['name'] for company in data['production_companies']]
            data['production_countries'] = [country['name'] for country in data['production_countries']]
            
            # Stock datas in a dict
            data_to_save = {
                'id_tmdb': data['id'],
                'id_imdb': data['imdb_id'],
                'title': data['title'],
                'revenue': data['revenue'],
                'budget': data['budget'],
                'review_score': data['vote_average'],
                'release_date': data['release_date'],
                'synopsis': data['overview'],
                'popularity': data['popularity'],
                'production_companies': data['production_companies'],
                'countries': data['production_countries'],
                'genres': data['genres'],
                'runtime': data['runtime'],
                
            }
            
            data_to_save['role'] = get_movie_actors(api_key_tmdb,id)
            data_to_save['keywords'] = get_the_movie_key_words(api_key_tmdb,id)
            #data_to_save['id_rt'] = get_RT_id_from_imdb_id(api_key_omdb, data['imdb_id'])
            data_to_save['certification'] = get_certification(api_key_tmdb, data['imdb_id'])
            movie_data_list.append(data_to_save)
        except:
            print('N/A')
    df = pd.DataFrame.from_dict(movie_data_list)
    return df

movies_ids = get_the_most_popular_movies_id(api_key_tmdb)
df = extract_movie_data_from_imdb_id(api_key_tmdb, api_key_omdb, movies_ids)
df['role'] = df['id_tmdb'].apply(lambda x: get_movie_actors(api_key_tmdb,x))
df['keywords'] = df['id_tmdb'].apply(lambda x: get_the_movie_key_words(api_key_tmdb,x))
#df['id_rt'] = df['id_imdb'].apply(lambda x: get_RT_id_from_imdb_id(api_key_omdb,x))
df['certification'] = df['id_imdb'].apply(lambda x: get_certification(api_key_tmdb,x))

with open('test_movie.json', 'w', encoding='utf-8') as f:
    df.to_json(f, orient='records', force_ascii=False) # orient='records' = to not have keys in the json. force_ascii=False to not have \u00e9 in the json
    
