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
		self.connect()
		self.createTable()

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
		print('Inserting user info for ' + user.username + '...')
		self.cursor.execute('''INSERT INTO users(
				 	 username, salt, hash) VALUES(?,?,?)''',
					 (user.username, user.salt, user.hash))
		self.db.commit()

	def retrieveUserInfo(self, username):
		'''Takes a username string (of a user object) and returns a tuple containing the username, salt, and hash.'''
		self.cursor.execute('''SELECT username, salt, hash FROM users WHERE username=?''', (username,))
		self.db.commit() 	# Not sure if a commit is needed here, but added a call just in case.
		userData = self.cursor.fetchone()
		if not userData: 	# Does the user exist in the database? If not, return None.
			print('WARNING: User ' + username + ' not found in database!')    ######## NEED FIX
			return None
		else:
			print('Retrieved info for user: ' + userData[0] + '.')
			return userData

	def deleteUser(self, username):
		'''Takes a username string (of a user object) and deletes that user from the database.'''
		print('Deleting user info for ' + username + 'from the database...')
		self.cursor.execute('''DELETE FROM users WHERE username=?''', (username,))
		self.db.commit()

	def close(self):
		'''Close the database connection.'''
		print('Closing the connection to database ' + self.databaseName + '...')
		self.db.close()
