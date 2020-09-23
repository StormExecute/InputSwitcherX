# InputSwitcherX

## Installation and Patching

0. Read [the notes](#descAndNodes) first.
1. Download Python 3 from official site - https://www.python.org/downloads/
2. Launch installer, click ```add python to PATH```
3. Clone this repository and cd there with command:
```bash
git clone https://github.com/StormExecute/InputSwitcherX.git && cd InputSwitcherX
```
4. Copy your original InputSwitch.dll file from %windir%\system32\InputSwitch.dll to /InputSwitcherX/input/ . This can be done with this command:
```bash
copy %windir%\system32\InputSwitch.dll input\InputSwitch.dll /Y
```
5. Create a patch based on your InputSwitch.dll file using the command:
```bash
python createPatch.py
```
6. At the output, you should get the output directory with the edited InputSwitch.dll. It remains to replace the original InputSwitch.dll in the system directory. To do this, **run setPatch.bat as administrator**.

<a name="descAndNodes"></a>
## Description and Notes

This is patcher for %windir%\system32\InputSwitch.dll . Its main purpose is to prevent the language switching animation from appearing.

To accomplish its task - the patch overwrites some hex data, which is responsible for the appearance of the above animation of the layout.

***Finding and changing the correct hex address is a risky task and perhaps for someone this patch will do more harm than good, so the responsibility for applying it is entirely up to whoever applies this patch!***

Regarding which hex data the patch rewrites. First of all, the details described in a special forum topic dedicated to this problem were taken into account - https://www.cyberforum.ru/windows10/thread2466696.html#post14150170 .

Comparing the differences between the patched and the original files, duplicate hex sections were identified that begin with **FF FF 83 F8 FF** and continue like **74 1F 48 63 D0**.

The continuing hex data in the patched file has been replaced with a void that continues until the next combination: **33 C0 48 8B**.

Based on the fact that the void in the file after the fix solves the original problem - replacing the same sections in the new version of the file should bring the desired result.

Roughly speaking, this patch replaces sections **74 1F 48 63 D0** to **33 C0 48 8B** with *90*, which is a void.

## Special thanks

NShut (https://www.cyberforum.ru/windows10/thread2466696.html#post14150170) - for data that helped automate the patching process
Waysek (https://www.cyberforum.ru/windows10/thread2466696-page2.html#post14410402) - for the base of .bat file posted in the final release of this repository
