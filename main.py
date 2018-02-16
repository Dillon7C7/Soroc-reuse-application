import getpass
import user
import database


def userInitialization():
	'''Login and registration logic.'''

	db = database.Database('users.db')
	
	while True:

		print('Press 1 to login.\nPress 2 to register your Soroc login ID with this application.')
		choice = input()
		if choice == '1' or choice == '2':
			break
		print('Invalid input!\n')

	while True:
		
		if choice == '1': # Handle the login case.

			# We try to get BOTH username and password before alerting the user that login
			# credientials are incorrect. This increases security, as an attacker doesn't know
			# if a username is in the database or not.

			print('Enter your username: ', end='')
			username = input()
			pw1 = getpass.getpass('Enter your password: ')

			userInfo = db.retrieveUserInfo(username, False) # Is the user registered in the database?	  
			if userInfo: # If True, user info was found. Now we can check the password.
				currentUser = user.User(*userInfo) # Create a User object.
				if currentUser.checkPassword(pw1):
					break

			# warning message from database.retrieveUserInfo()
			print('Incorrect username and/or password!\n')
		
		else: # choice == 2. Handle the "registration" case.

			print('Enter your Reuse Application login username: ', end='')
			username = input()
			if not db.retrieveUserInfo(username, False): # User doesn't already exist in the database.

				pw1 = getpass.getpass('Enter your password: ')
				pw2 = getpass.getpass('Enter your password again: ')

				if pw1 == pw2:
					currentUser = user.User(username)
					currentUser.hashPassword(pw1)
					db.insertUserInfo(currentUser)
					break

				else:
					print('Passwords don\'t match!!\n')

			else:
				print('User is already registered in database!\n')		

	db.close()

if __name__ == '__main__':

	print('Welcome to the Soroc Reuse Automation Application! Version 1\n')
	userInitialization()
	print('done')