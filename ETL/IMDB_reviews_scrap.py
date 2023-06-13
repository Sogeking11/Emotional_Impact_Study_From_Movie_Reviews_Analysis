import requests
from selenium import webdriver
import time
import pandas as pd
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime

# API TMDB
api_key = '5849fbb34bea488bb2d73d4d6638ff36'

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

def click_load_more(element):
    '''_summary_ : This function clicks on the "See more" button to extend the full comment
    '''
    try:
        see_more = element.find_element(By.CLASS_NAME, "ipl-expander")
        if see_more.is_displayed():
            see_more.click() 
    except:
        pass

# get the most popular movies id

movies_ids = get_the_most_popular_movies_id(api_key)
df = extract_movie_data_from_imdb_id([movies_ids[0]])
id = df['id_movie']

url = f'https://api.themoviedb.org/3/movie/{id}'
params = {'api_key': api_key}
response = requests.get(url, params=params)
data = response.json()
imdb_id = df['id_imdb']

# Selenium configuration
driver = webdriver.Chrome()  
driver.maximize_window()
wait = WebDriverWait(driver, 10)

data_comments = []
# get the reviews of the most popular movies
while True:
    for id in imdb_id:
        url = f'https://www.imdb.com/title/{id}/reviews?ref_=tt_ov_rt'
        driver.get(url)
        time.sleep(1)

        reviews = driver.find_elements(By.CLASS_NAME, "review-container")
        for review in reviews[:5]:
            click_load_more(review)
            # get the title of the movie
            try:
                title = df.loc[df['id_imdb'] == id, 'title'].iloc[0]
            except:
                title = 'title not found'
                
            # get the id of the movie
            try:
                id = df.loc[df['id_imdb'] == id, 'id_imdb'].iloc[0]
            except:
                id = 'id not found'
            # get the review score
            try:
                for score in review.find_elements(By.CLASS_NAME, "rating-other-user-rating"):
                    review_score = score.text.replace('/10','')
            except:
                review_score = 'Score not found'
            # get the review url and the user url
            try:
                lnks = review.find_elements(By.TAG_NAME,"a")
                review_url = lnks[0].get_attribute('href')
                user_url = lnks[1].get_attribute('href')
            except:
                review_url = 'URL not found'
            # get the review date and convert it to the right format
            try:
                review_date = review.find_element(By.CLASS_NAME, "review-date").text
                review_date = datetime.strptime(review_date, '%d %B %Y').strftime('%Y-%m-%d')
            except:
                review_date = 'date not found'
            # get the username
            try:
                username = review.find_element(By.CLASS_NAME, "display-name-link").text
            except:
                username = 'user not found'
            # get the comment of the user and remove the useless lines
            try:
                comment = review.find_element(By.CLASS_NAME, "content").text.replace('\n\n','\n')
                comment = comment.split('\n')
                comment = [line for line in comment if not 'Was this review helpful? Sign in to vote' in line] 
                comment = [line for line in comment if not 'Permalink' in line]
                comment = '\n'.join(comment)
            except:
                comment = 'comment not found'
            # store the data in a list of dictionaries
            data_comments.append({'id': id, 'title': title, 'user': username, 'comment': comment, 'score': review_score, 'user_url': user_url, 'review_url': review_url, 'date': review_date})
    break

csv_path = 'testV3.csv'

# write the data in a csv file
with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['id', 'title', 'user', 'comment', 'score', 'user_url', 'review_url', 'date']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data_comments)

print("Data saved in CSV file")

# close the driver
driver.quit()



