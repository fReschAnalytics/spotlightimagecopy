# -*- coding: utf-8 -*-
"""
This is a script to fetch the contents of Microsoft's
Spotlight Lock Screen content directory for a given user.
It necessarily assumes Windows 10 as the operating system.
"""

import glob
import os
import shutil

# Begin by fetching current user name.
USER = os.environ["USERNAME"]

# Define the source; wild card the string after the underscore for the
# ContentDeliveryManager_ directory. Define the storage directory.
SOURCE = glob.glob(
    "C:\\Users\\" + USER + "\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_*\\LocalState\\Assets")
DEST = "C:\\Users\\" + USER + "\\OneDrive\\Pictures\\Spotlight"

# Create the storage directory if it doesn't already exist.
if not os.path.exists(DEST):
    print("Making Necessary Directory")
    os.mkdir(DEST)

blacklisted_items = ["235935af667a82e2fd4a3f6efc77616e7be2892f5d94a3fc45cd01956a08e147"]

# For each filename in the ContentDeliveryManager_ directory, if it is bigger
# than 200 kb, copy it into the storage directory with a .png extension.
for dirname, dirnames, filenames in os.walk(SOURCE[0]):
    # print path to all subdirectories first.
    # for subdirname in dirnames:
    # print(os.path.join(dirname, subdirname))

    # print path to all filenames.
    for filename in filenames:
        if os.stat(os.path.join(dirname, filename)).st_size > 200000 and not filename in blacklisted_items  :
            print(os.path.join(dirname, filename))
            print("{0}\\{1}.bmp".format(DEST, filename))
            shutil.copyfile(os.path.join(dirname, filename),
                            DEST + "\\" + filename + ".bmp")
            shutil.copyfile(os.path.join(dirname, filename),
                            DEST + "\\" + filename + ".jpg")
