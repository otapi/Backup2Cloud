import configparser
import os
import tempfile

def zipencrypt(folder, zip):
    pass

def unzipdecrypt(zip, folder):
    pass

def downloadfile(cloudinfo, file):
    pass

def uploadfile(cloudinfo, file):
    pass

def Main():
    print("Backup2Cloud")

    print("Load INI")
    configfile = os.path.dirname(os.path.abspath(__file__))+"/Backup2Cloud.ini"
    logging.info(f"Using config {configfile}")
    config = configparser.ConfigParser()
    config.read(configfile)
    with tempfile.TemporaryDirectory() as tempdir:
        for cloudplace in config.sections():
            print(f"Process f{cloudplace}")
            token = None
            url = None
            folder = None

            for (key, val) in config.items(cloudplace):
                if key=="token":
                    token = val
                elif key=="url":
                    url = val
                else:
                    folder = val
                    zipfile = os.path.join(tempdir, folder, ".zip")
                    # process

            

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

