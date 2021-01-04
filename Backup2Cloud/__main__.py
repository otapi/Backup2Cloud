import configparser
import os
import tempfile
from .gdrive import GDrive

def zipencrypt(folder):
    pass

def unzipdecrypt(folder):
    pass

def Main():
    logging.info(f"Backup2Cloud")

    logging.info(f"Load INI")
    configfile = "Backup2Cloud.ini"
    logging.info(f"Using config {configfile}")
    config = configparser.ConfigParser()
    config.read(configfile)
    for cloudplace in config.sections():
        with GDrive() as gd:
            with tempfile.TemporaryDirectory() as tempdir:
                logging.info(f"Process {cloudplace}")
                zipfile = None

                for (key, val) in config.items(cloudplace):
                    if key=="credentials":
                        gd.connect(val)
                        continue
                    elif key=="folder":
                        folder = val
                        zipfile = os.path.join(tempdir, folder)
                        zipencrypt(folder=zipfile)
                    elif key=="file":
                        zipfile = val

                    if not gd.isconnected():
                        raise Exception(f"Credentials are missing from INI for {cloudplace}")
                    
                    if not zipfile:
                        raise Exception(f"Either the folder or file is missing from INI for {cloudplace}")
                    gd.uploadfile(filepath=zipfile)

### set up logging
import logging, sys, socket

machinename = socket.gethostname()
logging.basicConfig(
    level=logging.INFO,
    #format=f"%(message)s\t%(asctime)s\t{machinename}\t%(threadName)s\t%(levelname)s",
    format=f"%(message)s",
    handlers=[
        #logging.FileHandler(f"{logfile}.txt"),
        logging.StreamHandler(sys.stdout)
        #TalkerHandler()
    ]
)


# main run
try:
    Main()
except Exception:
    logging.exception("Fatal error")

