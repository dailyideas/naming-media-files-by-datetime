import datetime, logging, os, sys, time
import argparse, enum, re
from dataclasses import dataclass
from enum import Enum
from logging.handlers import RotatingFileHandler

from PIL import Image


#### #### #### #### #### 
####  Global constants #### 
#### #### #### #### ####
## Script setup
SCRIPT_NAME = os.path.basename(__file__).split(".")[0]
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__) )
ROOT_DIRECTORY = SCRIPT_DIRECTORY
LOG_DIRECTORY = os.path.join(ROOT_DIRECTORY, "log/", SCRIPT_NAME)
LOG_LEVEL = logging.INFO
## Application
IMAGE_FILE_EXTENSIONS = ["JPEG", "jpeg", "JPG", "jpg", "PNG", "png"]
VIDEO_FILE_EXTENSIONS = ["MP4", "mp4", "MOV", "mov", "WMV", "wmv"]
""" Naming of media file after it was edited
    1. Apple Inc. devices: append \"(Edited)\" to the file name
"""
EDITED_FILE_NAME_KEYS_LOWER_CASE = ["edit"]
""" Recognized editing softwares
    1. Windows Photo Editor
    2. Photoshop
    3. Lightroom
"""
EDITING_SOFTWARE_KEYS_LOWER_CASE = ["editor", "lightroom", "photoshop"]

#### #### #### #### #### 
#### Global variables #### 
#### #### #### #### #### 
#### Logging
log = logging.getLogger()


#### #### #### #### #### 
#### Global Setups #### 
#### #### #### #### #### 
#### Paths
os.makedirs(LOG_DIRECTORY, exist_ok=True)
#### Logging
formatter = logging.Formatter(
    "%(asctime)s-%(name)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S")
logHandler_console = logging.StreamHandler()
logHandler_console.setFormatter(formatter)
log.addHandler(logHandler_console)
logPath = os.path.join(LOG_DIRECTORY, SCRIPT_NAME + ".log")
logHandler_file = RotatingFileHandler(logPath, mode='a', maxBytes=2e6, 
    backupCount=10, encoding="utf-8")
logHandler_file.setFormatter(formatter)
log.addHandler(logHandler_file)
log.setLevel(LOG_LEVEL)
loggers = [logging.getLogger(name) for name in 
    logging.root.manager.loggerDict]
for logger in loggers:
    logger.setLevel(LOG_LEVEL)
#### MediaInfo object
MI_TriedLoading = False
MI = None


#### #### #### #### #### 
#### Prologue #### 
#### #### #### #### #### 
log.debug("Python version: %s", sys.version.split(" ")[0] )


#### #### #### #### #### 
#### Classes #### 
#### #### #### #### #### 
class DatetimeType(Enum):
    """ Difference between date taken, modified & created
    
        Reference
        ---- ----
        1. https://help.mycloud.ch/hc/en-us/articles/360003134159-What-is-the-difference-between-the-date-a-photo-video-was-taken-created-and-modified-
    """
    UNKNOWN = enum.auto()
    TAKEN = enum.auto() ## The time the photo / video is recorded
    EDITED = enum.auto() ## The time you edited the file by photo-editing software
    MODIFIED = enum.auto() ## The time you edited the file, including modification to the file's metadata. This information is set by the OS 
    CREATED = enum.auto() ## The time the file was saved or archived and is set by the OS (for example when moving, copying, or downloading the file)
    HARDCODED = enum.auto()


class ModificationType(Enum):
    UNKNOWN = enum.auto()
    ORIGINAL = enum.auto()
    EDITED = enum.auto()


@dataclass
class MediaFileInfo:
    Width:int
    Height:int
    DatetimeInfo:datetime.datetime
    DatetimeInfoType:DatetimeType
    EditingSoftware:str = ""


#### #### #### #### #### 
#### Functions #### 
#### #### #### #### #### 
def AbortProgram():
    log.error("Aborting program")
    sys.exit(1)


def GetInfoFromImage(filePath:str) -> MediaFileInfo:
    ## Pre-condition
    assert os.path.isfile(filePath)
    assert filePath.split(".")[-1] in IMAGE_FILE_EXTENSIONS
    ## Variables initialization
    with Image.open(filePath) as image:
        imageWidth, imageHeight = image.size
        """ Exif tags info. Extract exif data by Python
        
            Reference 
            ---- ----
            1. https://www.exiv2.org/tags.html
            2. https://stackoverflow.com/Questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image
        """
        exifData = image._getexif()
        if exifData is None:
            exifData = {} ## Ensure that the codes below can obtain the variable with correct data type
        exifData_36867 = exifData.get(36867, None) ## DateTimeOriginal: The date and time when the original image data was generated
        exifData_36868 = exifData.get(36868, None) ## DateTimeDigitized: The date and time when the image was stored as digital data
        exifData_306 = exifData.get(306, None) ## DateTime: The date and time the file was changed
        exifData_11 = exifData.get(11, None) ## ProcessingSoftware: The name and version of the software used to post-process the picture
        exifData_305 = exifData.get(305, None) ## Software: The name and version of the software or firmware of the camera or image input device used to generate the image
    fileStat = os.stat(filePath)
    fileMTime = datetime.datetime.fromtimestamp(fileStat.st_mtime)
    fileCTime = datetime.datetime.fromtimestamp(fileStat.st_ctime)
    ## Pre-processing
    exifData_36867 = datetime.datetime.strptime(exifData_36867, 
        "%Y:%m:%d %H:%M:%S") if isinstance(exifData_36867, str) else None
    exifData_36868 = datetime.datetime.strptime(exifData_36868, 
        "%Y:%m:%d %H:%M:%S") if isinstance(exifData_36868, str) else None
    exifData_306 = datetime.datetime.strptime(exifData_306, 
        "%Y:%m:%d %H:%M:%S") if isinstance(exifData_306, str) else None
    ## Get DatetimeInfo & DatetimeInfoType
    datetimeInfoType = DatetimeType.TAKEN
    datetimeInfo = exifData_36867
    if datetimeInfo is None: 
        datetimeInfoType = DatetimeType.TAKEN
        datetimeInfo = exifData_36868 
    if datetimeInfo is None:
        datetimeInfoType = DatetimeType.EDITED
        datetimeInfo = exifData_306
    if datetimeInfo is None:
        datetimeInfoType = DatetimeType.MODIFIED
        datetimeInfo = fileMTime
    if datetimeInfo is None or (
        isinstance(fileCTime, datetime.datetime) and \
        fileCTime < datetimeInfo):
        datetimeInfoType = DatetimeType.CREATED
        datetimeInfo = fileCTime
    if datetimeInfo is None:
        datetimeInfoType = DatetimeType.UNKNOWN
    ## Get EditingSoftware
    editingSoftware = exifData_11
    if editingSoftware is None:
        editingSoftware = exifData_305
    if editingSoftware is None:
        editingSoftware = ""
    ## Return
    return MediaFileInfo(
        Width=imageWidth,
        Height=imageHeight,
        DatetimeInfo=datetimeInfo,
        DatetimeInfoType=datetimeInfoType,
        EditingSoftware=editingSoftware
    )


def GetInfoFromVideo(filePath:str) -> MediaFileInfo:
    ## Inner functions
    def GetDatetimeFromMediaInfoFormatStr(datetimeStr:str):
        ## Pre-condition
        if not isinstance(datetimeStr, str):
            return None
        ## Main
        """ Example: UTC 2021-03-23 14:32:37
        
            1. Remove leading time zone info
            2. Convert to datetime object 
        """
        try:
            datetimeStr = re.sub(r"^[a-zA-Z ]*", '', datetimeStr) ## Remove leading time zone info
            datetimeInfo = datetime.datetime.strptime(
                datetimeStr, "%Y-%m-%d %H:%M:%S") ## Convert to datetime object 
        except:
            datetimeInfo = None
        return datetimeInfo
    
    ## Pre-condition
    global MI_TriedLoading, MI
    assert os.path.isfile(filePath)
    assert filePath.split(".")[-1] in VIDEO_FILE_EXTENSIONS
    ## Pre-processing & Pre-condition
    try:
        from lib.MediaInfo.MediaInfoDLL3 import MediaInfo, Stream
    except ModuleNotFoundError:
        log.exception(f"Cannot find the required module")
    if MI_TriedLoading is False and MI is None:
        try:
            MI = MediaInfo()
        except FileNotFoundError:
            log.exception(f"Cannot find the file required")
        finally:
            MI_TriedLoading = True
    if not isinstance(MI, MediaInfo):
        return None
    ## Variables initialization
    """ MediaInfo usage
    
        Reference
        ---- ----
        1. https://stackoverflow.com/questions/27850629/python-hachoir-metadata-reading-fps-tag-from-mp4-file
    """
    MI.Open(filePath)
    width = MI.Get(Stream.Video, 0, "Width")
    height = MI.Get(Stream.Video, 0, "Height")
    datetimeInfo_recorded = MI.Get(Stream.General, 0, 
        "Recorded_Date") ##
    datetimeInfo_digitalized = MI.Get(Stream.General, 0, 
        "Digitized_Date") ##
    datetimeInfo_encoded = MI.Get(Stream.General, 0, 
        "Encoded_Date") ## 
    MI.Close()
    fileStat = os.stat(filePath)
    fileMTime = datetime.datetime.fromtimestamp(fileStat.st_mtime)
    fileCTime = datetime.datetime.fromtimestamp(fileStat.st_ctime)
    ## Pre-processing
    datetimeInfo_recorded = GetDatetimeFromMediaInfoFormatStr(
        datetimeInfo_recorded)
    datetimeInfo_digitalized = GetDatetimeFromMediaInfoFormatStr(
        datetimeInfo_digitalized)
    datetimeInfo_encoded = GetDatetimeFromMediaInfoFormatStr(
        datetimeInfo_encoded)
    ## Main
    datetimeInfoType = DatetimeType.TAKEN
    datetimeInfo = datetimeInfo_recorded
    if datetimeInfo is None:
        datetimeInfoType = DatetimeType.TAKEN
        datetimeInfo = datetimeInfo_digitalized
    if datetimeInfo is None:
        datetimeInfoType = DatetimeType.EDITED
        datetimeInfo = datetimeInfo_encoded
    if datetimeInfo is None:
        datetimeInfoType = DatetimeType.MODIFIED
        datetimeInfo = fileMTime
    if datetimeInfo is None or (
        isinstance(fileCTime, datetime.datetime) and \
        fileCTime < datetimeInfo):
        datetimeInfoType = DatetimeType.CREATED
        datetimeInfo = fileCTime
    if datetimeInfo is None:
        datetimeInfoType = DatetimeType.UNKNOWN    
    return MediaFileInfo(
        Width=width,
        Height=height,
        DatetimeInfo=datetimeInfo,
        DatetimeInfoType=datetimeInfoType
    )
    
    
def GetFileModificationType(file_baseName:str, 
        mediaFileInfo:MediaFileInfo=None
    ) -> ModificationType:
    file_baseName_lowerCase = file_baseName.lower()
    if any( (c in file_baseName_lowerCase) for c in \
        EDITED_FILE_NAME_KEYS_LOWER_CASE):
        return ModificationType.EDITED
    file_editingSoftware_lowerCase = mediaFileInfo.EditingSoftware.lower()
    if any( (c in file_editingSoftware_lowerCase) for c in \
        EDITING_SOFTWARE_KEYS_LOWER_CASE):
        return ModificationType.EDITED
    return ModificationType.ORIGINAL


def GetNewFilePath(filePath:str, 
        alternativeDatetime:datetime.datetime=None
    ) -> str:
    ## Variables initialization & Pre-condition
    fileDirectory = os.path.dirname(filePath)
    fileName = os.path.basename(filePath)
    fileName_splitted = fileName.split(".")
    if len(fileName_splitted) == 1: ## Cannot obtain file extension
        return filePath
    if len(fileName_splitted) > 2: ## Recovers the files base name which contains "." 
        fileName_splitted = [
            ".".join(fileName_splitted[:-1] ),
            fileName_splitted[-1]
        ]
    file_baseName = fileName_splitted[0]
    file_extension = fileName_splitted[1]
    if file_extension in IMAGE_FILE_EXTENSIONS:
        mediaFileInfo = GetInfoFromImage(filePath=filePath)
    elif file_extension in VIDEO_FILE_EXTENSIONS:
        mediaFileInfo = GetInfoFromVideo(filePath=filePath)
    else:
        return filePath
    ## Pre-condition
    if mediaFileInfo is None:
        return filePath
    ## Pre-processing
    if isinstance(alternativeDatetime, datetime.datetime):
        useAlternative = \
            (mediaFileInfo.DatetimeInfoType == DatetimeType.UNKNOWN) or \
            (mediaFileInfo.DatetimeInfoType != DatetimeType.TAKEN and \
            alternativeDatetime.date() < mediaFileInfo.DatetimeInfo.date() )
        if useAlternative:
            mediaFileInfo.DatetimeInfoType = DatetimeType.HARDCODED
            mediaFileInfo.DatetimeInfo = alternativeDatetime
    ## Main
    if not isinstance(mediaFileInfo.DatetimeInfo, datetime.datetime):
        log.warning(f"Cannot obtain datetime info from file \"{fileName}\"")
        datetimeInfo_formattedStr = "00000000_000000"
        datetimeInfoType_formattedStr = \
            datetimeTypeToStringMap[DatetimeType.UNKNOWN]
        modificationType = ModificationType.UNKNOWN
        modificationType_formattedStr = \
            modificationTypeToStringMap[modificationType]
    else:
        datetimeInfo_formattedStr = mediaFileInfo.DatetimeInfo.strftime(
            "%Y%m%d_%H%M%S")
        datetimeInfoType_formattedStr = \
            datetimeTypeToStringMap[mediaFileInfo.DatetimeInfoType]
        modificationType = GetFileModificationType(
            file_baseName=file_baseName, mediaFileInfo=mediaFileInfo)
        modificationType_formattedStr = \
            modificationTypeToStringMap[modificationType]

    newFilePath = filePath
    sequenceNum = -1
    fileNameDuplicated = True
    while fileNameDuplicated is True:
        ## Pre-condition
        if sequenceNum >= 999:
            log.error("Sequence number exceeds limit")
            AbortProgram()
        ## Main
        sequenceNum += 1
        sequenceNum_formattedStr = str(sequenceNum).zfill(3)
        newFileName = (
            f"{datetimeInfo_formattedStr}_"
            f"{datetimeInfoType_formattedStr}_"
            f"{modificationType_formattedStr}_"
            f"{sequenceNum_formattedStr}.{file_extension}")
        if newFileName == fileName:
            newFilePath = filePath
            break
        newFilePath = os.path.join(fileDirectory, newFileName)
        fileNameDuplicated = os.path.isfile(newFilePath)
    return newFilePath


#### #### #### #### #### 
#### Main #### 
#### #### #### #### #### 
## Prologue
log.info("Starting program")

## Pre-processing
#### Reads settings from CLI argument
parser = argparse.ArgumentParser(
    description="Media files auto-naming settings", 
    allow_abbrev=False)
parser.add_argument("--dir",
    type=str,
    required=True,
    help="Directory of the media files for auto-naming")
""" Parse datetime.date

    Reference
    ---- ----
    1. https://stackoverflow.com/a/21437360
"""
parser.add_argument("--date",
    type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
    default=None,
    help="If datetime info is not found in the file, set the file's date as the provided value")
parser.add_argument("-r",
    action="store_true",
    help="Search media files in directories recursively")

## Variables initialization
args = parser.parse_args()
mediaFilesDirectory = args.dir
""" Convert datetime.date to datetime.datetime

    Reference
    ---- ----
    1. https://stackoverflow.com/a/1937636
"""
if isinstance(args.date, datetime.date):
    alternativeDatetime = datetime.datetime.combine(
        args.date, datetime.datetime.min.time() )
else:
    alternativeDatetime = None
datetimeTypeToStringMap = {
    DatetimeType.UNKNOWN: "X",
    DatetimeType.TAKEN: "T",
    DatetimeType.EDITED: "E",
    DatetimeType.MODIFIED: "M",
    DatetimeType.CREATED: "C",
    DatetimeType.HARDCODED: "H"
}
modificationTypeToStringMap = {
    ModificationType.UNKNOWN: "Xxxx",
    ModificationType.ORIGINAL: "Orig",
    ModificationType.EDITED: "Edit"
}

## Pre-condition
assert os.path.isdir(mediaFilesDirectory), \
    f"Provided directory \"{mediaFilesDirectory}\" does not exist"

## Main
if args.r: 
    ## Search media files in directories recursively
    """ Recursively traverse directories

        Reference
        ---- ----
        1. https://stackoverflow.com/questions/16953842/using-os-walk-to-recursively-traverse-directories-in-python
    """
    pathToFileList = []
    for root, dirs, files in os.walk(mediaFilesDirectory):
        pathToFileList.extend( [os.path.join(root, f) for f in files] )
else:
    ## Non-recursive search
    pathToFileList = [os.path.join(mediaFilesDirectory, f) for f in \
        os.listdir(mediaFilesDirectory) ]
    pathToFileList = [p for p in pathToFileList if os.path.isfile(p) ]

lastDirectory = None
for filePath in pathToFileList:
    ## Prologue
    currentDirectory = os.path.dirname(filePath)
    if currentDirectory != lastDirectory:
        log.info(f"Processing files at directory \"{currentDirectory}\"")
        lastDirectory = currentDirectory
    ## Main
    fileName = os.path.basename(filePath)
    newFilePath = GetNewFilePath(filePath=filePath, 
        alternativeDatetime=alternativeDatetime)
    if newFilePath == filePath:
        ## If new file naming is the same as the original one, do not rename
        log.info(f"{fileName} is not changed")
        continue
    os.rename(filePath, newFilePath)
    ## Epilogue
    newFileName = os.path.basename(newFilePath)
    log.info(f"{fileName} -> {newFileName}")

## Epilogue
log.info("Exiting program")
