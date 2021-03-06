rem create new folder and copy the built package from the dist folder first!
virtualenv -p python3 .
scripts\activate.bat
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib py7zr dirtools

rem #install
rem pip install -r requirements.txt

rem update the version number accordingly

rem pip install --upgrade Backup2Cloud
python -m Backup2Cloud
python -m Backup2Cloud -log debug

rem crontab -e
rem 00 00 16 * * /usr/bin/python3 -m Backup2Cloud > /mnt/HDD/Backup2Cloud/run.log
rem check /var/log/syslog