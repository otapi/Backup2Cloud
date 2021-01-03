import configparser
import os
import tempfile
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload


def zipencrypt(folder):
    pass

def unzipdecrypt(folder):
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
                credentialfile, ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive.file'])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds, cache_discovery=False)
    
    return service

def listfiles(credentialfile):
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

def downloadfile(credentialfile, file):
    pass

def uploadfile(credentialfile, file):
    if not os.path.isfile(file):
        raise Exception(f"The file to upload does not exists: {file}")
    service = gdrive(credentialfile)
    media = MediaFileUpload(file, mimetype='application/zip', resumable=True)

    
    request = service.files().create(media_body=media, body={'name': os.path.basename(file)})
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print("Uploaded %d%%." % int(status.progress() * 100))
        logging.info(f"Upload Complete!")
    service.close()

def Main():
    logging.info(f"Backup2Cloud")

    logging.info(f"Load INI")
    configfile = "Backup2Cloud.ini"
    logging.info(f"Using config {configfile}")
    config = configparser.ConfigParser()
    config.read(configfile)
    with tempfile.TemporaryDirectory() as tempdir:
        for cloudplace in config.sections():
            logging.info(f"Process {cloudplace}")
            credentialfile = None
            zipfile = None

            for (key, val) in config.items(cloudplace):
                if key=="credentials":
                    credentialfile = val
                    continue
                elif key=="folder":
                    folder = val
                    zipfile = os.path.join(tempdir, folder)
                    zipencrypt(folder=zipfile)
                elif key=="file":
                    zipfile = val

                if not credentialfile:
                    raise Exception(f"Credentials as missing from INI for {cloudplace}")
                
                if not zipfile:
                    raise Exception(f"Either the folder or file is missing from INI for {cloudplace}")
                uploadfile(credentialfile=credentialfile, file=zipfile)

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

