#setup
virtualenv -p python3 .
scripts\activate.bat
pip install --upgrade setuptools wheel
python -m pip install --user --upgrade twine

#build package and upload
#pip freeze > requirements.txt
scripts\activate.bat; Remove-Item dist/*; python setup.py sdist bdist_wheel; python -m twine upload dist/*

# install on client:
# sudo pip3 install --upgrade Backup2Cloud