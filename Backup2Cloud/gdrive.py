import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import logging

# Class to upload, download and list files on Google Drive.
class GDrive():
    def __init__(self, name, credentialfile):
        self.name = name
        self.service = None
        self.picklefile=os.path.join(os.path.dirname(credentialfile), f"{self.name}_token.pickle")
        self.connect(credentialfile)

    def connect(self, credentialfile):
        if self.service:
            logging.info(f"Already connected to GDrive. Avoid connecting multiple times by the same GDrive object.")

        logging.info(f"Connect to GDrive using {credentialfile}...")
        creds = None
        if os.path.exists(self.picklefile):
            with open(self.picklefile, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            logging.warning(f"There are no (valid) credentials available, the user should log in.") 
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentialfile, ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive.file'])
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.picklefile, 'wb') as token:
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

        filename = os.path.basename(filepath)
        exists = self.fileexists(filename)
        if overwrite and exists:
            logging.info(f"Already exists on GDrive, deleting: {filename}")
            logging.debug(f"exists: {exists}")
            self.service.files().delete(fileId=exists).execute()

        logging.info(f"Upload started for {filepath}...")
        media = MediaFileUpload(filepath, mimetype='application/x-7z-compressed', resumable=True)
        request = self.service.files().create(media_body=media, body={'name': filename})
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

        if not os.path.isdir(localfolder):
            raise Exception(f"The folder does not exists: {localfolder}")
        
        fileId = self.fileexists(filename)
        if not fileId:
            raise Exception(f"The file was not found on the GDrive: {filename}")
        
        destination = os.path.join(localfolder, filename)
        if os.path.exists(destination):
            raise Exception(f"Local file is already exists: {destination}")
        
        logging.info(f"Download started for {filename}...")
        request = self.service.files().get_media(fileId=fileId)

        with open(destination, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Downloaded %d%%." % int(status.progress() * 100))
        logging.info(f"Download Complete!")
        return destination

    # Return True if already connected
    def isconnected(self):
        if self.service:
            return True
        else:
            return False

    # Return free space on the GDrive
    def getFreespaceBytes(self):
        storageQuota = self.service.about().get(fields="storageQuota").execute()
        logging.debug(f"storageQuota: {storageQuota}")
        return int(storageQuota['storageQuota']['limit'])-int(storageQuota['storageQuota']['usage'])




