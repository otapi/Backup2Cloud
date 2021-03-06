import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Backup2Cloud",
    version="1.0.17",
    author="otapi",
    description="Backup specific folders to and upload to a cloud provider",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/otapi/Backup2Cloud",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'py7zr',
        'dirtools2'
       
    ],
    python_requires='>=3.7.3',
    package_data={
        # If any package contains *.txt files, include them:
        "": ["*.ini"],
    }
) 