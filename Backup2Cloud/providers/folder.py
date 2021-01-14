import os
import logging
from .providersinterface import ProvidersInterface
import shutil

""" Interface of the providers. Use logging to show info or warning and raise errors at errors. """

class Folder(ProvidersInterface):
    def __init__(self, name, credentialfile=None):
        """Constructor with custom name and optional credentials"""
        self.name = name

    def connect(self, credentialfile):
        """Lazy call of connect instead of constructor"""
        self.target = credentialfile
        if not os.path.isdir(self.target):
            os.makedirs(self.target)

    def uploadfile(self, filepath, overwrite=True):
        """Upload or copy specified local filepath to the provider space. Delete already existing one if overwrite=True"""
        if not self.target:
            raise Exception("Call Connect before start using Folder")
        
        if not os.path.isfile(filepath):
            raise Exception(f"The local file to upload does not exists: {filepath}")

        targetfile = os.path.join(self.target, os.path.basename(filepath))

        if overwrite and os.path.isfile(targetfile):
            logging.info(f"Already exists on Target, deleting: {targetfile}")
            os.remove(targetfile)

        logging.info(f"Copy started for {filepath}...")
        shutil.copyfile(filepath, targetfile)
        logging.info(f"File copied!")
        
    def downloadfile(self, filename, localfolder):
        """Download or copy remote file to specified local folder"""
        if not self.target:
            raise Exception("Call Connect before start using Folder")

        if not os.path.isdir(localfolder):
            raise Exception(f"The folder does not exists: {localfolder}")
        
        targetfile = os.path.join(self.target, filename)
        
        if not os.path.isfile(targetfile):
            raise Exception(f"The file was not found on the Target: {targetfile}")
        
        destination = os.path.join(localfolder, filename)
        if os.path.exists(destination):
            raise Exception(f"Local file is already exists: {destination}")
        
        logging.info(f"Copy started for {filename}...")
        shutil.copyfile(targetfile, destination)
        logging.info(f"File copied!")
        return destination
        
    def getFreespaceBytes(self) -> int:
        """Return the available free space on the provider"""
        usage = shutil.disk_usage(self.target)
        return usage[2]

    def fileexists(self, filename):
        """ Check if file exists with exact name on provider. Returns the full path of the file if yes."""
        targetfile = os.path.join(self.target, filename)
        if os.path.isfile(targetfile):
            return targetfile
        else:
            return None

    def getName(self) -> str:
        """Get providers name. Returns None if it was not properly initialized"""
        return self.name



