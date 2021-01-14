# Backup 2 Cloud
Backup specific folders and upload to a cloud provider. The uploaded files are 7zipped and encrypted locally. Uploads only those packages which were changed since last backup.

Currently only Google Drive is supported, but can handle multiple accounts.

Important: The tool can run only on machine with UI (with JavaScript enabled browser). Google doesn't allow to reach personal Google Drive files without UI: 'User data cannot be accessed from a platform without a UI because it requires user interaction for sign-in.'
## Install and Setup
Requirements: Python 3.7 with pip and setuptools. If not installed, do it on Debian:

`sudo apt install python3-venv python3-pip python3-setuptools`

Install the tool's package via pip:

`python -m pip install Backup2Cloud`

Run first time:

`python -m Backup2Cloud`

### INI file
Open with a texteditor the ini file at your home directory (as shown on the first run above). 
Follow notes in the ini file and setup one or more places to backup.

### .exclude file
If you want to exclude subfolders or files, you can specify them by the same patterns as .gitignore files. Open with a texteditor the .exclude file at your home directory (as shown on the first run above). 
Follow notes in the .exclude file and add folder/file patterns to exclude

### Enable Google Drive API
Enable the OAuth Client ID at Google Drive API via:
https://developers.google.com/drive/api/v3/quickstart/python
(Or you can manage your already exisiting Google APIs here: https://console.developers.google.com/apis/)
In resulting dialog click DOWNLOAD CLIENT CONFIGURATION and save the file credentials.json to your home directory (as shown on the first run above). 

Run the tool second time:
`python -m Backup2Cloud`

Let's follow the url (open it in a browser on the same) to authorize the API for each cloudspace sections: 'Please visit this URL to authorize this application'. Complete the access approval in a browser.

## Usage
Run a backup manually, or add the backup run to scheduler (e.g. cron):

`python -m Backup2Cloud`

Restore all backups manually to current folder:

`python -m Backup2Cloud -d *`

Command line interface:

`Backup2Cloud.py [-d *|ID [destination]]")
                default: upload the packaged folders to cloud")
     -d * [destination]: download and extract all entries of the INI to Folder")
                         (or to current folder if missing)")
    -d ID [destination]: download and extract specified ID entry of the INI to Folder")
                         (or to current folder if missing)")
                         e.g.: Backup2Cloud.py -d folder1")`






