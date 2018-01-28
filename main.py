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

#while True:
print('Enter your username: ', end='')
username = input()

if choice == 1: # Handle the login case.
	pw1 = getpass.getpass('Enter password: ')
	userInfo = db.retrieveUserInfo(username)
	



	if userInfo: # User info was found.
		account = user.User(*userInfo)

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