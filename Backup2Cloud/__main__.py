import configparser
import os
import tempfile
from .gdrive import GDrive
import logging

def zipencrypt(folder):
    pass

def unzipdecrypt(folder):
    pass

def cliHelp():
    print("Usage:")
    print("   Backup2Cloud.py [-d ID [Folder]]")
    print("             default: upload the packaged folders to cloud")
    print("      -d ID [Folder]: download and extract specified ID entry of the INI to Folder")
    print("                      (or to current folder if missing)")
    print("                      e.g.: Backup2Cloud.py -d folder1")
    print("")

CMD_UPLOAD = "CMD_UPLOAD"
CMD_DOWNLOAD = "CMD_DOWNLOAD"

def Main():
    logging.info(f"Backup2Cloud - Backup specific folders to and upload to a cloud provider")

    command = None
    if len(sys.argv)==1:
        command = CMD_UPLOAD
    
    download_id = None
    if len(sys.argv)>2:
        if sys.argv[1] == "-d":
            download_id = sys.argv[2]
            folder = None
            if len(sys.argv)>3:
                folder = sys.argv[3]
            command = CMD_DOWNLOAD
            
    if not command:
        cliHelp()
        return

    logging.info(f"Load INI...")
    configfile = "Backup2Cloud.ini"
    logging.info(f"Using config {configfile}")
    config = configparser.ConfigParser()
    config.read(configfile)
    for cloudplace in config.sections():
        with GDrive(cloudplace) as gd:
            with tempfile.TemporaryDirectory() as tempdir:
                logging.info(f"Processing {cloudplace}")
                zipfile = None
                id = None

                for (key, val) in config.items(cloudplace):
                    if key=="credentials":
                        gd.connect(val)
                        continue
                    elif key.startswith("folder"):
                        folder = val
                        id = key
                        zipfile = os.path.join(tempdir, folder)
                        if command == CMD_UPLOAD:
                            zipencrypt(folder=zipfile)
                    elif key.startswith("file"):
                        zipfile = val
                        id = key

                    if not gd.isconnected():
                        raise Exception(f"Credentials are missing from INI for {cloudplace}")
                    
                    if not zipfile:
                        raise Exception(f"Either the folder or file is missing from INI for {cloudplace}")
                    
                    logging.debug(f"command: {command}")

                    if command == CMD_UPLOAD:
                        gd.uploadfile(filepath=zipfile)

                    if command == CMD_DOWNLOAD:
                        logging.debug(f"download_id: {download_id}")
                        logging.debug(f"id: {id}")
                        if download_id == id:
                            gd.downloadfile(os.path.basename(zipfile), tempdir)
                            input(f"Check zip here: {tempdir}")

### set up logging
import logging, sys, socket

machinename = socket.gethostname()
logging.basicConfig(
    level=logging.DEBUG,
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

