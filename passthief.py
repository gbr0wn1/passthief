#!/usr/bin/env python
# 3rd party
import colorama as Color
from colorama import Fore,Back,Style
# Imports
from sys import path,executable,exit,version_info as version
import os
from time import localtime
from argparse import ArgumentParser
# Module functions and all
from data.core import *
# Init colorama
Color.init()
# Print the banner
PrintBanner()
# Add myself to the path (for pyinstaller's hiddenimports)
path.append(os.path.dirname(executable))
# Check for the Python version, Python 3.X required for now
ver = (version.major,version.minor)
if ver < (3,2):
	print("{red}This script requires Python 3.2 or greater{reset}\n".format(red=Fore.RED,
								         reset=Style.RESET_ALL))
	exit(2)
# Command line arguments
parser = ArgumentParser()
parser.add_argument("-m",metavar="MODULE NAME",nargs="*",help="modules to load")
parser.add_argument("-o",nargs="?",metavar="FILE", help="output file")
argv = parser.parse_args()
# Make it easier for plugins to be loaded from the command line
out = argv.o
argv = TransformArgs(argv.m)
# Load all the plugins/modules
modules = LoadModules(argv)
# Check the modules to see if they are good
modules = CheckModules(modules)
# Call all the steal methods
if out == None:
	time = localtime()
	print("\nStarted: {time}".format(time="{day}/{month}/{year} {hour}:{min}".format(day=time.tm_mday,
		                                                                         month=time.tm_mon,
		                                                                         year=time.tm_year,
		                                                                         hour=time.tm_hour,
		                                                                         min=time.tm_min)))
CallModules(modules,out)
if out == None:
	time = localtime()
	print("Finished: {time}".format(time="{day}/{month}/{year} {hour}:{min}".format(day=time.tm_mday,
		                                                                         month=time.tm_mon,
		                                                                         year=time.tm_year,
		                                                                         hour=time.tm_hour,
		                                                                         min=time.tm_min)))
else:
	print("\nWritten results to a file...")
# Done. Wait for a keypress
input("\nDone. Press enter to continue...")

# Functions
