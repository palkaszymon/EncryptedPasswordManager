import string
import random
import json
import os

class PasswordStore:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def load_passwords(self):
        with open(self.filename , 'r') as f:
            try:
                self.passwords = json.load(f)
            except json.decoder.JSONDecodeError:
                self.passwords = []

    def generate_password(self):
        password = []
        numbers = string.digits
        letters_lower = string.ascii_lowercase
        letters_upper = string.ascii_uppercase
        symbols = '!@#$%^&*'
        length = int(input("Enter the password's length (at least 8 is recommended): "))
        all_characters = numbers + letters_lower + letters_upper + symbols
        for i in range(length):
            password.append(random.choice(all_characters))
        return ''.join(password)

    def save_password(self):
        username = input('\nWhat is the username?: ')
        if input("If you want to generate a strong password type 'y', otherwise type 'n': ") == 'y':
            password = self.generate_password()
        else:
            password = input("Please enter the password you want to save: ")
        name = input('How do you want to name the username/password combination?: ')
        password_dict = {
            'name' : name,
            'username' : username,
            'password' : password,
        }
        self.passwords.append(password_dict)
        with open(self.filename, 'w') as f:
            json.dump(self.passwords, f)
        print(f'Password {name} saved!\n')

    def delete_password(self):
        names_list = [password['name'] for password in self.passwords]
        print(f'\nCurrently saved passwords: {names_list}\n')
        pwd_to_delete = input('Enter the name of the password to delete: ')
        for password in self.passwords:
            if password['name'] == pwd_to_delete:
                self.passwords.remove(password)
        with open(self.filename, 'w') as f:
            json.dump(self.passwords, f)
        print(f'Password {pwd_to_delete} deleted!\n')

    def show_all_passwords(self):
        for password in self.passwords: 
            print(password)

    def show_specific_password(self):
        pwd_to_show = input('\nEnter the name of the password: ')
        for password in self.passwords:
            if password['name'] == pwd_to_show:
                print(password)
