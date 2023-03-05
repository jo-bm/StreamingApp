import os,re
from flask import Flask, render_template, url_for, redirect, send_file,Response
from werkzeug.exceptions import HTTPException
import logging,json_logging,sys
from functions import list_files_in_folder

from google.cloud import storage
from google.oauth2.service_account import Credentials


# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)

json_logging.init_flask(enable_json=True)   
json_logging.init_request_instrument(app)


currentfolder = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return render_template('video.html')



@app.route('/file_list/<folder>')
def file_list(folder):
    global currentfolder
    currentfolder = folder
    folder_path = f'static/{folder}'
    
    files = list_files_in_folder(f"{folder}/")

    # Extract episode number from filenames using regex and store in a dictionary
    episode_dict = {}
    for file in files:
        match = re.search(r'S\d+E(\d+)', file)
        if match:
            episode_num = match.group(1)
            episode_dict[int(episode_num)] = file

    # Sort the episode dictionary by episode number
    episode_dict = dict(sorted(episode_dict.items()))

    return render_template('episodes.html', folder_path=folder_path, episodes=episode_dict, seriesname=currentfolder)


@app.route('/play/<filename>')
def play(filename):
    global currentfolder

    BUCKET_NAME = os.environ.get('BUCKET_NAME')

    #file_name = "Black_Lagoon/Black_Lagoon_S01E01.m4v"
    file_name = f'{currentfolder}/{filename}'

    credentials = Credentials.from_service_account_file("/media/jack/Second/proj/psychic-mason-374614-ef84d96f27ae.json")
    client = storage.Client(credentials=credentials)

    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)


    headers = {"Range": "bytes=0-"}

    return Response(blob.download_as_bytes(), headers=headers, mimetype="video/mp4")
    
    



@app.errorhandler(Exception)
def handle_exception(error):
    # pass through HTTP errors
    if isinstance(error, HTTPException):
        return error
    logging.critical("HTTP error has occurred in: %s", error)
    # now you're handling non-HTTP exceptions only
    return render_template("404.html", error=error)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

