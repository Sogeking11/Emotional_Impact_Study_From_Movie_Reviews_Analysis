import pandas
from dataset_extract_stock import make_csv as csv
from dataset_extract_stock import csv_insert
from dataset_extract_stock import db_stock
from dataset_extract_stock import feedReviewTable


def stockMovies_csv(csvFile):
    """    
    Take a csv file which contains data for movie table to send them 
    in movie table.

    Args:
        csvFile (csv): file contains some properties that we can find on movie table
    """

    # read csv and convert dataframe
    df = pandas.read_csv(csvFile)
    
    # connect to BDD
    cnx = db_stock.connect_to_db()
    
    # add datas
    db_stock.add_datas(cnx, df)


def create_feed_csvFiles(filename):
    """   
    Project part One:
    Prepare datas in csv files before send them to database.

    Args:
        filename (str): Here we have urls that have reviews, each line in file is a url.

    Returns:
        str: csv filename
    """
        
    # create csv file
    csvfilename = csv.csvInit(filename)

    # feed csv file
    csv_insert.feedCsv(csvfilename)

    return csvfilename


if __name__ == "__main__":

    # directories
    org = "../aclImdb/"
    testPath = org + "test/"
    trainPath = org + "train/"

    # files concerned
    fileList = [testPath + "urls_neg.txt",
                testPath + "urls_pos.txt",
                trainPath + "urls_neg.txt",
                trainPath + "urls_pos.txt",
                trainPath + "urls_unsup.txt"]
    
    # make csv files and stock them in CINE_EMOTION DB
    csvFilename_list = []
    for i in range(len(fileList)):
        csvFileName = create_feed_csvFiles(fileList[i])
        csvFilename_list.append(csvFileName)

    for i in range(len(csvFilename_list)):
        stockMovies_csv(csvFilename_list[i])

    # here we make the link between generated csv files and the directory where we can find
    # all reviews
    source_dict = {
        csvFilename_list[0]: testPath + "neg/",
        csvFilename_list[1]: testPath + "pos/",
        csvFilename_list[2]: trainPath + "neg/",
        csvFilename_list[3]: trainPath + "pos/",
        csvFilename_list[4]: trainPath + "unsup/"
    }

    # push reviews in DB according to csv files generated
    feedReviewTable(source_dict)