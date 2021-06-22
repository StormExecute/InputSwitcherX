from sys import exit as sysExit
from time import sleep
from binascii import unhexlify, hexlify
from shutil import copyfile
from pathlib import Path as pathLibPath
from os import path as osPath, makedirs as osMakedirs, environ as env, listdir, system as cmd

def make_dirs(dest):
    if not osPath.exists(dest):
        osMakedirs(dest)
        
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

        
class Patch():

    def getSystem32(self):
    
        system32 = osPath.join(env["windir"], "System32")
    
        if not isExists(system32):
        
            return osPath.join(env["windir"], "system32")
            
        return system32

    def __init__(self):
    
        self.thisPath = pathLibPath(__file__).parent.absolute()
        self.mainFileName = "InputSwitch.dll"
        self.hasErrors = False
    
        dirs = [
        
            self.getSystem32()
            
        ]
        
        for dir in listdir(osPath.join(env["windir"], "WinSxS")):
        
            if osPath.isdir(osPath.join(env["windir"], "WinSxS", dir)):
            
                if "inputswitch" in dir:
                
                    dirs.append(osPath.join(env["windir"], "WinSxS", dir))
                
        print("Процесс патчинга начинается. Отключение explorer.exe...")
                
        cmd("taskkill /F /IM explorer.exe")
        
        sleep(2)
                
        for dir in dirs:
        
            self.do(dir)
            
        cmd("start %windir%\explorer.exe")
            
        if self.hasErrors is True:
        
            print("Патч завершился с ошибками. Это есть не добрый знак. Попытайтесь откатить изменения с помощью \"python offPatch.py\"")
            sysExit(1)
            
        else:
        
            print("Done!")
            sysExit(0)
            
    def warn(self, warntext):
    
        print("WARN! FilePath: " + self.filePath + " : " + warntext)
            
    def error(self, error):
    
        self.hasErrors = True
        print("ERROR! FilePath: " + self.filePath + " : " + error)
        
    def do(self, dir):
    
        basename = osPath.basename(dir)
        self.filePath = osPath.join(dir, self.mainFileName)
        
        if not isExists(self.filePath):

            self.warn("not exists")
            return
        
        # set group of admins as the owners of file 
        cmd("takeown /F \"" + self.filePath + "\" /A")
        
        # give the administrator group full access to this file 
        cmd("icacls \"" + self.filePath + "\" /grant:r \"*S-1-5-32-544\":f")
            
        # backup
        if not isExists("./backup/" + basename):
        
            backupPath = osPath.join(self.thisPath, "backup", basename, self.mainFileName)
        
            make_dirs("./backup/" + basename)
            copyfile(self.filePath, backupPath)
            
            f = open(osPath.join(self.thisPath, "backup", basename, "info.txt"), "a")
            f.write(self.filePath)
            f.close()
            
        
        status = self.processPatch()
        
        # return the rights to trusted installer
        cmd("icacls \"" + self.filePath + "\" /setowner \"NT SERVICE\TrustedInstaller\" /C /L /Q")
        
        # give administrators and trusted installer read and execute permissions
        cmd("icacls \"" + self.filePath + "\" /grant:r \"NT SERVICE\TrustedInstaller\":rx")
        cmd("icacls \"" + self.filePath + "\" /grant:r \"*S-1-5-32-544\":rx")
            
        
    def processPatch(self):
    
        with open(self.filePath, 'rb') as f:

            hexdata = hexlify(f.read()).decode("utf-8")
            
            i = 0
            pointer = 0
            hexAsList = []
            
            for h in hexdata:

                if i % 2 == 0 and i != 0: pointer += 1
                
                if not pointer < len(hexAsList): hexAsList.append(h)
                else: hexAsList[pointer] += h
                
                i += 1
            
            i = 0
            inARow = 0
            maxArea = 40
            res = 0
            
            for h in hexAsList:
            
                if inARow >= 5:
                
                    if maxArea > 0:
                    
                        maxArea -= 1
                        
                        hexAsList[i] = "90"
                        
                        if h == "33" and inARow == 5:
                        
                            inARow += 1
                            
                        elif h == "c0" and inARow == 6:
                        
                            inARow += 1
                            
                        elif (h == "48" or h == "8b") and inARow == 7:
                        
                            # final
                            
                            hexAsList[i] = h
                            hexAsList[i - 1] = "c0"
                            hexAsList[i - 2] = "33"
                            
                            res = 1
                            
                            break
                        
                    else:
                    
                        break
                        
                elif h == "ff" and inARow == 0:
                    inARow += 1
                elif h == "ff" and inARow == 1:
                    inARow += 1
                elif h == "83" and inARow == 2:
                    inARow += 1
                elif h == "f8" and inARow == 3:
                    inARow += 1
                elif h == "ff" and inARow == 4:
                    inARow += 1
                else:
                    inARow = 0
                    
                i += 1
                
            if res == 0:
                self.error("cant patch this dll!")
                return False
                
            with open(self.filePath, 'wb') as fout:
                for h in hexAsList:
                    fout.write(unhexlify(h))
                    
            print(self.filePath + ": SUCCESSFUL PATCHING")
            return True
        
Patch();