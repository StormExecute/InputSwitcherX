@echo off
cd /d "%~dp0"

Title InputSwitcherX
set systemDll=%windir%\system32\InputSwitch.dll

openfiles > NUL 2>&1
IF %ERRORLEVEL% EQU 0 (

    if exist ".\output\InputSwitch.dll" (
    
        takeown /F %systemDll% /A
        icacls %systemDll% /grant:r "*S-1-5-32-544":f
        taskkill /F /IM explorer.exe
        PING -n 2 -w 1000 127.0.0.1 > nul
        copy ".\output\InputSwitch.dll" %systemDll% /Y
        PING -n 2 -w 1000 127.0.0.1 > nul
        start %windir%\explorer.exe
        icacls %systemDll% /setowner "NT SERVICE\TrustedInstaller" /C /L /Q
        icacls %systemDll% /grant:r "NT SERVICE\TrustedInstaller":rx
        icacls %systemDll% /grant:r "*S-1-5-32-544":rx
        echo Done!
        pause
    
    ) else (
    
        echo Run python createPatch.py first!
        pause
    
    )

) else (

    echo Run this patch with admin rights!
    pause

)