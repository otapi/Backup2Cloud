#setup
virtualenv -p python3 .
scripts\activate.bat
pip install --upgrade setuptools wheel

#build package
#pip freeze > requirements.txt
python setup.py sdist bdist_wheel

#upload package
python -m pip install --user --upgrade twine
python -m twine upload dist/*