	# Steam Smurf Switcher with mobile support using steam.guard by ValvePython and PyAutoIt by jacexh #
						# PyAutoIt: https://pypi.python.org/pypi/PyAutoIt/0.4 #
						# steam.guard: https://github.com/ValvePython/steam #
											# Much love, jfx #
									
# TO-DO: 
# Encryption #:
	# Coming soon, AES encryption with master password #

import autoit, time, os, json, subprocess, base64
import steam.guard as sa

# Config settings here, feel free to change them!
configpath = os.getenv('APPDATA')+"\\jfx"
config = configpath + "\\users.json"

# Config
if not os.path.exists(configpath):
    os.makedirs(configpath)

# Check to see if the config exists, if not make one
# Messy way of doing it but it gets the job done... maybe I'll re-do it one day...
try:
	with open(config, 'r') as data_file:    
		data = json.load(data_file)
except:
	f = open(config, 'w+')
	f.write('{"accounts":[]}')
	f.close()
	with open(config) as data_file:    
		data = json.load(data_file)

# Defining key stuff #

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
	
def enter():
	raw_input("Press ENTER to continue . . .")

def validateInput(input):
	if input.isdigit() == False or int(input) >= i or int(input) < 1:
		return False
	else:
		return True
	
def createNewAccount():
	newusername = raw_input("Enter the username: ")
	newpassword = raw_input("Enter the password: ")
	newmobile = raw_input("Enter the mobile code, blank if none: ")

	data['accounts'].append({  
		'username': newusername,
		'password': newpassword,
		'mobile': newmobile
	})
	
	with open(config, 'w') as outfile:  
		json.dump(data, outfile, sort_keys = False, indent = 4, ensure_ascii=False)
	
	print "Account created."
	enter()
	main()

	
def deleteAccount(i):
	chosenDelete = raw_input("Type the number for the account you would like to delete: ")
	
	while validateInput(chosenDelete) == False: #validation, check if its a number
		print "ERROR: Choose an account on the list."
		chosenDelete = raw_input("Type the number for the account you would like to delete: ")
		
	chosenDelete = int(chosenDelete) - 1 #line it up with the json, make it an int
	del data['accounts'][chosenDelete]
	
	with open(config, 'w') as outfile:  
		json.dump(data, outfile, sort_keys = False, indent = 4, ensure_ascii=False)
	
	print "Account deleted."
	enter()
	main()

	
def editConfig():
	subprocess.call(['notepad.exe', config]) #we use subprocess here because its better and it works
	enter()
	main()

def browserLogin(i):
	chosenAccount = raw_input("Type the number for the account you would like to display login details for: ")
	
	while validateInput(chosenAccount) == False: #validation, check if its a number
		print "ERROR: Choose an account on the list"
		chosenAccount = raw_input("Type the number for the account you would like to display login details for: ")

	chosenAccount = int(chosenAccount) - 1 #line it up with json, make int
	
	print "username: {}".format(data['accounts'][chosenAccount]['username'])
	print "password: {}".format(data['accounts'][chosenAccount]['password'])
	if data['accounts'][chosenAccount]['mobile']:
		print "2FA code: {}".format(sa.generate_twofactor_code(base64.b64decode(data['accounts'][chosenAccount]['mobile'])))
	enter()
	main()
	
def mobileCode(i):
	chosenAccount = raw_input("Type the number for the account you would like to display login details for: ")
	
	while validateInput(chosenAccount) == False: #validation, check if its a number
		print "ERROR: Choose an account on the list"
		chosenAccount = raw_input("Type the number for the account you would like to display login details for: ")

	chosenAccount = int(chosenAccount) - 1 #line it up with json, make int
	if data['accounts'][chosenAccount]['mobile']:
		print "2FA code: {}".format(sa.generate_twofactor_code(base64.b64decode(data['accounts'][chosenAccount]['mobile'])))
	else:
		print "Error finding mobile code for account"
	enter()
	main()
	
def main ():

	cls()
	
	print "########################"
	print "# jfx's Smurf Switcher #"
	print "########################"
	print ""
	
	global i
	i = 1
	for account in data['accounts']:
		print str(i) + ' - ' + account['username']
		i = i + 1

	print
	print "n - Add new account"
	print "d - Delete an account"
	print "e - Edit config"
	print "b - Print login details (for browser logins)"
	print "c - Mobile code only"
	print
	print "Typing in the account and ENTER will auto login to that account"

	chosenAccount = raw_input("Type your choice then press ENTER: ")


	while chosenAccount.isdigit() == False: # validation, check if its a number, this check is needed to differentiate the character options from numerical and also to provide some nice feedback to the user
		if chosenAccount == "n" or chosenAccount == "e" or chosenAccount == "d" or chosenAccount == "b" or chosenAccount == "c": # we skip if its one of the alpha values
			break
		print "ERROR: Please enter a valid option"
		chosenAccount = raw_input("Type the number for the account then press ENTER: ")


	if chosenAccount.isdigit() == False: #if its still false its one of the alpha values
		if chosenAccount == "n":
			createNewAccount()		
		
		if chosenAccount == "d":
			deleteAccount(i)
			
		if chosenAccount == "e":
			editConfig()
			
		if chosenAccount == "b":
			browserLogin(i)
			
		if chosenAccount == "c":
			mobileCode(i)

	else: #they chose a number of some sorts

		while validateInput(chosenAccount) == False: #validation, check if the account exists
			print "ERROR: Choose an account on the list."
			chosenAccount = raw_input("Type the number for the account then press ENTER: ")

		chosenAccount = int(chosenAccount) - 1
		
		print "Killing Steam..."
		os.system('taskkill /f /im steam.exe') #kill steam
		print "Waiting 3 seconds before starting Steam..."
		time.sleep(3)

		# For some reason subprocess doesn't work, leaving this commented out until I figure out why...
		#dargds = ['C:\Program Files (x86)\Steam\Steam.exe', '-login', data['accounts'][chosenAccount]['username'], data['accounts'][chosenAccount]['password']]#args
		#subprocess.call(dargds) #run steam

		print "Launching Steam..."
		os.system('start "" "C:\Program Files (x86)\Steam\Steam.exe" -login {} {}'.format(data['accounts'][chosenAccount]['username'],data['accounts'][chosenAccount]['password']))

		if data['accounts'][chosenAccount]['mobile']: #if theres a mobile code
			print "Waiting for Steamguard window..."
			autoit.win_wait("Steam Guard") #wait for window... sometimes it takes a while

			print "Steamguard window found, generating code..."
			code = sa.generate_twofactor_code(base64.b64decode(data['accounts'][chosenAccount]['mobile']))
			
			autoit.win_activate("Steam Guard") #open it up in case it's not activated
			autoit.win_wait_active("Steam Guard") #wait for it to be activated, in case of delay
			print "Entering auth code: {} into window...".format(code)
			autoit.send(code)
			time.sleep(0.2) #small delay cant hurt
			autoit.send('{ENTER}')
		
		raw_input()

if __name__ == "__main__":
	main()
