import logging

""" Interface of the providers. Use logging to show info or warning and raise errors at errors. """

class ProvidersInterface:
    def __init__(self, name, credentialfile=None):
        """Constructor with custom name and optional credentials"""
        pass

    def connect(self, credentialfile):
        """Lazy call of connect instead of constructor"""
        raise Exception("This is the interface. The interface should not be called directly!")

    def uploadfile(self, filepath, overwrite=True):
        """Upload or copy specified local filepath to the provider space. Delete already existing one if overwrite=True"""
        raise Exception("This is the interface. The interface should not be called directly!")

    def downloadfile(self, filename, localfolder) -> str:
        """Download or copy remote file to specified local folder. The local folder should already exists. Returns local file path"""
        raise Exception("This is the interface. The interface should not be called directly!")

    def getFreespaceBytes(self) -> int:
        """Return the available free space on the provider"""
        raise Exception("This is the interface. The interface should not be called directly!")

    def fileexists(self, filename) -> str:
        """ Check if file exists with exact name on provider. Returns the id of the file if yes."""
        raise Exception("This is the interface. The interface should not be called directly!")

    def close(self):
        """Close any living connections with the provider"""
        raise Exception("This is the interface. The interface should not be called directly!")

    def getName(self) -> str:
        """Get providers name. Returns None if it was not properly initialized"""
        return None

