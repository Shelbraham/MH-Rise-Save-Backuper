### config ###
steamBasePath = R"C:\Program Files (x86)\Steam\userdata"
steamId = "54470748"
gameId = "1446780"

backupFolder = R"D:\Dropbox\MH_Rise_Backups"

# maximum number of backups to keep, set to zero to keep all
maxFilesToKeep = 20


### begin program ###
import shutil
import os.path
from datetime import datetime
from os import listdir, remove
from os.path import isfile


saveFolder = os.path.join(steamBasePath, steamId, gameId)
destination = os.path.join(backupFolder, "save")
dateStamp = (
    datetime.isoformat(datetime.now())
    .replace("-", "")
    .replace(":", "")
    .replace("T", "_")[:-7]
)
targetFile = os.path.join(backupFolder, f"MHRise_SaveData.{dateStamp}")
try:
    shutil.rmtree(destination)
except FileNotFoundError:
    pass
print("Copying files to backupfolder...")
shutil.copytree(saveFolder, destination)
print("Compressing backup...")
shutil.make_archive(targetFile, "zip", destination)

if maxFilesToKeep > 0:
    print("Pruning old backups...")
    files = [f for f in listdir(backupFolder) if isfile(os.path.join(backupFolder, f))]
    files.sort()
    allFiles = set(files)
    keepFiles = set(files[-maxFilesToKeep:])
    delFiles = allFiles - keepFiles

    for fname in delFiles:
        print(f"Deleting '{fname}'....")
        remove(os.path.join(backupFolder, fname))

print("All Done!")
input("Press ENTER to close...")
