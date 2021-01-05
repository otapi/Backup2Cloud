import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import logging

# Class to upload, download and list files on Google Drive.
class GDrive():
    def __init__(self, name, credentialfile=None):
        self.name = name
        self.service = None
        if credentialfile:
            self.connect(credentialfile)

    def connect(self, credentialfile):
        if self.service:
            logging.info(f"Already connected to GDrive. Avoid connecting multiple times by the same GDrive object.")

        logging.info(f"Connect to GDrive using {credentialfile}...")
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        picklefile=f"{self.name}_token.pickle"
        if os.path.exists(picklefile):
            with open(picklefile, 'rb') as token:
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
            with open(picklefile, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds, cache_discovery=False)
        logging.info(f"Connected!")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.service:
            self.service.close()

    def listfiles(self):
        if not self.service:
            raise Exception("Call Connect before start using GDrive")
        results = self.service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        return items

    def printfiles(self):
        items = self.listfiles()
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

    # Check if file exists with exact name on GDrive. Returns the id of the file if yes.
    def fileexists(self, filename):
        items = self.listfiles()
        if items:
            for item in items:
                if item['name'] == filename:
                    return item['id']
        return None

    # Upload specified local filepath to GDrive. Delete already existing one if overwrite=True
    def uploadfile(self, filepath, overwrite=True):
        if not self.service:
            raise Exception("Call Connect before start using GDrive")
        if not os.path.isfile(filepath):
            raise Exception(f"The local file to upload does not exists: {filepath}")

        logging.info(f"Upload started for {filepath}...")
        media = MediaFileUpload(filepath, mimetype='application/zip', resumable=True)
        request = self.service.files().create(media_body=media, body={'name': os.path.basename(filepath)})
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print("Uploaded %d%%." % int(status.progress() * 100))
            logging.info(f"Upload Complete!")

    # Download the specified file from GDrive to the specified local folder. Returns the local filepath.
    def downloadfile(self, filename, localfolder):
        if not self.service:
            raise Exception("Call Connect before start using GDrive")

    # Return True if already connected
    def isconnected(self):
        if self.service:
            return True
        else:
            return False





