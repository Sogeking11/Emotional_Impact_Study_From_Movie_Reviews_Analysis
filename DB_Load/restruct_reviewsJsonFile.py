"""
This script aims to restructure the reviews json file produced from API.
"""

# Import Packages and modules
import json
import logging
import pandas as pd
import re
from pathlib import Path




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


def restruct_ReviewsJsonFile(jsonFile):
    """Aims to restructured as needed the reviews json source file
    produced from API.
    This function will put in place where the source file is a new JsonFile
    with the needed structure, its name will be formed with the source file name
    where we add the _restructured at the end.

    Args:
        jsonFile (str): Path of the malformed json file according to our needs
    
    Returned:
        json: restructured json object according to our needs
    """

    # make from filpath Path object
    file_path = Path(jsonFile)

    with open(file_path, 'r', encoding='utf-8') as openfile:
    
        # Reading from json file
        try:
            json_object = json.load(openfile,)
        except ValueError as e:
            logging.error('invalid json: %s' %e)


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

        

    # create new filename
    new_filename = str(file_path.stem) + '_restructured.json'
    new_filename = file_path.parent / new_filename
  
    with open(new_filename, 'w', encoding='utf-8') as outfile:
        json.dump(restruct_json, outfile, ensure_ascii=False, indent=4)

    return restruct_json