import sys
import pandas

from dataset_extract_stock import scrap_data as scrap

def feedCsv(csvfile):
    """
    Take csv file as parameter and feed it with TITLE, RELEASE YEAR, IMDB RATING properties
    for each rows by using scrap_data.py module to find properties
    on IMDB website.
    Cause it can take long time to scrap datas a countdown will permit to know
    when operation will finished on stdout.

    Args:
        csvfile (str): the csv file that have been made by make_csv.py module
    """

    df = pandas.read_csv(csvfile)
    
    totalLines = len(df)
    totalLines = totalLines//100 # just a try
    for i in range(totalLines):
        # get imdb id from data frame
        imdb_id = df.loc[i, 'IMDB ID']

        xpath = scrap.data_prop["title"]  
        df.loc[i, 'TITLE'] = scrap.getData(imdb_id, xpath)

        xpath = scrap.data_prop["release_year"]
        df.loc[i, 'RELEASE YEAR'] = scrap.getData(imdb_id, xpath)

        xpath = scrap.data_prop["imdb_rating"]
        df.loc[i, 'IMDB RATING'] = scrap.getData(imdb_id, xpath)

        sys.stdout.write('\r' + csvfile)
        # countdown
        sys.stdout.write('\r'+ str(totalLines-(i+1)) + "/"+ str(totalLines))                
        sys.stdout.flush()

    df.to_csv(csvfile, index=False)