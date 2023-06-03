import os
import sys
import re
import pandas


from db_stock import connect_to_db
import mySecrets


def get_numbered_files(directory):
    # regex
    a = "_{1}.+"
    
    file_dict = {}

    fileNumber = len(os.listdir(directory))
    
    for filename in os.listdir(directory):
        # get position from the filename
        posFile = re.sub(a, "", filename)
        # get score reviewfromfilename
        filename = str(filename)
        score = filename.replace(".txt", "")
        reg = "^.+_"
        score = re.sub(reg, "", score)
        file_dict[posFile] = (filename, score)

        #file_list[posFile] = filename
   
    return file_dict

# will return the unique idMovie to push as foreign key in review table
# in a part of movie table.
# this due to copies we have in different dataset files
def get_idMovie(cursor, lineNumber, filmId, startAt):

    end = startAt + lineNumber
    if startAt != 0:
        startAt = startAt + 1

    left = str(end)
    startAt = str(startAt)
    lineNumber = str(lineNumber)
    
    # sql request
    sql = "select id_movie from movie where (id_movie between " + startAt + " and " + left + ") and id_imdb = \"" + filmId + "\""
    cursor.execute(sql)

    # get result from sql request
    id_movie = curseur.fetchall()

    return id_movie[0], end

def pushToReviewTable(cursor, review, score, foreign_id_movie):
    cursor = cnx.cursor()
    # sql request
    score = int(score)
    sql = "INSERT INTO review (score, text, movie_idmovie, source, reviewer_id_reviewer) \
        VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql,(score, review, foreign_id_movie, "imdb", 12))

    cnx.commit()





if __name__ == "__main__":

    print("Hello World !")

    # get cursor from db
    db_host = mySecrets.secrets["DATABASE_HOST"]
    db_port = mySecrets.secrets["DATABASE_PORT"]
    db_user = mySecrets.secrets["DATABASE_USER"]
    db_password = mySecrets.secrets["DATABASE_PASSWORD"]
    db_database = mySecrets.secrets["DATABASE_NAME"]

    # connect to BDD
    cnx = connect_to_db(db_host, db_port, db_user, db_password, db_database)

    # csvfile and directories
    testPath = "../aclImdb/test/"
    trainPath = "../aclImdb/train/"

    source_dict = {
        testPath + "urls_neg.csv": testPath + "neg/",
        testPath + "urls_pos.csv": testPath + "pos/",
        trainPath + "urls_neg.csv": trainPath + "neg/",
        trainPath + "urls_pos.csv": trainPath + "pos/",
        trainPath + "urls_unsup.csv": trainPath + "unsup/",
    }

    startAt = 0
    end = 0
    for csvFile, directory in source_dict.items():
        startAt = end
        # dictionnary of filenames their keys are their position number in string
        filePosition_dict = get_numbered_files(directory)
    
        # get dataframe from csv
        df = pandas.read_csv(csvFile)

        # in csv file from begin to end of file
        # line number to treat in movie table in that csv
        lineNumber = len(df)

        # stdout to see which file is treated
        sys.stdout.write('\n' + str(csvFile) + '\n')
        sys.stdout.flush()



        row_count = 0
        for index, row in df.iterrows():
            review_numb_per_film = row["COPIES NUMBER"]
            filmId_from_csv = row["IMDB ID"]

            # from db, get movie id with imdb_id
            # get cursor
            curseur = cnx.cursor()

            # call func that care of part in movie table relatively to
            # the csv file we are in
            myList = get_idMovie(curseur, lineNumber, filmId_from_csv, startAt)
            foreign_id_movie = myList[0]

            # this must help to push from files data consecutively
            end = myList[1]


            # go to directory reviews relative to csv file to get reviews
            # get file number in that directory
            for i in range(review_numb_per_film):
                review = ""
                str_i = str(row_count + i)
                reviewAndScore = filePosition_dict[str_i]
                reviewFileName = directory  + "/" + reviewAndScore[0]
                score = reviewAndScore[1]
                with open(reviewFileName, 'r') as f:
                    review = f.readline()
                
                pushToReviewTable(cnx, review, score, foreign_id_movie)

            row_count = row_count + review_numb_per_film

            # countdown
            sys.stdout.write('            \r'+ str(index + 1) + "/ " + str(lineNumber)) 
            sys.stdout.write('             le startAt actuel est: ' + str(startAt) + ' le END actuel est: ' + str(end))                 
            sys.stdout.flush()

    cnx.close()