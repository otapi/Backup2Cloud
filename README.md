# Backup 2 Cloud
Backup specific folders and upload to a cloud provider. The uploaded files are 7zipped and encrypted locally. Uploads only those packages which were changed since last backup.

Currently only Google Drive is supported, but can handle more accounts.
## Install and Setup
Install the package via pip:

`python -m pip install Backup2Cloud`

Run first time:

`python -m Backup2Cloud`

Enable the Google Drive API via:
https://developers.google.com/drive/api/v3/quickstart/python
(Or you can manage your already exisiting Google APIs here: https://console.developers.google.com/apis/)
In resulting dialog click DOWNLOAD CLIENT CONFIGURATION and save the file credentials.json to your home directory (as shown on the first run above). 

Open with a texteditor the ini file at your home directory (as shown on the first run above). 
Follow notes in the ini file and setup one or more places to backup.

Run the tool second time:
`python -m Backup2Cloud`

Let's follow the url (or open on a separated device) to authorize the API for each cloudspace sections: 'Please visit this URL to authorize this application'. Complete the authorizes in a browser, even on other machine.

## Usage
`Backup2Cloud.py [-d *|ID [destination]]")`

`                default: upload the packaged folders to cloud")`

`     -d * [destination]: download and extract all entries of the INI to Folder")`

`                         (or to current folder if missing)")`

`    -d ID [destination]: download and extract specified ID entry of the INI to Folder")`

`                         (or to current folder if missing)")`

`                         e.g.: Backup2Cloud.py -d folder1")`


Run a backup manually:

`python -m Backup2Cloud`

Or add the backup run to scheduler (e.g. cron)

Restore all backups manually to current folder:

`python -m Backup2Cloud -d *`



