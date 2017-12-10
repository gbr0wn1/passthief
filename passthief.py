#!/usr/bin/env python
# Future
from __future__ import print_function
# 3rd-party
import colorama as Color
from colorama import Fore,Back,Style
# Imports
from sys import argv,path,executable
import os
from time import localtime
# Module functions and all
from data.const import *
# Init colorama
Color.init()
# Print the banner
PrintBanner()
# Add myself to the path (for pyinstaller's hiddenimports)
path.append(os.path.dirname(executable))
# Make it easier for plugins to be loaded from the command line
argv = ParseArgs(argv)
# Load all the plugins/modules
modules = LoadModules(argv)
# Check the modules to see if they are good
modules = CheckModules(modules)
# Call all the steal methods
time = localtime()
print("\nStarted: {time}".format(time="{day}/{month}/{year} {hour}:{min}".format(day=time.tm_mday,
                                                                                 month=time.tm_mon,
                                                                                 year=time.tm_year,
                                                                                 hour=time.tm_hour,
                                                                                 min=time.tm_min)))
CallModules(modules)
time = localtime()
print("Finished: {time}".format(time="{day}/{month}/{year} {hour}:{min}".format(day=time.tm_mday,
                                                                                 month=time.tm_mon,
                                                                                 year=time.tm_year,
                                                                                 hour=time.tm_hour,
                                                                                 min=time.tm_min)))
