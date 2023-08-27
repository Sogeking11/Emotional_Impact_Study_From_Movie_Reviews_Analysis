import os
import logging
from pathlib import Path

from cloudevents.http import from_http
import gcsfs


from flask import Flask, request, render_template

from loadEnv import loadEnv
from DB_Load import load_movies, load_reviews



# logging configuration
logger = logging.getLogger(__name__)
# creates Handlers
handler_1 = logging.FileHandler(filename="logs/" + __name__ + ".log", mode="w")
# setting handler
handler_1.setLevel(logging.DEBUG)
# logger level
logger.setLevel(logging.INFO)
# formatters + adding them on handlers
formatter_1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler_1.setFormatter(formatter_1)
logger.addHandler(handler_1)

bucket =""

# load on db
def load(filename):
    """Load a json file to DB
    
    Args:
        filename (str): name of the json file
    """

    
    # handle the bucket
    gcs_file_system = gcsfs.GCSFileSystem(project="CineMotion-Artifact-Stockage")
    gcs_json_path = "gs://cinemotion_bucket/" + filename
    fileToLoad = gcs_file_system.open(gcs_json_path)

    if "Movies" in filename:
        # Load file to DB
        logger.info(f"Loading {fileToLoad} to DB")
        load_movies(fileToLoad)
    elif "Reviews" in filename:
        # Load file to DB
        logger.info(f"Loading {fileToLoad} to DB")
        load_reviews(fileToLoad)
    else:
        logger.info(f"No load for {fileToLoad}")

    # close the file

# for GCP to lesson as a web server
app = Flask(__name__)

# [START eventarc_http_quickstart_handler]
# [START eventarc_audit_storage_handler]
@app.route("/", methods=["POST"])
def index():
    # Create a CloudEvent object from the incoming request
    event = from_http(request.headers, request.data)
    # Gets the GCS bucket name from the CloudEvent
    # Example: "storage.googleapis.com/projects/_/buckets/my-bucket"

    # get the filename that has been added to the bucket
    bucket = event.get("subject")
    filename = bucket.replace("objects/", "")

    print(f"Detected change in Cloud Storage bucket: {bucket}")
    load(filename)
    return (f"Detected change in Cloud Storage bucket: {bucket}", 200)


# route /
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "Hello Guys, This message to inform that the {bucket} is now sending to db, hope db is is feeding now!"
    return render_template('index.html',message=message,)




if __name__ == '__main__':

    # check
    print("Hello World !")

    # lesson on port as a web service
    # GCP Cloud service mandatory
    server_port = os.environ.get('PORT', '8081')
    app.run(debug=True, port=server_port, host='0.0.0.0')