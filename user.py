import os
import binascii
import hashlib

class User(object):
	'''A user of the Soroc reuse system.

		Attributes:
			username: A string representing the user's username.
			password: A string representing the user's password.
			salt: A 16-byte long bytes object representing the user's salt.
			hashed: a bytes object representing the user's hashed password.		 
	'''

	def __init__(self, username, salt=b'', hashed=b''):
		self.username = username
		self.salt = salt
		self.hash = hashed
 
	def generateSalt(self):
		'''Generate a salt to be used to hash the user's password as a bytes object'''
		if not self.salt: 	# If the salt variable is empty, we need to generate a salt.
			print('Generating salt for ' + self.username + '...')
			self.salt = os.urandom(16)
			self.salt = binascii.hexlify(self.salt)
		else:
			while True:
				print('User already has a salt! Generate new one? (y/n)')
				decision = input()

				if decision == 'Y'.lower():
					self.salt = b''
					self.generateSalt()
					break
				elif decision == 'N'.lower():
					break
				else:
					print('Invalid input!')
		return self.salt
            
	def hashPassword(self, password):
		'''Return a user's hashed plaintext password as a bytes object.'''
		password = password.encode('UTF-8')

		if self.salt == b'': # Generate a salt if the generateSalt() call is forgetten.
			self.salt = self.generateSalt() # Generate a salt first.

		print('Hashing ' + self.username + '\'s password...')

		self.hash = kdfWrapper(self.salt, password)
		return self.hash

	def checkPassword(self, loginPassword):
		'''Returns True if a user's entered password's hash matches the hash of the stored password.'''
		return kdfWrapper(self.salt, loginPassword.encode('UTF-8')) == self.hash

def kdfWrapper(salt, password):
	'''Returns a hexlified desired key from a salt and a passphrase.'''
	dk = hashlib.pbkdf2_hmac( 	# KDF function for hashing and key stretching.
		'sha256',
		password,
		salt,
		100000)
	dk = binascii.hexlify(dk)
	return dk