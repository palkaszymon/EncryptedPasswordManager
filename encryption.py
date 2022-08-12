import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import secrets
import base64
import os.path
from manager import PasswordStore


class Encryption:
    def __init__(self, master_password):
        self.master_password = master_password
        self.filename = 'passwords.json'
    
    def generate_salt(length):
        with open('salt.salt', 'wb') as file:
            file.write(secrets.token_bytes(length))

    def derive_key(self):
        if not os.path.exists('salt.salt'):
            Encryption.generate_salt(16)
        salt = open('salt.salt', 'rb').read()
        kdf = Scrypt(salt=salt, length=32, n=2**20, r=8, p=1)
        return kdf.derive(self.master_password.encode())

    def generate_key(self):
        derived_key = Encryption.derive_key(self.master_password)
        return base64.urlsafe_b64encode(derived_key)

    def encrypt_file(self):
        key = Encryption.generate_key(self.master_password)
        f = Fernet(key)
        with open(self.filename, 'rb') as file:
            file_contents = file.read()
            file_encrypted = f.encrypt(file_contents)
        with open(self.filename, 'wb') as file:
            file.write(file_encrypted)

    def decrypt_file(self):
        key = Encryption.generate_key(self.master_password)
        f = Fernet(key)
        with open(self.filename, 'rb') as file:
            file_contents = file.read()
            try:
                file_decrypted = f.decrypt(file_contents)
            except cryptography.fernet.InvalidToken:
                print('Incorrect Password')
        with open(self.filename, 'wb') as file:
            file.write(file_decrypted)
