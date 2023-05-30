import pandas
from dataset_extract_stock import make_csv as csv
from dataset_extract_stock import csv_insert
from dataset_extract_stock import db_stock
from dataset_extract_stock import mySecrets

def stockMovies_csv(csvFile):
    db_host = mySecrets.secrets["DATABASE_HOST"]
    db_port = mySecrets.secrets["DATABASE_PORT"]
    db_user = mySecrets.secrets["DATABASE_USER"]
    db_password = mySecrets.secrets["DATABASE_PASSWORD"]
    db_database = mySecrets.secrets["DATABASE_NAME"]

    # read csv and convert dataframe
    df = pandas.read_csv(csvFile)
    
    # connect to BDD
    cnx = db_stock.connect_to_db(db_host, db_port, db_user, db_password, db_database)
    
    # add datas
    db_stock.add_datas(cnx, df)



def create_feed_csvFiles(filename):
    """
    Project part One:
    Prepare datas in csv files before send them to database.
    """
        
    # create csv file
    csvfilename = csv.csvInit(filename)

    # feed csv file
    csv_insert.feedCsv(csvfilename)

    return csvfilename


if __name__ == "__main__":
    
    path = "../aclImdb/"

    # files concerned
    fileList = [# "test/urls_neg.txt",
                "test/urls_pos.txt",
                "train/urls_neg.txt",
                "train/urls_pos.txt",
                "train/urls_unsup.txt"]
    
    # make csv files and stock them in CINE_EMOTION DB
    csvFilename_list = []
    for i in range(len(fileList)):
        filename = path + fileList[i]
        csvFileName = create_feed_csvFiles(filename)
        csvFilename_list.append(csvFileName)


    #create_feed_csvFiles()
    for i in range(len(csvFilename_list)):
        stockMovies_csv(csvFilename_list[i])