import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import secrets
import base64
import os.path

class Encryption:
    def __init__(self, master_password):
        self.master_password = master_password
        self.filename = 'passwords.json'
        self.key = self.generate_key()

# Generating a random byte-string to use as a salt for the key
    def generate_salt(self,length):
        with open('salt.salt', 'wb') as file:
            file.write(secrets.token_bytes(length))

# Key derivation function, using the Scrypt algorithm giving us a key derived from the password input by the user
    def generate_key(self):
        if not os.path.exists('salt.salt'):
            self.generate_salt(16)
        salt = open('salt.salt', 'rb').read()
        kdf = Scrypt(salt=salt, length=32, n=2**20, r=8, p=1)
        return base64.urlsafe_b64encode(kdf.derive(self.master_password.encode()))

    def encrypt_file(self):
        f = Fernet(self.key)
        with open(self.filename, 'rb') as file:
            file_contents = file.read()
            file_encrypted = f.encrypt(file_contents)
        with open(self.filename, 'wb') as file:
            file.write(file_encrypted)

    def decrypt_file(self):
        f = Fernet(self.key)
        with open(self.filename, 'rb') as file:
            file_contents = file.read()
            try:
                file_decrypted = f.decrypt(file_contents)
                with open(self.filename, 'wb') as file:
                    file.write(file_decrypted)
            except cryptography.fernet.InvalidToken:
                print('Incorrect Password')
                exit()
