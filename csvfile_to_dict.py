import pandas as pd
import ast
import re
import logging
import json

# basic config for logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log.log', filemode='w')


def getRoleInDF(list_dict: list):
  list_role = ast.literal_eval(list_dict)
  df_role = pd.DataFrame.from_dict(list_role)
  df_role = df_role.drop_duplicates()
  return df_role

def getListFromString(keyword_string: str):
  mylist = keyword_string[1:-1].split(',')
  myReg = "\W+"
  result_list = list(map(lambda x:re.sub(myReg,"",x), mylist))
  return result_list

def csvToDictFile(csv_file: str):
  myDf = pd.read_csv(csv_file, delimiter=';', header=0)

  lineerror = 1
  myDict = {}
  for i in range(0, len(myDf)):
    try:
      # get title
      title = myDf['title'][i]
      #get certification
      certification = myDf['certification'][i]
      # get revenue
      revenue = myDf['revenue'][i]
      # get budget
      budget = myDf['budget'][i]
      # get review score
      review_score = myDf['review_score'][i]
      # get release date
      release_date = myDf['release_date'][i]
      # get runtime
      runtime = myDf['runtime'][i]
      # get popularity
      popularity = myDf['popularity'][i]
      # get synopsis
      synopsis = myDf['synopsis'][i]
      # get tmdb identification
      id_tmdb = myDf['id_tmdb'][i]
      # get imdb idenfication
      id_imdb = myDf['id_imdb'][i]
      # get production list
      prod_list = getListFromString(myDf['production_companies'][i])
      # get country list
      country_list = getListFromString(myDf['countries'][i])
      # get genre list
      genre_list = getListFromString(myDf['genres'][i])
      # role, and participant entities : name, gender, popularity, role
      df_role = getRoleInDF(myDf['role'][i])
      # keywords list
      keywords_list = getListFromString(myDf['keywords'][i])

      # preparing data in dict
      # movie 
      movie = {
                "title":title,
                "certification":certification,
                "revenue":revenue,
                "budget":budget,
                "review_score":review_score,
                "release_date":release_date,
                "popularity": 2.5, # valeur absente
                "runtime":runtime,
                "synopsis":synopsis, 
               }
      # sources
      sources = {"imdb" : id_imdb, "tmdb" : id_tmdb}

      # participant roles case
      role = {}
      for row in range(0, len(df_role)):
        role[row] = {
                        "name":df_role['name'][row],
                        "gender":df_role['gender'][row],
                        "popularity":df_role['popularity'][row],
                        "role":df_role['role'][row]
                      }
        
      #put all inside myDict
      myDict[i] = {
                    "movie":movie,
                    "sources":sources,
                    "participant_roles":role,
                    "keywords":keywords_list,
                    "production_companies":prod_list,
                    "countries":country_list,
                    "genres":genre_list,
                    "role":role
                    }
      
    except Exception:
      lineerror += i
      logging.exception(f"Syntax error on line {lineerror} from csv file")
      continue
  
  # convert to json string
  #json_string = json.dumps(myDict)

  return myDict


if __name__ == "__main__":

  myDict = csvToDictFile("testapi100.csv")
  print(myDict)
