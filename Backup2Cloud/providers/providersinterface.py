import logging

""" Interface of the providers. Use logging to show info or warning and raise errors at errors. """

class ProvidersInterface:
    def __init__(self, name, credentialfile=None):
        """Constructor with custom name and optional credentials"""

    def connect(self, credentialfile):
        """Lazy call of connect instead of constructor"""
        pass

    def uploadfile(self, filepath, overwrite):
        """Upload or copy specified local filepath to the provider space. Delete already existing one if overwrite=True"""
        pass

    def downloadfile(self, filename, localfolder) -> str:
        """Download or copy remote file to specified local folder. The local folder should already exists. Returns local file path"""
        pass

    def getFreespaceBytes(self) -> int:
        """Return the available free space on the provider"""

    def close(self):
        """Close any living connections with the provider"""
        pass
