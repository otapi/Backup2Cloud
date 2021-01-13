rem create new folder and copy the built package from the dist folder first!
virtualenv -p python3 .
scripts\activate.bat
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib py7zr dirtools

rem #install
rem pip install -r requirements.txt

rem update the version number accordingly

rem pip install Backup2Cloud-0.0.1.tar.gz
python -m Backup2Cloud

