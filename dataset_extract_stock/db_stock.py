import sys
import pandas as p
import pymysql as maria
from pymysql.connections import Connection


def connect_to_db(host: str, port:int, user: str, password: str, database: str) -> maria.connections.Connection:
    """_summary_ : permet de se connecter à une base de données
    Args:
        host (str): machine sur laquelle se trouve la base de données
        port (str): port ouvert de la BDD
        user (str): login de la base de données
        password (str): password de la base de données
        database (str): nom de la base de données
    Returns:
        maria.connections.Connection: appel vers la base de données
    """
    try:
        connexion = maria.connect(host=host,
                                  port=port,
                                  user=user,
                                  password=password,
                                  database=database)
    except maria.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    
    return connexion


def add_datas(cnx: Connection , data: p.DataFrame):
    """_summary_ : permet d'ajouter un client dans la base de données
    Args:
        cnx (maria.connections.Connection): appel vers la base de données
        data (p.DataFrame): DataFrame contenant les données
    """
    # on crée un curseur. Un curseur permet de parcourir les enregistrements d'un résultat
    curseur = cnx.cursor()
    # on crée une requête sql pour ajouter les clients
    sql = "INSERT INTO movie (id_imdb, release_date, review_score, title) \
        VALUES (%s, %s, %s, %s)"
    
    for index, row in data.iterrows():
        
        # check and change NAN values
        if p.isna(row["RELEASE YEAR"]):
            row["RELEASE YEAR"] = 0
        if p.isna(row["IMDB RATING"]):
            row["IMDB RATING"] = 0
        if p.isna(row["TITLE"]):
            row["TITLE"] = "None"

        # conv imdb rating from float to string
        row["IMDB RATING"] = str(row["IMDB RATING"])
        
        # on exécute la requête sql
        curseur.execute(sql, \
            (row["IMDB ID"], row["RELEASE YEAR"], row["IMDB RATING"], row["TITLE"]))
        
    # on commit les changements. Commiter permet de valider les changements
    cnx.commit()
    # on ferme la connexion (c'est raccrocher le téléphone)
    cnx.close()