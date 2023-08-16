import requests
import pandas as pd
from datetime import datetime
import json
import api_keys
from bs4 import BeautifulSoup


# API TMDB
api_key = api_keys.TMDB


def get_the_most_popular_movies_id(api_key):
    """_summary_ : This function returns the list of the most popular movies id from the TMDB API

    Returns:
        list_of_popular_movies_id: List of the most popular movies id from the TMDB API
    """    
    total_pages = 1
    list_of_popular_movies_id = []
    for page in range(1,total_pages+1):

        url = 'https://api.themoviedb.org/3/movie/popular'
        params = {'api_key': api_key, 'page': page}
        response = requests.get(url, params=params)
        data = response.json()
        total_pages = data['total_pages']
        for popular_film in data['results']:
            list_of_popular_movies_id.append(popular_film['id'])
        
    return list_of_popular_movies_id

def extract_movie_data_from_imdb_id(id_list):
    """_summary_ : This function extracts the movie components from the differents apis (TMDB, OMDB) to feed our database
    Returns:
        df: Pandas Dataframe of the movie table and its close relations 
    """
    movie_data_list = []
    for id in id_list:
        url = f'https://api.themoviedb.org/3/movie/{id}'
        params = {'api_key': api_key}
        response = requests.get(url, params=params)
        data = response.json()
        data_to_save = {
            'id_movie': data['id'],
            'id_imdb': data['imdb_id'],
            'title': data['original_title'],
            'synopsis': data['overview'],
            'popularity': data['popularity'],
            'production_companies': data['production_companies'],
            'countries': data['production_countries'],
            'revenue': data['revenue'],
            'budget': data['budget'],
            'genres': data['genres'],
            'release_date': data['release_date'],
            'runtime': data['runtime'],
            'review_score': data['vote_average'],
        }
        movie_data_list.append(data_to_save)
    df = pd.DataFrame.from_dict(movie_data_list)
    return df

# def click_see_all(element):
#     '''_summary_ : This function clicks on the "See more" button to extend the full comment
#     '''
#     try:
#         see_all = element.find_element(By.CLASS_NAME, "ipl-expander")
#         if see_all.is_displayed():
#             see_all.click() 
#     except:
#         pass

# def click_load_more():
#     '''_summary_ : This function clicks on the "Load more" button to extend the full comment
#     '''
#     while True:
#         try:
#             load_more = driver.find_element(By.CLASS_NAME, "ipl-load-more__button")
#             if load_more.is_displayed():
#                 load_more.click() 
#                 time.sleep(1)
#         except:
#             break


# get the reviews of the most popular movies
def get_reviews(imdb_id):
    """_summary_ : This function extracts the reviews from the IMDB website.
    Returns:
        data_comments: List of the reviews
    """
    # get only the first 30 reviews per movie
    data_comments = []
    while True:
        for id in imdb_id:
            url = f'https://www.imdb.com/title/{id}/reviews?ref_=tt_ov_rt'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            reviews = soup.find_all('div', class_='review-container')
            
            # # click "Load more" button until we get to 30 reviews
            # if len(reviews) < 30:
            #     try:
            #         load_more_button = driver.find_element(By.CLASS_NAME, "ipl-load-more__button")
            #         load_more_button.click()
            #         time.sleep(1)
            #     except:
            #         break
            
            for review in reviews:
                #click_see_all(review)
                # get the title of the movie
                try:
                    title = df.loc[df['id_imdb'] == id, 'title'].iloc[0]
                except:
                    title = 'N/A'
                    
                # get the id of the movie
                try:
                    id = df.loc[df['id_imdb'] == id, 'id_imdb'].iloc[0]
                except:
                    id = 'N/A'
                # get the review score
                try:
                    review_score = review.select_one('.rating-other-user-rating span').text

                except:
                    review_score = '0'
                # get the review url and the user url
                try:
                    lnks = review.find_all('a', href=True)
                    review_url = lnks[0]['href']
                    user_url = lnks[1]['href']
                    # review_url = review.find('a', class_='title').get('href')
                    # user_url = review.find('a', class_='display-name-link').get('href')
                    # lnks = review.find_elements(By.TAG_NAME,"a")
                    # review_url = lnks[0].get_attribute('href')
                    # user_url = lnks[1].get_attribute('href')
                except:
                    review_url = 'N/A'
                    user_url = 'N/A'
                # get the review date and convert it to the right format
                try:
                    review_date = review.find('span', class_='review-date').text
                    #review_date = review.find_element(By.CLASS_NAME, "review-date").text
                    review_date = datetime.strptime(review_date, '%d %B %Y').strftime('%Y-%m-%d')
                except:
                    review_date = 'N/A'
                # get the username
                try:
                    username = review.select_one('.display-name-link').text
                except:
                    username = 'N/A'
                # get the comment of the user and remove the useless lines. Get only 500 characters max
                try:
                    comment = review.select_one('.text.show-more__control').text   #.text.replace('\n\n','\n')
                    # comment = comment.split('\n') 
                    # comment = [line for line in comment if not 'Was this review helpful? Sign in to vote' in line] 
                    # comment = [line for line in comment if not 'Permalink' in line]
                    # comment = '\n'.join(comment)
                    #comment = comment[:500]
                except:
                    comment = 'N/A'
                # store the data in a list of dictionaries
                data_comments.append({'id': id, 'title': title, 'user': username, 'comment': comment, 'score': review_score, 'user_url': user_url, 'review_url': review_url, 'date': review_date})
        break
    return data_comments


if __name__ == "__main__":
    # get the most popular movies id
    api_df = pd.read_json('/home/jovyan/data/data_full.json')
    # movies_ids = get_the_most_popular_movies_id(api_key)
    df = api_df
    id = df['id_tmdb']

    url = f'https://api.themoviedb.org/3/movie/{id}'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    data = response.json()
    imdb_id = df['id_imdb']

    

    data_comments = get_reviews(imdb_id)

    # write the data in a json file
    with open('test_reviews.json', 'w', encoding='utf-8') as f:
        json.dump(data_comments, f, ensure_ascii=False, indent=4)

    print("Data saved in Json file")


    '''
    Set un minimum de mots (10?)
    25 commentaires par films
    Ne prendre que les films contenant contenant 25 commentaires
    '''