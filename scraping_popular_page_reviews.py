import requests
from selenium import webdriver
import time
import pandas as pd
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# API TMDB
api_key = '5849fbb34bea488bb2d73d4d6638ff36'

def get_the_most_popular_movies_id(api_key):
    # Cette fonction retourne la liste des identifiants des films les plus populaires de l'API TMDB
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

def extract_movie_data_from_imdb_id(id_list):
    movie_data_list = []
    for id in id_list:
        url = f'https://api.themoviedb.org/3/movie/{id}'
        params = {'api_key': api_key}
        response = requests.get(url, params=params)
        data = response.json()

        # for key in data.keys():
        #     print('|||',key,'|||')
        #     print(data[key])
            
            
        # Stocker les données dans un dictionnaire
        data_to_save = {
            'id_movie': data['id'],
            'id_imdb': data['imdb_id'],
            'title': data['original_title'],
            'synopsis': data['overview'],
            'popularity': data['popularity'],
            'production_companies': data['production_companies'],
            'spoken_languages': data['spoken_languages'],
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

# Fonction pour cliquer sur le bouton "Voir plus" pour étendre le commentaire complet
def cliquer_voir_plus(element):
    try:
        voir_plus = element.find_element(By.CLASS_NAME, "ipl-expander")
        if voir_plus.is_displayed():
            voir_plus.click()  # Attendre un court instant pour que le texte étendu se charge
    except:
        pass

# Obtenir les identifiants des films populaires

movies_ids = get_the_most_popular_movies_id(api_key)
df = extract_movie_data_from_imdb_id(movies_ids)
id = df['id_movie']

url = f'https://api.themoviedb.org/3/movie/{id}'
params = {'api_key': api_key}
response = requests.get(url, params=params)
data = response.json()
imdb_id = df['id_imdb']

# Configurer Selenium pour le scraping
driver = webdriver.Chrome()  # Remplacez '/path/to/chromedriver' par le chemin vers votre chromedriver
driver.maximize_window()
wait = WebDriverWait(driver, 10)

donnees_commentaires = []
# Récupérer les reviews des films populaires sur IMDb
while True:
    for id in imdb_id:
        url = f'https://www.imdb.com/title/{id}/reviews?ref_=tt_ov_rt'
        driver.get(url)
        time.sleep(1)
        # Cliquez sur le bouton "Load more" jusqu'à ce qu'il disparaisse
        while True:
            try:
                load_more_button = driver.find_element(By.CLASS_NAME, "ipl-load-more__button")
                load_more_button.click()
                time.sleep(1)
            except:
                break

        # Récupérer les commentaires
        reviews = driver.find_elements(By.CLASS_NAME, "review-container")
        for review in reviews:
            # Cliquer sur le bouton "Voir plus" pour étendre le commentaire complet
            cliquer_voir_plus(review)
            # récupérer le titre du film
            try:
                title = df.loc[df['id_imdb'] == id, 'title'].iloc[0]
            except:
                title = 'Titre non trouvé'
                
            # Récupérer l'identifiant du film
            try:
                id = df.loc[df['id_imdb'] == id, 'id_imdb'].iloc[0]
            except:
                id = 'Identifiant non trouvé'
            # Récupérer le score du film
            try:
                review_score = review.find_element(By.CLASS_NAME, "rating-other-user-rating").text.replace('\n','')
            except:
                review_score = 'Score non trouvé'
            # Récupéré l'url de l'utilisateur
            try:
                user_url = review.find_element(By.CLASS_NAME, "display-name-link").get_attribute('href')
            except:
                user_url = 'URL non trouvé'
            # Récupérer le nom de l'utilisateur
            try:
                username = review.find_element(By.CLASS_NAME, "display-name-link").text
            except:
                username = 'Utilisateur non trouvé'
            # Récupérer le commentaire
            try:
                comment = review.find_element(By.CLASS_NAME, "content").text
            except:
                comment = 'Commentaire non trouvé'
            # Stocker les données dans un dictionnaire
            donnees_commentaires.append({'Titre': title, 'Utilisateur': username, 'Commentaire': comment, 'Score': review_score, 'Identifiant': id, 'URL': user_url})
    break

# Chemin du fichier CSV de destination
chemin_fichier_csv = 'testV3.csv'

# Écriture des données dans le fichier CSV
with open(chemin_fichier_csv, mode='w', newline='', encoding='utf-8') as fichier_csv:
    fieldnames = ['Titre', 'Utilisateur', 'Commentaire', 'Score', 'Identifiant', 'URL']
    writer = csv.DictWriter(fichier_csv, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(donnees_commentaires)

print("Les données des commentaires de IMDB ont été stockées dans le fichier CSV.")

# Fermer le navigateur
driver.quit()
