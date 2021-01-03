# Backup 2 Cloud
Backup specific folders to and upload to a cloud provider

## Install
`python -m pip install Backup2Cloud`

Enable the Drive API via:
https://developers.google.com/drive/api/v3/quickstart/python
In resulting dialog click DOWNLOAD CLIENT CONFIGURATION and save the file credentials.json to your working directory. 

Or you can manage your already exisiting Google APIs here: https://console.developers.google.com/apis/

At first run, let's follow the url (or open on a separated device) to authorize the API: 'Please visit this URL to authorize this application'


## Usage
Set up INI file

Run a backup:
`python -m Backup2Cloud`
Or add the backup run to scheduler (e.g. cron)
