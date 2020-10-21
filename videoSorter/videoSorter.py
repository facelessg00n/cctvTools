import os
import shutil
import logging
import pathlib

# Sorts IP camera file with the following naming convention
# IP Camera*_NVR_Name_NVR_Name_2020082700000_000_000
# Sorts into NVR> Camera > Date > Hour folders and writes a log.

# ---Config----
debugMessages = False

# ---inputs----
fileType1 = ".jpg"
fileType2 = ".mp4"

originPath = os.getcwd()
print(originPath)
targetPath = os.getcwd() + "/out"
print(targetPath)

# ---Config the logger-----
logging.basicConfig(
    filename="log.txt",
    format="%(levelname)s:%(asctime)s:%(message)s",
    level=logging.DEBUG,
)

files = [
    f
    for f in os.listdir(originPath)
    if (f.endswith(fileType1) or f.endswith(fileType2))
]


def idFiles(fileName):
    global fileType1
    if fileName.endswith(fileType1):
        print("This is a JPG: " + fileName)
    elif fileName.endswith(fileType2):
        print("This is an MP4: " + fileName)


# create a folder and then move files into it
def createFolder(fileName):
    # string operation to sort camera and date
    folderCam = fileName.split("_")[0]
    folderPlace = fileName.split("_")[1]
    folderDateTime = fileName.split("_")[3]
    folderDateTime = folderDateTime[0:12]
    folderDate = (
        folderDateTime[0:4] + "_" + folderDateTime[4:6] + "_" + folderDateTime[6:8]
    )
    folderTime = folderDateTime[8:10] + "_hrs"

    # ye olde print debug
    if debugMessages:
        print(folderCam)
        print(folderPlace)
        print(folderDateTime)
        print(folderTime)
    else:
        pass

    path = os.path.normpath(
        os.path.join(targetPath, folderPlace, folderCam, folderDate, folderTime)
    )

    if debugMessages:
        print(path)
    else:
        pass

    try:
        os.makedirs(path)
        shutil.move(fileName, path)
        logging.info("moving %s to %s" % (fileName, path))
        print("moving %s to %s" % (fileName, path))

    except OSError as error:
        # print(error)
        # we still need to move things eve if the folder exists error is thrown
        try:
            shutil.move(fileName, path)
            print("moving %s to %s" % (fileName, path))
            logging.info("moving %s to %s" % (fileName, path))

            # this will be thrown if the folder already exists.
        except OSError as error:
            logging.warning("Failed to move %s due to %s" % (fileName, error))

        except:
            logging.warning("Failed to move %s due to %s" % (fileName, error))
            pass


for x in files:
    if debugMessages:
        idFiles(x)
    else:
        pass
    createFolder(x)
