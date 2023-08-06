import argparse
import os
from dotenv import load_dotenv
from colorama import Fore, Style
from dev_assistant_client.auth import login, logout
from dev_assistant_client.utils import APP_URL, TOKEN_FILE
from dev_assistant_client.device import connect, wsConnect

import pkg_resources

# Get the version of the current package
package_version = pkg_resources.get_distribution(
    "dev-assistant-client").version

print(Fore.LIGHTGREEN_EX + 
'''
    .-----.   Dev Assistant
    | >_< |   ''' + Fore.YELLOW + 'v' + package_version + Fore.LIGHTGREEN_EX + ''' 
    '-----'   ''' + Fore.YELLOW + 'https://' + (APP_URL or 'devassistant.tonet.dev') + Fore.LIGHTGREEN_EX + '''
''' 
+ Style.RESET_ALL)

load_dotenv()


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
        wsConnect()
