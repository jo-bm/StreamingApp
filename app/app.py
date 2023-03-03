import os,re
from flask import Flask, render_template, url_for, redirect, send_file

app = Flask(__name__)

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
    files = os.listdir(folder_path)

    # Extract episode number from filenames using regex
    episode_dict = {}
    for file in files:
        match = re.search(r'S\d+E(\d+)', file)
        if match:
            episode_num = match.group(1)
            episode_dict[episode_num] = file
    
    return render_template('episodes.html', folder_path=folder_path, episodes=episode_dict, seriesname=currentfolder)



@app.route('/play/<filename>')
def play(filename):
    global currentfolder
    video_path = f'static/{currentfolder}/{filename}'
    return send_file(video_path, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

