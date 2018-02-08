import sqlite3
import re

class Database(object):
	'''The database used to store users' passwords.

		Attributes:
			databaseName: A string representing the database name.
			db: A sqlite3 connection object representing the connection to the database.
			cursor: A sqlite3 cursor object representing the database's cursor.
	'''

	def __init__(self, databaseName):
		self.databaseName = databaseName
		self.db = None
		self.cursor = None
		self.connect() # Connect to the database.
		self.createTable() # Create the table that will hold users' data.

	def handleExtension(self, filename):
		'''Append '.db' to filename if it doesn't exist.'''
		filenameRegex = re.compile(r'.+\.db')
		mo = filenameRegex.search(self.databaseName)
		if not mo: 	# If the given database name doesn't end in '.db', append '.db'.
			self.databaseName = self.databaseName + '.db'
		return self.databaseName

	def connect(self):
		'''Connect to a database and create the cursor for it.'''
		self.databaseName = self.handleExtension(self.databaseName)
		print('Connecting to database ' + self.databaseName + '...')
		self.db = sqlite3.connect(self.databaseName)
		self.cursor = self.db.cursor()	

	def createTable(self):
		'''Create the table that will be used to store user data.'''
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
					 		id INTEGER PRIMARY KEY NOT NULL,
					 		username TEXT NOT NULL UNIQUE,
					 		salt BLOB NOT NULL UNIQUE,
					 		hash BLOB NOT NULL UNIQUE)''')
		self.db.commit()

	def insertUserInfo(self, user):
		'''Takes a user object and inserts the user's information into the database.'''
		if not user.salt or not user.hash: # Don't insert if the user doesn't have a hash or a salt.
			print('Please hash ' + user.username + '\'s password first!')
			print('No data inserted.')
		else:
			try:
				with self.db: # Automatically commit or rollback transactions using with statement.
					self.db.execute('''INSERT INTO users(
							 	 username, salt, hash) VALUES(?,?,?)''',
								 (user.username, user.salt, user.hash))
					print('User info for ' + user.username + 'inserted into database!')
			except sqlite3.IntegrityError:
				print('User is already registered in database!')

			# Since we are dealing with a database object,
			# we do not need to close the connection here using a finally clause.

	def retrieveUserInfo(self, username, verbose=True):
		'''Takes a username string (of a user object) and returns a tuple containing the username, salt, and hash.'''
		# By calling with the username string, we don't need to create a User object.
		self.cursor.execute('''SELECT username, salt, hash FROM users WHERE username=?''', (username,))
		self.db.commit() # Not sure if a commit is needed here, but added a call just in case.

		userData = self.cursor.fetchone()
		if not userData: # Does the user exist in the database? If not, return None.
			print('WARNING: User ' + username + ' not found in database!')  
		else:
			if verbose:
				print('Retrieved data for user: ' + userData[0] + '.')

		return userData

	def deleteUser(self, user):
		'''Takes a user object and deletes that user's data from the database.'''
		if not self.retrieveUserInfo(user, False):
			print('Nothing found to delete!')
		else:
			print('Deleting data for ' + user.username + ' from the database...')
			self.cursor.execute('''DELETE FROM users WHERE username=?''', (username,))
			self.db.commit()

	def close(self):
		'''Close the database connection.'''
		print('Closing the connection to database ' + self.databaseName + '...')
		self.db.close()