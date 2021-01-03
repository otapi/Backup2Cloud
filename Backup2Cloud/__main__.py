import configparser
import os
import tempfile
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload


def zipencrypt(folder, zip):
    pass

def unzipdecrypt(zip, folder):
    pass

def gdrive(credentialfile):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialfile, ['https://www.googleapis.com/auth/drive.metadata.readonly'])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def downloadfile(credentialfile, file):
    service = gdrive(credentialfile)
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    service.close()
    pass

def uploadfile(credentialfile, file):
    service = gdrive(credentialfile)
    media = MediaFileUpload(file, mimetype='application/zip', resumable=True)
    request = service.files().insert(media_body=media, body={'name': os.path.basename(file)})
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print("Uploaded %d%%." % int(status.progress() * 100))
        print("Upload Complete!")
    service.close()

def Main():
    print("Backup2Cloud")

    print("Load INI")
    configfile = os.path.dirname(os.path.abspath(__file__))+"/Backup2Cloud.ini"
    logging.info(f"Using config {configfile}")
    config = configparser.ConfigParser()
    config.read(configfile)
    with tempfile.TemporaryDirectory() as tempdir:
        for cloudplace in config.sections():
            print(f"Process f{cloudplace}")
            credentialfile = None
            folder = None

            for (key, val) in config.items(cloudplace):
                if key=="credentials":
                    credentialfile = val
                else:
                    folder = val
                    zipfile = os.path.join(tempdir, folder, ".zip")
                    # process

            

### set up logging
import logging, sys, socket

machinename = socket.gethostname()
logging.basicConfig(
    level=logging.INFO,
    #format=f"%(message)s\t%(asctime)s\t{machinename}\t%(threadName)s\t%(levelname)s",
    format=f"%(message)s",
    handlers=[
        #logging.FileHandler(f"{logfile}.txt"),
        logging.StreamHandler(sys.stdout)
        #TalkerHandler()
    ]
)


# main run
try:
    Main()
except Exception:
    logging.exception("Fatal error")

