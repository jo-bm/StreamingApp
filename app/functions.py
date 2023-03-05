import os
from google.cloud import storage




def list_files_in_folder(folder_name):

    client = storage.Client()

    bucket = client.get_bucket(os.environ.get('BUCKET_NAME'))
    blobs = bucket.list_blobs(prefix=folder_name)

    blobs = [i.name.split('/')[1] for i in blobs]
    return blobs
 

