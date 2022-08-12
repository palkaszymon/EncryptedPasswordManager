import os
from encryption import Encryption
from manager import PasswordStore
import json


passwords = PasswordStore('passwords.json')

print("Welcome to the Encrypted Password Manager!")

if not os.path.exists('salt.salt'):
    encryption = Encryption(input('Please input your master password, which will be used to decrypt your password vault: '))
    key = encryption.generate_key()
else:
    encryption = Encryption(input('Enter your password to access your vault: '))

while True:
    answer = input("""What do you want to do with the manager?
Type 1 if you want to add a new password
Type 2 if you want to delete a password
Type 3 if you want to see your whole vault
Type 4 if you want to see a specific password
Type q to quit the program: """)
    if answer == '1':
        passwords.save_password()
    elif answer == '2':
        passwords.delete_password()
    elif answer == '3':
        passwords.show_all_passwords()
    elif answer == '4':
        passwords.show_specific_password()
    elif answer == 'q':
        break
