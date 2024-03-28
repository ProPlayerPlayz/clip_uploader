import httplib2 # pip install httplib2
import os
import random
import sys
import time

from googleapiclient.discovery import build # pip install google-api-python-client
from googleapiclient.errors import HttpError # pip install google-api-python-client
from googleapiclient.http import MediaFileUpload # pip install google-api-python-client
from oauth2client.client import flow_from_clientsecrets # pip install oauth2client
from oauth2client.file import Storage # pip install oauth2client
from oauth2client.tools import argparser, run_flow # pip install oauth2client

# Code Snippet from Google Documentation
# ------------------------------------------------------------------------------------------------
# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.cloud.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json" # This is the file that contains the client_id and client_secret

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_EDIT_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_MANAGE_SCOPE = "https://www.googleapis.com/auth/youtube"
SCOPES = [YOUTUBE_UPLOAD_SCOPE, YOUTUBE_EDIT_SCOPE, YOUTUBE_MANAGE_SCOPE]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
# ------------------------------------------------------------------------------------------------


# Code Snippet from Google Documentation which has been modified to fit the program
# ------------------------------------------------------------------------------------------------

# getting authenticated service without the console part
def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=SCOPES,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0]) # storing the credentials in a file
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)
        print("Storing credentials to " + "%s-oauth2.json" % sys.argv[0])

    return build(YOUTUBE_API_SERVICE_NAME,
                 YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, file, vidtitle):
    tags = None
    body=dict(
        snippet=dict(
        title=vidtitle,
        description="This File was uploaded using API",
        tags=tags,
        categoryId=22
        ),
        status=dict(
        privacyStatus="unlisted"
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting "chunksize" equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        media_body = MediaFileUpload(file, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)

# ------------------------------------------------------------------------------------------------

# We adopt the same exponential backoff strategy to resume a 
# failed upload from the Google Documentation Examples
# ------------------------------------------------------------------------------------------------

# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print ("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print("Video id '%s' was successfully uploaded." % response['id'])
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

    if error is not None:
      print(error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)

# ------------------------------------------------------------------------------------------------

# Main Program to check if the video already exists in the channel and then upload it

# ------------------------------------------------------------------------------------------------

youtube = get_authenticated_service()
path = "D:\\Editting Stuff Master Version\\Raw Footage\\Valorant"

# getting the list of videos in the channel
list_request = youtube.videos().list(
    part="snippet",
    maxResults=50,
    myRating="like"
)

videos_on_yt = list_request.execute()

# looping through every mp4 file in the folder and checking its name with the list of videos
# if the video already exists, it will not be uploaded
for filename in os.listdir(path):
    if filename.endswith(".mp4"):
        print(filename)
        title = filename.split(".")[0]
        for item in videos_on_yt['items']:
            if item['snippet']['title'] == filename:
                print("Video already exists.")
                break
        else:
            initialize_upload(youtube, os.path.join(path, filename), title)
        continue
    else:
        continue

# ------------------------------------------------------------------------------------------------
# Function Handle to use elsewhere
    
def authenticate(secrets_file):
    global CLIENT_SECRETS_FILE
    CLIENT_SECRETS_FILE = secrets_file
    global youtube
    youtube = get_authenticated_service()
    
def upload_videos(path):
    youtube = get_authenticated_service()
    list_request = youtube.videos().list(
        part="snippet",
        maxResults=50,
        myRating="like"
    )

    videos_on_yt = list_request.execute()

    for filename in os.listdir(path):
        if filename.endswith(".mp4"):
            print(filename)
            title = filename.split(".")[0]
            for item in videos_on_yt['items']:
                if item['snippet']['title'] == filename:
                    print("Video already exists.")
                    break
            else:
                initialize_upload(youtube, os.path.join(path, filename), title)
            continue
        else:
            continue
# ------------------------------------------------------------------------------------------------
