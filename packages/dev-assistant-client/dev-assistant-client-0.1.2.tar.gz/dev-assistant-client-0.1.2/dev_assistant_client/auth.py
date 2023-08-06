import getpass
import http.client
import json
import os
from colorama import Fore, Style
from dev_assistant_client.utils import TOKEN_FILE, USER_DATA, APP_URL, API_PATH
from dev_assistant_client.device import connect


def login(args):
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")

    payload = json.dumps({
        'email': email,
        'password': password,
    })

    headers = {
        'content-type': 'application/json',
        'accept': 'application/json'
    }

    conn = http.client.HTTPSConnection(APP_URL)
    conn.request("POST", API_PATH + '/login', body=payload, headers=headers)
    response = conn.getresponse()

    if response.status == 200:
        token = response.read().decode()
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        print(Fore.GREEN + "Logged in." + Style.RESET_ALL)

        headers = {
            'authorization': 'Bearer ' + token,
            'accept': 'application/json'
        }

        conn.request("GET", API_PATH + '/user', headers=headers)
        response = conn.getresponse()
        user = json.loads(response.read().decode())

        if 'name' in user:
            with open(USER_DATA, "w") as f:
                json.dump(user, f)
            print(Fore.GREEN + "Hello,", user['name'] + Style.RESET_ALL)

        connect()
    else:
        print(Fore.RED + "Failed to log in!" + Style.RESET_ALL)
        print("Error: ", response.read().decode())


def logout(args):
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token = f.readline()
        os.remove(TOKEN_FILE)

        headers = {
            'authorization': 'Bearer ' + token,
            'content-Type': 'application/json',
            'accept': 'application/json'
        }

        conn = http.client.HTTPSConnection(APP_URL)
        conn.request("POST", API_PATH + '/logout', headers=headers)
        response = conn.getresponse()

        if response.status == 200:
            if os.path.exists(USER_DATA):
                with open(USER_DATA, "r") as f:
                    user = json.load(f)
                print("See you soon,", user['name'])
                os.remove(USER_DATA)
            print("Logged out.")
