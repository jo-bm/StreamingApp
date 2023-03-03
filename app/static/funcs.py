
import os
from google.cloud import storage


def dirdownload(directory_name,bucket_name):

    # create a client instance
    client = storage.Client()

    # get the bucket and list all blobs in the directory
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=directory_name)

    # create a directory on the local machine to store the files
    os.makedirs(directory_name, exist_ok=True)

    # download each file in the directory
    for blob in blobs:
        # construct the file path on the local machine
        file_path = os.path.join(directory_name, blob.name.replace(directory_name, ""))

        # download the file to the local machine
        blob.download_to_filename(file_path)

        print(f"File {blob.name} has been downloaded to {file_path}")





#get the directory names from environment variable
series_csv = os.getenv("SERIESCSV")
directory_names = series_csv.split(",")
bucket_name = os.environ.get("BUCKET_NAME")

# loop through each directory name and call dirdownload()
for directory_name in directory_names:
    
    dirn = directory_name + '/'
    dirdownload(dirn,bucket_name)