from sys import exit as sysExit
from time import sleep
from shutil import copyfile
from os import path as osPath, listdir, system as cmd

def isExists(path):

    result = osPath.exists(path)
    
    if result == False:

        try:
        
            f = open(path)
            f.close()
            
            return True
        
        except IOError:
        
            return False
            
            
        return False
        
    return True
    
if not isExists("./backup"):

    print("Backup directory does not exist!")
    sysExit(1)
    
cmd("taskkill /F /IM explorer.exe")

sleep(2)

for dir in listdir("./backup"):

    if osPath.isdir("./backup/" + dir):
    
        file = open("./backup/" + dir + "/info.txt", "r")
        
        filePath = file.read()
        
        cmd("takeown /F \"" + filePath + "\" /A")
        cmd("icacls \"" + filePath + "\" /grant:r \"*S-1-5-32-544\":f")
        
        copyfile("./backup/" + dir + "/InputSwitch.dll", filePath)
        
        cmd("icacls \"" + filePath + "\" /setowner \"NT SERVICE\TrustedInstaller\" /C /L /Q")
        cmd("icacls \"" + filePath + "\" /grant:r \"NT SERVICE\TrustedInstaller\":rx")
        cmd("icacls \"" + filePath + "\" /grant:r \"*S-1-5-32-544\":rx")
        
cmd("start %windir%\explorer.exe")

print("Done!")