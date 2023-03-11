
import os,re
from flask import Flask, render_template, url_for,Response, Blueprint
from werkzeug.exceptions import HTTPException
import logging
from functions import list_files_in_folder

from google.cloud import storage


currentfolder = ''

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')


@views.route('/file_list/<folder>')
def file_list(folder):
    global currentfolder
    currentfolder = folder
    
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

    return render_template('episodes.html', episodes=episode_dict, seriesname=currentfolder)


@views.route('/play/<filename>')
def play(filename):
    global currentfolder

    BUCKET_NAME = os.environ.get('BUCKET_NAME')

    file_name = f'{currentfolder}/{filename}'

    client = storage.Client()

    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)

    headers = {"Range": "bytes=0-"}

    return Response(blob.download_as_bytes(), headers=headers, mimetype="video/mp4")



@views.errorhandler(Exception)
def handle_exception(error):
    # pass through HTTP errors
    if isinstance(error, HTTPException):
        return error
    logging.critical("HTTP error has occurred in: %s", error)
    # now you're handling non-HTTP exceptions only
    return render_template("404.html", error=error)