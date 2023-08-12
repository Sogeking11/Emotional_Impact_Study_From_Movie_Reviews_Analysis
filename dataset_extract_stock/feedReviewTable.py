import os
import sys
import re
import pandas

# don't know why when I use it(the import just under that comment) to get get_numbered_files function
# to generate csv reviews in csvDataset-to-Json module
# it's not working
# must be module declaration on __init__ ??
#from db_stock import connect_to_db


def get_numbered_files(directory):
    """
    Generate a dictionnary that got keys corresponding to the position of the review
    and as value a list where we can found the filename and the review's score.

    Args:
        directory (str): Directory path where we got review files

    Returns:
        dictionnary: {position :(filename, score)}
    """

    # regex to extract the review position from filename in directory
    # according to url text file
    reg1 = "_{1}.+"
    
    file_dict = {}
    
    for filename in os.listdir(directory):

        # get position from the filename
        posFile = re.sub(reg1, "", filename)

        # get score reviewfromfilename
        filename = str(filename)
        score = filename.replace(".txt", "")
        # regex to isolate review score in filename
        reg2 = "^.+_"
        score = re.sub(reg2, "", score)
        file_dict[posFile] = (filename, score)
   
    return file_dict


def get_idMovie(cursor, lineNumber, filmId, startAt):
    """ 
    Will return the unique idMovie to push as foreign key in review table
    in a part of movie table.
    this due to copies we have in different dataset files

    Args:
        cursor (DB object): Allow to request our db
        lineNumber (int): Correspond to the range in movie table where to search id_movie
        filmId (str): It's the imdb id we are looking for in movie table
        startAt (int): Row position where to start research

    Returns:
        list: return the movie table key that will be the foreign key in review table,
              and the last row that has been searched that will be the start of the next search.
    """

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
    id_movie = cursor.fetchall()

    return id_movie[0], end


def pushToReviewTable(cnx, review, score, foreign_id_movie):
    """
    Push record datas in review table.

    Args:
        cursor (DB object): Allow to request our db
        review (BloB): The review itself.
        score (str): Te review score.
        foreign_id_movie (int): id corresponding to the film concerned by the review.
    """
    cursor = cnx.cursor()

    # sql request
    score = int(score)
    sql = "INSERT INTO review (score, text, movie_idmovie, source, reviewer_id_reviewer) \
        VALUES (%s, %s, %s, %s, %s)"
    
    # when we execute, we need to give a value reviewer_id_reviewver cause it can't stay null
    # that's why we give 12 as value it can be any integer
    cursor.execute(sql,(score, review, foreign_id_movie, "imdb", 12))

    cnx.commit()



def feedReviewTable(source_dict):
    """
    Here we have a general function that go inside all csv files generated before.
    it goes line by line, taking imdb id, go to movie table to take the movie id corresponding.
    This movie id will be the foreign key in review table.
    After this, the function goes to the corresponding directory where we can find reviews,
    retrieve scorefrom filename and the review text to push them on review table without forgot
    the corresponding foreign key.

    Args:
        source_dict (dictionnary): here we make the link between generated csv files
                                   and the directory where we can find all reviews.
    """

    # connect to BDD
    cnx = connect_to_db()


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

        # stdout to see which file is in operation
        sys.stdout.write('\n' + str(csvFile) + '\n')
        sys.stdout.flush()


        # help to make correspondance between the review file in the directory and the record in the csv file
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

                # open file to get review
                with open(reviewFileName, 'r') as f:
                    review = f.readline()

                # send the review, score and foreign_id_movie in review table
                pushToReviewTable(cnx, review, score, foreign_id_movie)

            # Init row_count
            row_count = row_count + review_numb_per_film

            # countdown
            sys.stdout.write('            \r'+ str(index + 1) + "/ " + str(lineNumber)) 
            sys.stdout.write('             le startAt actuel est: ' + str(startAt) + ' le END actuel est: ' + str(end))                 
            sys.stdout.flush()

    cnx.close()