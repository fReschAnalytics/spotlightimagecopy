"""
Script is meant to grab the current lock screen image and set the
desktop wallpaper to be the same image from the results of the
SpotLightImageCopy.py script.
"""

import ctypes
import os
import winreg
from ctypes import wintypes


# Get current key function
def get_reg(KeyName, REG_PATH, name):
    try:
        if KeyName == 'HKEY_CURRENT_USER':
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                          winreg.KEY_READ)
        elif KeyName == 'HKEY_LOCAL_MACHINE':
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0,
                                          winreg.KEY_READ)
        else:
            pass

        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None


# Set registry key function
def set_reg(KeyName, DES_PATH, name, value):
    try:
        if KeyName == 'HKEY_CURRENT_USER':
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, DES_PATH)
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, DES_PATH, 0,
                                          winreg.KEY_WRITE)
        elif KeyName == 'HKEY_LOCAL_MACHINE':
            winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, DES_PATH)
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, DES_PATH, 0,
                                          winreg.KEY_WRITE)
        else:
            pass

        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


# Fetch the right version from the directory for the creative bit
REG_PARENT = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Authentication\\LogonUI\\Creative\\"
CREATIVE_VERSIONS = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PARENT, 0, winreg.KEY_READ)
ACTIVE_CREATIVE_VERSION = winreg.EnumKey(CREATIVE_VERSIONS, 0)
winreg.CloseKey(CREATIVE_VERSIONS)

# Set the REG_PATH to the right creative version
REG_PATH = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Authentication\\LogonUI\\Creative\\" + ACTIVE_CREATIVE_VERSION

print(REG_PATH)

# Get current profile
reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 1,
                         winreg.KEY_READ)
profiles = winreg.EnumKey(reg_key, 2)
winreg.CloseKey(reg_key)

print(profiles)

# Fetch the current lock screen
currentImage = get_reg("HKEY_LOCAL_MACHINE", REG_PATH + "\\" + profiles, 'landscapeImage')
print(currentImage)

# Split the path of currentImage
tmp = currentImage.split("\\")

# Fetch the current wallpaper
DES_PATH = "Control Panel\\Desktop"

currentWallpaper = get_reg("HKEY_CURRENT_USER", DES_PATH, "WallPaper")
print(currentWallpaper)

whr = currentWallpaper.split("\\")

if whr[3][0:len(whr[3]) - 4] != tmp[9]:
    # Fetch current user name.
    USER = os.environ["USERNAME"]

    # Create the location of the copied image
    val = "C:\\Users\\"+USER+"\\OneDrive\\Pictures\\Spotlight\\" + tmp[9] + ".bmp"
    print(val)

    # subprocess.call("rundll32.exe user32.dll, UpdatePerUserSystemParameters")
    SPI_SETDESKWALLPAPER = 0x0014
    SPIF_UPDATEINIFILE = 0x0001
    SPIF_SENDWININICHANGE = 0x0002

    user32 = ctypes.WinDLL('user32')
    SystemParametersInfo = user32.SystemParametersInfoW
    SystemParametersInfo.argtypes = ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint
    SystemParametersInfo.restype = wintypes.BOOL
    print(SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, val, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE))
