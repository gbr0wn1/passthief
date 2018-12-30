# :: passthief :unlock: :running::dash:
A Python script to steal all the passwords via the use of plugins :smiling_imp:
## Disclaimer:
Do not use this tool for illegal purposes ( steal from somebody else ).<br />
In accordance with the Computer Misuse Act 1990, it is illegal to use this tool in order to access or attempt to access a computer system without authorisation.
I am not responsible for any damage you cause while using this tool.
## Usage:
<b>passthief</b> is a Python script designed to work with dynamic loading of modules or plugins, whatever you may call them.<br />
By default Firefox and Chrome modules are enabled.<br/>
If you wish to use a module called "linux", you call the script like this:
```bash
./passthief.py -m linux
```
The output should be something like this(if the module is present):
```

	██████╗  █████╗ ███████╗███████╗████████╗██╗  ██╗██╗███████╗███████╗
	██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║  ██║██║██╔════╝██╔════╝
	██████╔╝███████║███████╗███████╗   ██║   ███████║██║█████╗  █████╗
	██╔═══╝ ██╔══██║╚════██║╚════██║   ██║   ██╔══██║██║██╔══╝  ██╔══╝
	██║     ██║  ██║███████║███████║   ██║   ██║  ██║██║███████╗██║
	╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚═╝
	Version 0.2.1
	
[*] Checking modules:
[*] Loaded module: Linux
[*] Loaded module: Firefox
[*] Loaded module: Chrome

Started: 10/12/2017 3:9
-Chrome:
...
-Firefox:
...
-Linux:
...
Finished: 10/12/2017 3:9

```
Otherwise, it would fail to load the module and continue with what it has by default.
## Writing a module:
If you wish to write a module for <b>passthief</b>,you're lucky because it's very easy.<br />
All you have to do is create a corresponding .py file in the modules directory.<br />
Let's write a test module together:
```bash
cd modules
touch test.py
```
Open up your favorite code/text editor and let's get started.
```python
# You can use 3rd party imports too, but PyInstaller might not like it
import colorama
from colorama.Fore import GREEN
from colorama.Style import RESET_ALL
# Each module must have a steal method for it to be valid
# The steal method returns a string,which will then be written either
# on the screen or in a file
def steal():
	colorama.init()
    	return print_it()
# It can have other methods too,passthief doesn't care
# All it cares about is the steal method
def print_it():
	return "{g}This works!{rs}".format(g=GREEN,rs=RESET_ALL)
```
Now try it out:
```bash
./passthief.py -m test
```
## PyInstaller
For 'freezing' <b>passthief</b> I use PyInstaller as it allows me to load the modules at runtime.<br />
I was having some problems with using 3rd party modules(like colorama),but appending them to the hiddenimports list in the <b>passthief.spec</b> file seemed to fix it, for now.<br />
Be aware that if you use 3rd party modules you might want to edit the file.<br />
If you have any ideas be sure to let me know.





