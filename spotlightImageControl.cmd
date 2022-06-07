@echo off
REM This is a control file for copying the contents of the spotlight image directory and then setting them as the users wallpaper.

C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe C:\Users\%USERNAME%\Documents\Projects\Python\spotlightimagecopy\SpotlightImageCopy.py
C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe C:\Users\%USERNAME%\Documents\Projects\Python\spotlightimagecopy\SetSpotlightAsWallpaper.py