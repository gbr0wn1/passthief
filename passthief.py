#!/usr/bin/env python
# Import the core of the script
from data.core import PassthiefCore
# And colorama
import colorama as Color # Coloring
from colorama import Fore,Back,Style # Coloring
# Initialize everything
PassthiefCore.Initialize()
# Print the banner
PassthiefCore.PrintBanner()
# Check version
if PassthiefCore.CheckVersion():
	print("{red}This script requires Python 3.2 or greater{reset}\n".format(red=Fore.RED,
										 reset=Style.RESET_ALL))
	exit(2)
# Get the command line arguments
psArguments = PassthiefCore.GetArguments()
outFile = psArguments.o
outFormat = psArguments.f
# Load modules ahead
psModules = PassthiefCore.LoadModules(sorted(PassthiefCore.ParseModules(psArguments.m)))
# Check if output type is valid, or not specified at all
if outFile is not None:
	if outFormat is None:
		outFormat = 'text'
	elif PassthiefCore.CheckFormat(outFormat):
		print("{red}Invalid output format specified{reset}\n".format(red=Fore.RED,
									         						 reset=Style.RESET_ALL))
		exit(1)
# Main logic
PassthiefCore.CallModules(psModules,outFile,outFormat)
# Done. Wait for a keypress
input("\nDone. Press enter to continue...")
