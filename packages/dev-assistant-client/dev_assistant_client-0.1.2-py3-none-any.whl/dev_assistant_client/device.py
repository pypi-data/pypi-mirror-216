import getpass
import http.client
import json
import platform
import socket
import time
import uuid
import re
from colorama import Fore, Style
import pusher
from dev_assistant_client.utils import TOKEN_FILE, APP_URL, API_PATH


def get_device_id():
    try:
        with open('device_id', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


DEVICE_ID = get_device_id()


def create_device_payload():
    return json.dumps({
        'id': DEVICE_ID or '',
        'name': socket.gethostname(),
        'type': 'desktop',
        'ip_address': socket.gethostbyname(socket.gethostname()),
        'mac_address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
        'os': platform.system(),
        'os_version': platform.release(),
        'architecture': platform.machine(),
        'python_version': platform.python_version(),
        'username': getpass.getuser(),
    }, indent=4)

def connect():
    with open(TOKEN_FILE, "r") as f:
        token = f.read()

    headers = {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    payload = create_device_payload()
    
    print("Connecting to the server...")
    # print(Fore.LIGHTGREEN_EX + payload + Style.RESET_ALL)

    conn = http.client.HTTPSConnection(APP_URL)
    conn.request("POST", API_PATH + '/devices/connect',
                 body=payload, headers=headers)
    response = conn.getresponse()

    if response.status == 200:
        print(Fore.LIGHTGREEN_EX + "Successfully connected!" + Style.RESET_ALL)
        print("Server response: ", response.read().decode())
    else:
        print(Fore.LIGHTRED_EX + "Failed to connect!" + Style.RESET_ALL)
        print("Response: ", response.read().decode())
        print("Status code: ", response.status)

def wsConnect():
    pusher_client = pusher.Pusher(
        app_id='1626464',
        key='5ed50462cadb0ee89c69',
        secret='6494511d80820ffe943a',
        cluster='sa1',
        ssl=True
    )

    def callback(data):
        print('Received event: ' + str(data))

    pusher_client.subscribe('my-channel')
    pusher_client.bind('my-event', callback)

    while True:
        time.sleep(1)  # Keep the program running.
