import os
from encryption import Encryption
from manager import PasswordStore

print("Welcome to the Encrypted Password Manager!")

# The existence of a saved salt file means the program has been run before
if not os.path.exists('salt.salt'):
    encryption = Encryption(input('Please input your master password, which will be used to decrypt your password vault: '))
else:
    encryption = Encryption(input('Enter your password to access your vault: '))

# Creating an instance of PasswordStore and loading the passwords into self.passwords
if os.path.exists('passwords.json'):
    encryption.decrypt_file()
passwords = PasswordStore('passwords.json')
passwords.load_passwords()

# Later in the programs' running each action begins with decrypting passwords.json, and to do that the file has to be firstly encrypted
encryption.encrypt_file()

while True:
    answer = input("""\nWhat do you want to do with the manager?\n
Type 1 if you want to add a new password
Type 2 if you want to delete a password
Type 3 if you want to see your whole vault
Type 4 if you want to see a specific password
Type q to quit the program: """)
    if answer == '1':
        encryption.decrypt_file()
        passwords.save_password()
        encryption.encrypt_file()
    elif answer == '2':
        encryption.decrypt_file()
        passwords.delete_password()
        encryption.encrypt_file()
    elif answer == '3':
        encryption.decrypt_file()
        passwords.show_all_passwords()
        encryption.encrypt_file()
    elif answer == '4':
        encryption.decrypt_file()
        passwords.show_specific_password()
        encryption.encrypt_file()
    elif answer == 'q':
        break
    else:
        print('\nIncorrect action, choose one from the list please')
