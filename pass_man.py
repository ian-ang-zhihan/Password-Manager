import json
import random
from cryptography.fernet import Fernet

# -----------

# Generate a key to later be used to decrypt
"""
def write_key():
    key = Fernet.generate_key()
    with open('pass_key.key', 'wb') as pass_key:
        pass_key.write(key)


write_key()
"""
# Once a key is generated, DON'T use this function

# -----------


def load_key():
    with open('pass_key.key', 'rb') as pass_key:
        key = pass_key.readline()

    return key


def auth():
    attempts = 2
    while True:
        master_password = input('Master Password: ')
        if master_password == '123':  # <-- Enter your master password here
            break
        else:
            if attempts == 0:
                print('You have exceeded 3 tries...')
                quit()
            else:
                print('Incorrect Password...')
                attempts -= 1
                continue


def generate_password():
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~`!@#$%^&*()_-+={[}]|\:;<>?/'
    length = int(
        input('How many characters would you like your password to be?: '))
    generated_password = ''
    for i in range(length):
        generated_password += random.choice(characters)
    return generated_password


def add():
    with open('data.json', 'r') as f:
        json_data = json.loads(f.read())

    id = 0
    for object in json_data['data']:
        if object:
            id = object['ID']

    app = input('What app is this for?: ')
    email = input('Please enter the email: ')
    username = input('Please enter the username: ')

    generate_or_nah = input(
        'Would you like to generate the password? [y/n]: ').lower()
    if generate_or_nah == 'y':
        pwd = generate_password()
        print('Generated Password: ', pwd)
    else:
        pwd = input('Please enter the password: ')

    notes = []
    have_notes = input(
        'Do you have additional notes to write? [y/n]: ').lower()

    if have_notes == 'y':
        have_note = True
        while have_note:
            note = input('Please add a note [endtask(e)]: ')
            if note == 'e':
                break
            elif note == '':
                print('Note cannot be an empty string')
                continue
            else:
                notes.append(note)

    data = {
        "ID": id + 1,
        "App": app,
        "Email": email,
        "Username": username,
        "Password": fer.encrypt(pwd.encode()).decode(),
        "Notes": notes
    }

    json_data['data'].append(data)

    with open('data.json', 'w') as f:
        f.write(json.dumps(json_data, indent=1))


def view():
    with open('data.json', 'r') as f:
        json_data = json.loads(f.read())

    for data in json_data['data']:
        print('ID: ', data['ID'])
        print('App: ', data['App'])
        print('Email: ', data['Email'])
        print('Username: ', data['Username'])

        pwd = data['Password']
        pwd = fer.decrypt(pwd.encode()).decode()
        data['Password'] = pwd
        print('Password: ', data['Password'])

        print('Notes: ', data['Notes'])
        print()


def edit():
    while True:
        object_id = input('What is the object ID? [endtask(e)]: ')

        if object_id.lower() != 'e' and object_id.isdigit() == False:
            print('Invalid ID...')
            continue

        if object_id.lower() == 'e':
            break

        with open('data.json', 'r') as f:
            json_data = json.loads(f.read())

        # Checks if ID is valid
        ids = set()
        for i in range(len(json_data['data'])):
            ids.add(json_data['data'][i]['ID'])

        if int(object_id) not in ids:
            print('Error 404: ID Not Found...')
            continue

        for object in json_data['data']:
            if object["ID"] == int(object_id):
                while True:
                    print()
                    print(object)

                    field = input(
                        'Which field would you like to change [endtask(e)]: ')

                    if field not in ['App', 'Email', 'Username', 'Password', 'Notes', 'e']:
                        print('Invalid Field...')
                        continue

                    if field.lower() == 'e':
                        break

                    elif field == 'Notes':
                        pop_or_append = input(
                            "Do you want to add or remove('remove' removes the most recent data added) to Notes? [remove(r) | add(a)]: ").lower()
                        if len(object[field]) == 0 and pop_or_append == 'r':
                            print('No notes to remove...')
                            continue
                        else:
                            if pop_or_append == 'r':
                                object[field].pop()
                                print('Note Removed Successfully...')
                                continue
                            else:
                                new_data = input('New Data: ')
                                object[field].append(new_data)
                                print('Note Added Successfully...')
                                continue

                    elif field == 'Password':
                        new_data = input('New Data: ')
                        object[field] = fer.encrypt(new_data.encode()).decode()
                        print('Password Successfully Updated...')
                        continue

                    else:
                        new_data = input('New Data: ')
                        object[field] = new_data
                        print(f'{field} Updated Successfully...')
                        continue

                updated_data = {
                    "ID": object['ID'],
                    "App": object['App'],
                    "Email": object['Email'],
                    "Username": object['Username'],
                    "Password": object['Password'],
                    "Notes": object['Notes']
                }

                object = updated_data

        with open('data.json', 'w') as f:
            f.write(json.dumps(json_data, indent=1))


def delete():

    while True:
        object_id = input('What is the object ID? [endtask(e)]: ')

        if object_id.lower() != 'e' and object_id.isdigit() == False:
            print('Invalid ID...')
            continue

        if object_id.lower() == 'e':
            break

        with open('data.json', 'r') as f:
            json_data = json.loads(f.read())

        # Checks if ID is valid
        ids = set()
        for i in range(len(json_data['data'])):
            ids.add(json_data['data'][i]['ID'])

        if int(object_id) not in ids:
            print('Error 404: ID Not Found...')
            continue

        # Deletes object
        for i in range(len(json_data['data'])):
            if json_data['data'][i]['ID'] == int(object_id):
                del json_data['data'][i]
                break

        # Updates IDs that do not increment in order
        for i in range(len(json_data['data']) - 1):
            if json_data['data'][0]['ID'] != 1:
                json_data['data'][0]['ID'] = 1
                json_data['data'][1]['ID'] = 2
            else:
                json_data['data'][i+1]['ID'] = json_data['data'][i]['ID'] + 1

        with open('data.json', 'w') as f:
            f.write(json.dumps(json_data, indent=1))
            print('Data Deleted Successfully...')


# -----------

key = load_key()
fer = Fernet(key)

auth()

while True:
    mode = input(
        'Choose a mode... [view(v) | add(a) | edit(e) | delete(d) | quit(q)]: ').lower()
    if mode == 'v':
        view()
    elif mode == 'a':
        add()
    elif mode == 'e':
        edit()
    elif mode == 'd':
        delete()
    elif mode == 'q':
        break
    else:
        print('Invalid Mode...')
        continue
