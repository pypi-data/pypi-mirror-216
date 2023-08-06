import os
from nitrado.games import ArkServer
from arkdriver.driver.driver import Driver
from arklibrary.admin.admin import Admin
from time import sleep
import requests
from requests import Response
from datetime import datetime


def get_new_commands(domain: str, server: ArkServer, driver_token: str) -> list:
    count = 0
    while count < 10:
        try:
            server_name = server.query.server_name.replace("\r", "").replace("\n", "")
            json = {'driver_token': driver_token}
            if server_name:
                json['server_name'] = server_name
            headers = {'mime': 'application/json'}
            data = requests.post(f"{domain}/command_control/queued", json=json, headers=headers).json()
            return data["commands"]
        except Exception as e:
            print(f"[Error]: {str(e)}")
        count += 1
    raise Exception("Unable to get a response from the server: get_new_commands")


def set_commands_as_executed(domain: str, commands: list, driver_token: str, server: ArkServer) -> None:
    count = 0
    while count < 10:
        try:
            json = {
                'commands': commands,
                'driver_token': driver_token,
            }
            headers = {'mime': 'application/json'}
            response = requests.patch(f'{domain}/command_control/bulk', json=json, headers=headers)
            if response.status_code == 200:
                return response.json()
            for command in commands:
                print(command)
            print(f"[Error]: failed to update commands, status_code was {response.status_code}\n")
            print(f"[Response]: {response.text}\n")
        except Exception as e:
            print(f"[Error]: {str(e)}")
        count += 1
    raise Exception("Unable to get a response from the server: set_commands_as_executed")


def fetch_commands(url: str, server: ArkServer, driver_token:str, interval=10, wait=5):
    while True:
        commands = []
        try:
            commands = get_new_commands(url, server, driver_token)
        except:
            print(f"\r[Error] Request to api crashed.")
        if len(commands) == 0:
            print(f"\rWaiting for new commands to be created...", end='')
            sleep(wait)
            continue
        print()
        i = 0
        while i < len(commands):
            print(f"DATA[{i}: {min(i+interval, len(commands))}]:")
            for command in commands[i:i+interval]:
                name = None
                server_name = command['server_name']
                service_id = str(command['service_id'])
                code = command['code']
                if service_id:
                    name = service_id
                if server_name:
                    name = server_name
                    if len(server_name) > 30:
                        name = f"{server_name[:27]}..."
                print(f"\t{name:>30} {'->':^6} {code:<500}")
            yield commands[i:i+interval]
            i += interval


def run(url: str, driver_token: str, gamertag: str = None, server: ArkServer = None, interval: int = 10, wait: int = 5):
    driver = Driver()
    admin = Admin(driver=driver)
    if server.admin_password:
        admin.enable_cheats(server.admin_password)
    if server.server_password:
        admin.enable_cheats(server.server_password)
    if server.current_admin_password:
        admin.enable_cheats(server.current_admin_password)
    admin.gcm().enemy_ignores_me()
    admin.execute()
    for commands in fetch_commands(url, server, driver_token, interval=interval, wait=wait):
        for command in commands:
            admin.command_list.append(command['code'])
            command['executed'] = True
            command['admin_gamertag'] = gamertag
            command['server_name'] = server.query.server_name.replace("\r", "").replace("\n", "")
            command['service_id'] = str(server.service_id)
            command['executed_at'] = str(datetime.now())
        admin.execute()
        set_commands_as_executed(url, commands, driver_token, server)

