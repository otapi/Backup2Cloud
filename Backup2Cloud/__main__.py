import configparser
import os
import tempfile
from .gdrive import GDrive
import logging
import py7zr
import hashlib

def confiscateName(id, file):
    name = id+os.path.basename(file)
    return hashlib.md5(bytes(name, 'utf-8')).hexdigest()

def cliHelp():
    print("Usage:")
    print("   Backup2Cloud.py [-d *|ID [destination]]")
    print("             default: upload the packaged folders to cloud")
    print("       -d * [destination]: download and extract all entries of the INI to Folder")
    print("                      (or to current folder if missing)")
    print("      -d ID [destination]: download and extract specified ID entry of the INI to Folder")
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
    destination = os.getcwd()
    if len(sys.argv)>2:
        if sys.argv[1] == "-d":
            command = CMD_DOWNLOAD
            download_id = sys.argv[2]
            if len(sys.argv)>3:
                destination = sys.argv[3]
            if not os.path.isdir(destination):
                os.makedirs(destination)
            
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
                packagePassword = None
                folderval = None

                for (key, val) in config.items(cloudplace):
                    if key=="credentials":
                        gd.connect(val)
                        continue
                    elif key=="packagepassword":
                        packagePassword = val
                        continue
                    elif key.startswith("folder"):
                        folder = val
                        folderval = val
                        id = key
                        logging.info(f"Using {folder}={id}")
                        zipfile = os.path.join(tempdir, confiscateName(id, folder))+".7z"
                        if command == CMD_UPLOAD:
                            logging.info(f"Compressing to {zipfile}...")
                            with py7zr.SevenZipFile(zipfile, 'w', password=packagePassword) as archive:
                                archive.set_encrypted_header(True)
                                archive.writeall(folder, os.path.basename(folder))
                            logging.info(f"Compress done!")
                    elif key.startswith("file"):
                        zipfile = val
                        folderval = val
                        id = key

                    logging.debug(f"command: {command}")
                    logging.debug(f"key: {key}")
                    logging.debug(f"val: {val}")

                    if not gd.isconnected():
                        raise Exception(f"Credentials are missing from INI for {cloudplace}")
                    
                    if not zipfile:
                        raise Exception(f"Either the folder or file is missing from INI for {cloudplace}")

                    if command == CMD_UPLOAD:
                        size = "%.1f" % (os.path.getsize(zipfile)/(1024*1024))
                        logging.info(f"The package takes {size} MBytes of {id}={folderval}")
                        gd.uploadfile(filepath=zipfile)

                    if command == CMD_DOWNLOAD:
                        logging.debug(f"download_id: {download_id}")
                        logging.debug(f"id: {id}")
                        if download_id == "*" or download_id == id:
                            localzip = gd.downloadfile(os.path.basename(zipfile), tempdir)
                            destinationCurr = os.path.join(destination, id)
                            if id == "folder" or id == "file":
                                destinationCurr = destination

                            logging.info(f"Extracting to {destinationCurr}...")
                            with py7zr.SevenZipFile(localzip, mode='r', password=packagePassword) as archive:
                                archive.extractall(destinationCurr)
                            logging.info(f"Extract done!")
            freespace = "%.1f" % (gd.getFreespaceBytes()/(1024*1024))
            logging.info(f"Free space on {cloudplace}: {freespace} GBytes")


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

