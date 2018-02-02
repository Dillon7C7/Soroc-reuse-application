import getpass
import user
import database

print('Welcome to the Soroc Reuse Automation Application! Version 1')
db = database.Database('users.db')

while True:
	print('Press 1 to login.\nPress 2 to register your Soroc login ID with this application.')
	choice = input()
	if choice == '1' or choice == '2':
		break
	print('Invalid input!')

while True:
	print('Enter your username: ', end='')
	username = input()
	if choice == '1': # Handle the login case.

		# We try to get BOTH username and password before alerting the user that login
		# credientials are incorrect. This increases security, as an attacker doesn't know
		# if a username is in the database or not.
		pw1 = getpass.getpass('Enter password: ')
		userInfo = db.retrieveUserInfo(username) # Is the user registered in the database?
				  
		if userInfo: # If True, user info was found. Now we can check the password.
			currentUser = user.User(*userInfo) # Create a User object.
			isPasswordCorrect = currentUser.checkPassword(pw1)
			if isPasswordCorrect:
				break
		print('Incorrect username and/or password!')
		# warning message from database.retrieveUserInfo()
print('Gong xi ni')

# else: 	# choice == 2
# 	while True:
# 		pw1 = getpass.getpass('Enter password: ')
# 		pw2 = getpass.getpass('Enter password again: ')
# 		if pw1 == pw2:
# 			break
# 		print('Passwords did not match!')




### ---------------- user not in database

# print('User not found in database! Either the user doesn\'t exist, or the database file was moved.')
# print('')