import configparser
import os
import tempfile
from . import providers
import logging
import py7zr
import hashlib
from pathlib import Path
import shutil 
from dirtools2.dirtools2 import Dir
import argparse
import logging, sys

def formatSize(bytes):
    logging.debug(f"bytes: {bytes}")
    bytes = float(bytes)
    kb = bytes / 1024
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2fG" % (G)
        else:
            return "%.2fM" % (M)
    else:
        return "%.2fkb" % (kb)
        
def confiscateName(id, file):
    name = id+os.path.basename(file)
    return hashlib.md5(bytes(name, 'utf-8')).hexdigest()

def getChecksumBigfile(file):
    with open(file, "rb") as f:
        file_hash = hashlib.md5()
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            file_hash.update(chunk)
    return file_hash.hexdigest()

CMD_UPLOAD = "Upload"
CMD_DOWNLOAD = "Download"

def Main():
    print(f"Backup2Cloud - Backup specific folders to and upload to a cloud provider")

    parser = argparse.ArgumentParser()
    parser.add_argument('destination', nargs='?', default=os.getcwd(),
                        help='Optional destination folder at Download mode. Example: C:\output, default=current folder')
    parser.add_argument( '-d',
                        '--download',
                        help='Download and extract all (*) or only the specified ID entry of the INI to Destination folder. Example: -d folder1' )
    parser.add_argument( '-log',
                        '--loglevel',
                        default='info',
                        help='Provide logging level. Example --loglevel debug, default=info' )
    args = parser.parse_args()

    logging.basicConfig(
        level=args.loglevel.upper(),
        format=f"[%(levelname)s]\t%(message)s",
        handlers=[
            #logging.FileHandler(f"{logfile}.txt"),
            logging.StreamHandler(sys.stdout)
            #TalkerHandler()
        ]
    )

    if not args.loglevel.upper()=="INFO":
        logging.info(f'Logging level changed to: {args.loglevel.upper()}')

    command = None
    download_id = None
    destination = args.destination

    if args.download:
        command = CMD_DOWNLOAD
        download_id = args.download
        if not os.path.isdir(destination):
            os.makedirs(destination)
    else:
        command = CMD_UPLOAD

    logging.info(f"Mode: {command}")
    verdict = ""
    logging.info(f"Load INI...")
    homefolder = os.path.join(str(Path.home()), ".Backup2Cloud")
    if not os.path.isdir(homefolder):
        os.makedirs(homefolder)
        
    configfile = os.path.join(homefolder, "Backup2Cloud.ini")
    ignorefile = os.path.join(homefolder, ".exclude")
    logging.info(f"Using config {configfile}")
    if not os.path.isfile(configfile):
        scriptfolder = os.path.dirname(os.path.abspath(__file__))
        shutil.copyfile(os.path.join(scriptfolder,"Backup2Cloud.ini"), configfile)
        shutil.copyfile(os.path.join(scriptfolder,".exclude"), configfile)
        logging.error(f"Edit {configfile} first! You can also edit the exclude file here {ignorefile}")
        return
    
    if not os.path.isfile(ignorefile):
        ignorefile = None

    config = configparser.ConfigParser()
    config.read(configfile)
    tempdirname = None
    if config.has_option('Options', 'tempdir'):
        tempdirname=config['Options']['tempdir']
        logging.debug(f"Using custom temporary folder: {tempdirname}")
        if not os.path.isdir(tempdirname):
            os.makedirs(tempdirname)

    logging.info(f"Checking for cloudplace credentials")
    for cloudplace in config.sections():
        for (key, val) in config.items(cloudplace):
            if key=="type":
                if val=="GDrive":
                    provider = providers.GDrive(cloudplace, os.path.join(homefolder, "credentials.json"))
                    freespace = formatSize(provider.getFreespaceBytes())
                    logging.info(f"Free space on {cloudplace}: {freespace}")

    for cloudplace in config.sections():
        if cloudplace=="Options":
            continue
        
        verdict = "Verdict\nCPlace\tState\tID\tConfiscated name\tLocal place\tPackage size\n"
        logging.info(f"Processing {cloudplace}")
        packagePassword = None
        provider = providers.ProvidersInterface(None)
        sumsize = 0

        with tempfile.TemporaryDirectory(dir=tempdirname) as tempdir:
            for (key, val) in config.items(cloudplace):
                if key=="type":
                    if val=="GDrive":
                        provider = providers.GDrive(cloudplace, os.path.join(homefolder, "credentials.json"))
                    elif val=="Folder":
                        provider = providers.Folder(cloudplace)
                    continue

                elif key=="target":
                    provider.connect(val)
                    continue

                elif key=="packagepassword":
                    packagePassword = val
                    continue
                
                # Folders or files
                elif key.startswith("folder") or key.startswith("file"):
                    if not provider.getName():
                        raise Exception(f"Type is missing from INI for {cloudplace}")

                    isfolder = key.startswith("folder")
                    logging.info(f"Using {key}={val}")
                    zipfile = os.path.join(tempdir, confiscateName(key, val))+".7z"

                    if command == CMD_UPLOAD:
                        checksum = None
                        if isfolder:
                            d = Dir(val)
                            checksum = d.hash()
                        else: 
                            checksum = getChecksumBigfile(val)
                        logging.debug(f"checksum: {checksum}")

                        checksumfilename = os.path.join(homefolder, f"{cloudplace}_{os.path.basename(zipfile)}").replace(".7z", ".checksum")

                        logging.debug(f"checksumfilename: {checksumfilename}")
                        if provider.fileexists(os.path.basename(zipfile)) and os.path.isfile(checksumfilename):
                            with open(checksumfilename, 'r') as f:
                                oldchecksum=f.read()

                            logging.debug(f"oldchecksum: {oldchecksum}")
                            
                            if checksum == oldchecksum:
                                logging.info(f"No changes in the package, upload skipped for: {cloudplace}|{val}")
                                verdict += f"{cloudplace}\tNo change\t{key}\t{os.path.basename(zipfile)}\t{val}\tskipped\n"
                                continue
                        
                        size = 0
                        if isfolder:
                            if not packagePassword:
                                raise Exception(f"Packagepassword is missing from INI for {cloudplace}")

                            logging.info(f"Compressing to {zipfile}...")

                            d = Dir(val, exclude_file=ignorefile)
                            with py7zr.SevenZipFile(zipfile, 'w', password=packagePassword) as archive:
                                archive.set_encrypted_header(True)
                                for foldername, subfolders, filenames in d.walk():
                                    for filename in filenames:
                                        logging.debug(f"  adding {filename}")
                                        archive.write(os.path.join(foldername, filename), arcname=os.path.join(os.path.relpath(foldername, os.path.dirname(val)), filename))
                            logging.info(f"Compress done!")
                        else:
                            zipfile = val

                        size = formatSize(os.path.getsize(zipfile))
                        sumsize += os.path.getsize(zipfile)
                        
                        logging.info(f"The package takes {size}")
                        logging.info(f"Uploading package for: {cloudplace}|{key}={val}")
                        provider.uploadfile(filepath=zipfile)
                        
                        with open(checksumfilename, 'w') as f:
                            f.write(checksum)
                        verdict += f"{cloudplace}\tUploaded\t{key}\t{os.path.basename(zipfile)}\t{val}\t{size}\n"
                    
                    elif command == CMD_DOWNLOAD:
                        logging.debug(f"download_id: {download_id}")
                        logging.debug(f"val: {val}")
                        if download_id == "*" or download_id == val:
                            localzip = provider.downloadfile(os.path.basename(zipfile), tempdir)
                            
                            size = formatSize(os.path.getsize(localzip))
                            verdict += f"{cloudplace}\tDownloaded\t{key}\t{os.path.basename(zipfile)}\t{val}\t{size}\n"

                            logging.debug(f"destination: {destination}")
                            if isfolder:
                                destinationCurr = destination
                                logging.info(f"Extracting to {destinationCurr}...")
                                with py7zr.SevenZipFile(localzip, mode='r', password=packagePassword) as archive:
                                    archive.extractall(destinationCurr)
                                logging.info(f"Extract done!")
                            else:
                                destinationCurr = os.path.join(destination, os.path.basename(val))
                                logging.info(f"Copy to {destinationCurr}")
                                shutil.copyfile(localzip, destinationCurr)
                                logging.info(f"File copied!")

        freespace = formatSize(provider.getFreespaceBytes())
        logging.info(f"Free space on {cloudplace}: {freespace}")
        verdict += f"{cloudplace}\tAll packages on {cloudplace} take {formatSize(sumsize)} of {freespace}\t\t\t\t\n"
        provider.close()
    
    logging.info(f"--------")
    logging.warning(verdict)

Main()

