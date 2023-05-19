import csv

def csvInit(filename):
    """
    the csvInit function will create a new csv file with
    element from dataset that will finally be put inside
    the table CINE_EMOTION.movie.
    the first element in each line will be the copies number of a
    line we found in original file.
    The second and last element will be the imdb_id of each films
    we find in the original file.

    """
    # Create csv file
    filename = filename + '.csv'
    numcopy = 0
    imdb_id =""
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['COPIES NUMBER', 'IMDB ID', 'TITLE', 'RELEASE YEAR', 'IMDB RATING']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # open source file and read it
        
        writer.writerow({'COPIES NUMBER':numcopy, 'IMDB ID': imdb_id})
        #writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        #writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
    csvfile.close()

    
    # Open original file
    # get url, count copies, and isolate imdb_id
    # put in csv file first the copies number, secondly the imdb_id
    


    # close all files
   
csvInit("monFichier")
