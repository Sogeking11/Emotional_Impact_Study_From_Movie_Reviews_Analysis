import csv

def csvInit(filename):
    """
    the csvInit function will create a new csv file with
    element from dataset that will finally be put inside
    the table CINE_EMOTION.movie.
    the first element in each line will be the copies number of a
    lines we found in source file.
    The second and last element will be the imdb id of each films
    we found in the source file.

    Args:
        filename (str): Source file
    """

    
    # create csv file
    csvfile = filename.replace('txt', 'csv')
    with open(csvfile, 'w', newline='') as csvfile:
        fieldnames = ['COPIES NUMBER', 'IMDB ID', 'TITLE', 'RELEASE YEAR', 'IMDB RATING']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # mask to get imdb_id from url
        a = "http://www.imdb.com/title/"
        b = "/usercomments"

        imdb_id =""
        # open source file to get datas from it
        with open("../testfile.txt", 'r') as f:
            for line in f.readlines():

                # get imdb Id
                line = line.replace(a, '')
                line = line.replace(b, '')

                # exclude all line return in each lines except for the last line
                if '\n' in line:
                    line = line.replace('\n', '')

                if line == imdb_id:
                    cmpt += 1
                else:
                    if imdb_id != "":
                        # put cmpt and imdb Id in csv file
                        writer.writerow({'COPIES NUMBER':cmpt, 'IMDB ID': imdb_id})
                        
                    imdb_id = line
                    cmpt = 1
            # put cmpt and imdb Id in csv file
            writer.writerow({'COPIES NUMBER':cmpt, 'IMDB ID': imdb_id})

