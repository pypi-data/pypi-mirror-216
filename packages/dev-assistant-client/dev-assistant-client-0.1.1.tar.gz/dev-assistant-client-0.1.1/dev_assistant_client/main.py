import socket
import os
import getpass
import requests
import argparse
import json

API_URL = 'https://devassistant.tonet.dev/api/'
TOKEN_FILE = os.path.expanduser("~/.dev_assistant_token")
USER_DATA = os.path.expanduser("~/.dev_assistant_user")


def main(args=None):
    parser = argparse.ArgumentParser(prog='dev-assistant')
    subparsers = parser.add_subparsers()

    # Use 'start' as an alias for the main command
    parser_main = subparsers.add_parser('start')
    parser_main.set_defaults(func=start)

    parser_logout = subparsers.add_parser('logout')
    parser_logout.set_defaults(func=logout)

    args = parser.parse_args(args)

    if 'func' in args:
        args.func(args)
    else:
        start(args)


def start(args):
    if not os.path.exists(TOKEN_FILE):
        login(args)
    else:
        connect()


def connect():
    with open(TOKEN_FILE, "r") as f:
        token = f.read()

    headers = {
        'Authorization': 'Bearer ' + token,
    }

    # Se a API_URL do seu servidor Laravel contém ".test", você pode desativar a verificação SSL
    verify = False if ".test" in API_URL else True

    try:
        # Enviar uma solicitação GET para o servidor
        response = requests.get(API_URL, headers=headers,
                                verify=verify, timeout=5)

        # Verificar se a solicitação foi bem-sucedida
        if response.status_code == 200:
            print("Successfully connected to the server.")
            print("Server response:", response.text)
        else:
            print("Failed to connect to the server.")
            print("Status code:", response.status_code)

    except requests.exceptions.RequestException as e:
        # Se ocorrer um erro de rede, imprimir uma mensagem de erro
        print("An error occurred:", e)


def login(args):
    email = input("E-mail: ")
    password = getpass.getpass("Password: ")

    response = requests.post(API_URL + 'login', data={
        'email': email,
        'password': password,
        'device_name': socket.gethostname()
    })

    if response.status_code == 200:
        with open(TOKEN_FILE, "w") as f:
            f.write(response.text)
        print("Logged in.")
        # Get the user's details and print greetings message
        response = requests.get(API_URL + 'user', headers={
            'Authorization': 'Bearer ' + response.text,
        })
        response = response.json()
        if 'name' in response:
            with open(USER_DATA, "w") as f:
                json.dump(response, f)
            print("Hello,", response['name'])
        connect()
    else:
        print("Failed to log in.")


def logout(args):
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    if os.path.exists(USER_DATA):
        with open(USER_DATA, "r") as f:
            user = json.load(f)
        print("See you soon,", user['name'])
        os.remove(USER_DATA)
    print("Logged out.")
