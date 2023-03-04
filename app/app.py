import os,re
from flask import Flask, render_template, url_for, redirect, send_file
from werkzeug.exceptions import HTTPException
import logging,json_logging,sys

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
    try:
        files = os.listdir(folder_path)
    except FileNotFoundError:   
        return render_template('downloading.html')

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
    video_path = f'static/{currentfolder}/{filename}'
    return send_file(video_path, mimetype='video/mp4')

@app.route('/status')
def status():
    series_csv = os.getenv("SERIESCSV")
    directory_names = series_csv.split(",")
    print(directory_names)
    for i in directory_names:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), f"static/{i}")):
            return "part of the files still downloading"
    return "all files downloaded"

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

