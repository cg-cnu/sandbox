#!/usr/bin/python

import os
import sys
import shutil
import tarfile

blenderFolder = sys.argv[1]

# get folder name 
folderName, frmt = os.path.splitext(blenderFolder)
# get version
version = blenderFolder.split("-")[1]

installationPath = '/opt/blender/'
symlinkPath = "/opt/blender/launcher/"

# checking if you need to overwrite the existing version
# if os.path.exists(installationPath+version):

	# error checking if the input is a file or folder
	# if format in [".bz2", ".tar"]:

tar = tarfile.open(blenderFolder)
tar.extractall(path=installationPath)
tar.close()

os.rename(installationPath+folderName, installationPath+version)


# create symlink
os.symlink(installationPath+version+"/blender", symlinkPath + "blend" + version)




