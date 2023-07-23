import pandas as pd
import json
from datetime import date

from dataset_extract_stock import get_numbered_files 



def csv_Dataset_To_Json_File(csv_path, filenamePart):
    """This function convert a csv file to a json file.
    The csv file must have the following columns:
    COPIES NUMBER, IMDB ID, TITLE, RELEASE YEAR, IMDB RATING
    The json file will have the following columns:
    nb_cpy, id_imdb, title, release_date, imdb_rating

    Args:
        csv_path (str): file path name that will be operate
        filenamePart (str): filename part to distinguish from others dataset source files

    Returns:
        dataframe: image of the csv file received
    """

    # make csv file a dataframe
    df = pd.read_csv(csv_path, header=0)

    # rename columns
    df.rename(columns={
        'COPIES NUMBER': 'nb_cpy',
        'IMDB ID':'id_imdb',
        'TITLE':'title',
        'RELEASE YEAR':'release_date',
        'IMDB RATING':'imdb_rating'
        }, inplace=True)
    
    # transform date
    df['release_date'] = df['release_date'].\
                                dropna().\
                                apply(lambda x: str(date(int(x), 1, 1)))
    
    #transform null values on title parameter
    df['title'] = df['title'].apply(lambda x: "None" if pd.isnull(x) else x)
    
    # convert in json
    jsonFormat = df.to_json(orient='records')

    filenamePath = "./datas/" + filenamePart + "_dataset.json"
    # write on json file
    with open(filenamePath, 'w') as f:
        f.write(jsonFormat)

    return df

def get_Review_Text(filename):
    """This function get the review text from a file.

    Args:
        filename (str): file path name that will be operate

    Returns:
        str: review text
    """

    # open file
    with open(filename, 'r') as f:
        review = f.read()
        return review
    
def make_Reviews_Json_File(source, df_Movies, filenamePart):
    """This function make a json file that contain all reviews of movies.

    Args:
        source (str): file path name that will be operate
        df_Movies (dataframe): dataframe that contain all movies information
        filenamePart (str): filename part to distinguish from others dataset source files

    """

    # create the dict that include filename reviews and their scores according to movies csv files generated
    mydictReview_dir = get_numbered_files(source)

    # first review number for a movie id
    # it start at 0 for the first movie find the dataframe
    review_Number_Start_At = 0

    # dictionnary that will grab all reviews reference per movies id
    reviews_File_Ref_dict= {}
    for index, row in df_Movies.iterrows():
        # care of imdb_id copies
        if row['id_imdb'] not in reviews_File_Ref_dict:
            reviews_File_Ref_dict[row['id_imdb']] = []

        # last review file calcul

        # create the dict that include filename reviews and their scores according to movies csv files generated
    # this source has been made in dataset_extract_stock module and is needed to complete dataset Json review file
    mydictReview_dir = get_numbered_files(source)

    # first review number for a movie id
    # it start at 0 for the first movie find the dataframe
    review_Number_Start_At = 0

    # dictionnary that will grab all reviews reference per movies id
    reviews_File_Ref_dict= {}
    for index, row in df_Movies.iterrows():
        # care of imdb_id copies
        if row['id_imdb'] not in reviews_File_Ref_dict:
            reviews_File_Ref_dict[row['id_imdb']] = []

        # last review file calcul
        review_Number_End_At = review_Number_Start_At + row['nb_cpy'] - 1

        # make a list start and end
        if review_Number_Start_At != review_Number_End_At:
            list = [review_Number_Start_At, review_Number_End_At]
        else:
            list = [review_Number_Start_At]

        # push reviews start and end in list according to movie id
        reviews_File_Ref_dict[row['id_imdb']].append(list)

        # new origine calcul
        review_Number_Start_At += row['nb_cpy']

    # make a fusion between reviews identification per movies dictionnary 
    # and the dictionnary that have image of directory content where are review files
    myFinalReviews_dict = {}
    for key, value in reviews_File_Ref_dict.items():

        # init each key got a list as value
        myFinalReviews_dict[key] = []

        # initialise the start and end review file concerned by the movie
        lastFile = None
        list = value[0]
        if len(list) == 2:
            lastFile = list[1]
        startFile = list[0]

        review_dict = {}
        if lastFile is not None:
            # means there is more than one review for the movie
            for i in range(startFile, lastFile + 1):
                # the filename is send to get_Review_Text function
                indice_str = str(i)
                mylist = mydictReview_dir[indice_str]
                review_text = get_Review_Text(source + mylist[0])
                review_score = mylist[1]

                # parameter needed to get just one row in reviewer table
                review_dict['url'] = "From_DataSet"

                review_dict['text'] = review_text
                review_dict['score'] = review_score
                myFinalReviews_dict[key].append(review_dict)
                review_dict = {}
        else:
            # means there is only one review for the movie
            startfile_str = str(startFile)
            review_text = get_Review_Text(source + mydictReview_dir[startfile_str][0]) 
            review_score = mydictReview_dir[startfile_str][1]
            
            # parameter needed to get just one row in reviewer table
            review_dict['url'] = "From_DataSet"

            review_dict['text'] = review_text
            review_dict['score'] = review_score
            myFinalReviews_dict[key].append(review_dict)


    # convert dict in json
    jsonFormat = json.dumps(myFinalReviews_dict)

    filenamePath = "./datas/" + filenamePart + "_Reviews_dataset.json"
    # save json in file
    with open(filenamePath, 'w') as f:
        f.write(jsonFormat)



if __name__ == "__main__":
    
    # directories
    org = "../aclImdb/"
    testPath = org + "test/"
    trainPath = org + "train/"

    # dataset movies csv files
    fileList = [testPath + "urls_neg.csv",
                testPath + "urls_pos.csv",
                trainPath + "urls_neg.csv",
                trainPath + "urls_pos.csv",
                trainPath + "urls_unsup.csv"]
    
    # here we make the link between generated csv files and the directory where we can find
    # all reviews
    source_dict = {
        fileList[0]: testPath + "neg/",
        fileList[1]: testPath + "pos/",
        fileList[2]: trainPath + "neg/",
        fileList[3]: trainPath + "pos/",
        fileList[4]: trainPath + "unsup/"
    }
    
    # create all json files from dataset csv files 
    # and their respective directory
    for key, value in source_dict.items():

        # part of file name to produce
        fileNamePartResult = key.split("/")[2] + "-" + key.split("/")[-1].split(".")[0]

        # convert dataset movies csv file in json file  
        df_result = csv_Dataset_To_Json_File(key, fileNamePartResult)

        # make json file with all reviews in its corresponding directory
        mySource = source_dict[key]
        make_Reviews_Json_File(mySource, df_result, fileNamePartResult)

   