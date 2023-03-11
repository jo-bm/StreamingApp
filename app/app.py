import os,re
from flask import Flask, render_template, url_for, redirect, send_file,Response
from werkzeug.exceptions import HTTPException
import logging,json_logging,sys
from functions import list_files_in_folder
from views import views
from google.cloud import storage



# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)
app.register_blueprint(views)

json_logging.init_flask(enable_json=True)   
json_logging.init_request_instrument(app)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

