from sys import exit as sysExit
from binascii import unhexlify, hexlify
from os import path as osPath, makedirs as osMakedirs

def make_dirs(dest):
    if not osPath.exists(dest):
        osMakedirs(dest)

with open('./input/InputSwitch.dll', 'rb') as f:

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
    inNopSet = 0
    res = 0
    
    for h in hexAsList:
    
        if inARow == 6 and inNopSet >= 29:
            break
        elif inARow == 6 and h != "33":
            hexAsList[i] = "90"
            inNopSet += 1
            #28 last here
        elif inARow == 6 and h == "33":
            if inNopSet == 28: res = 1
            break
        elif h == "74" and inARow == 0:
            inARow += 1
        elif h == "1f" and inARow == 1:
            inARow += 1
        elif h == "48" and inARow == 2:
            inARow += 1
        elif h == "63" and inARow == 3:
            inARow += 1
        elif h == "d0" and inARow == 4:
            inARow += 1
        elif inARow == 5:
            
            for lasts in range(6): hexAsList[i - lasts] = "90"
            inNopSet = 1
            inARow = 6
            
        else:
            inARow = 0
            
        i += 1
        
    if res == 0:
        print("Cant patch dll!")
        sysExit(1)
        
    make_dirs("./output")
        
    with open('./output/InputSwitch.dll', 'wb') as fout:
        for h in hexAsList:
            fout.write(unhexlify(h))
            
    print("Done!")
    sysExit(0)