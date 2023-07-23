import json
import logging
import pandas as pd
import re

def extract_source_string(url):
    """ 
    Extract source string from url.
    Return source string or False if it does not exist.
    """
    
    # here is to extract source string from url
    pattern = r"\.([^.]*)\."
    match = re.search(pattern, url)
    if match:
        source = match.group(1)
        return source
    else:
        return False


def restruct_redaJsonFile(jsonFile):
    """Aims to restructured as needed the reviews json source file
    produced by Reda.

    Args:
        jsonFile (json): malformed json file according to our needs
    
    Returned:
        json: restructured json file according to our needs
    """

    with open(jsonFile, 'r', encoding='utf-8') as openfile:
    
        # Reading from json file
        try:
            json_object = json.load(openfile,)
        except ValueError as e:
            logging.error('invalid json: %s' % e)


    # convert json object to a pandas dataframe
    df = pd.DataFrame(json_object)
    print(df.head())

    # get list of all unique ids
    list_ids = df['id'].unique().tolist()

    # restructured json
    restruct_json = {}

    # structure json by movie id 
    for id in list_ids:
        df_uniqueMovie = df[df['id'] == id]
        restruct_json[id] = []
        
        # go on dataframe and get all reviews for each movie
        for index, row in df_uniqueMovie.iterrows():
            dict = {}
            dict['score'] = row['score']
            dict['text'] = row['comment']
            dict['date'] = row['date']

            # extract source string from url if it exists
            review_url = row['review_url']
            dict['source'] = "None"
            if extract_source_string(review_url):
                dict['source'] = extract_source_string(review_url)

            dict['url'] = row['review_url']
            dict['username'] = row['user']
            dict['user_url'] = row['user_url']
            restruct_json[id].append(dict)

        

    # write json to file
    file_name = 'datas/test_reviews_restructured.json'
    with open(file_name, 'w', encoding='utf-8') as outfile:
        json.dump(restruct_json, outfile, ensure_ascii=False)

    return file_name

if __name__ == "__main__":
    restruct_redaJsonFile("datas/test_reviews.json")