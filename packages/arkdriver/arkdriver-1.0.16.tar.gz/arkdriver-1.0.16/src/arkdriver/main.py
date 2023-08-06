from __future__ import annotations
import arkdriver
from arkdriver.presentation.presentation import main as presentation
from arkdriver.driver.application import Application
from arkdriver.driver.run import run
from nitrado import Global, initialize
from nitrado.games import ArkServer
from arkdriver.session.session import sign_in_dialogue
import requests
import os

URL = 'https://api.loadingproductions.com'
TEST_URL = 'http://127.0.0.1:5000'
TEST_CLOUD_URL = 'http://3.137.160.113'


def assert_nitrado_is_alive() -> None:
    health = Global.health_check()
    if not health.success:
        raise Exception("Unable to get a response from Nitrado")


def assert_api_is_alive(domain: str) -> None:
    response = requests.get(f"{domain}/main_control/ping")
    if not response.status_code == 200:
        raise Exception("Unable to get a response from Ark-API")
    if 'Content-Type' not in response.headers and response.headers['Content-Type'] != 'application/json':
        raise Exception("Unable to get a response from Ark-API")


def initialize_nitrado_api(domain: str) -> tuple[str, str]:
    nitrado_api_key, driver_token, gamertag = sign_in_dialogue(domain)
    initialize(nitrado_api_key, save=False)
    info = Global.token_info()
    if not info.valid:
        raise Exception("Nitrado API Token is not valid. You need to register the API key with LoadingProductions.")
    return driver_token, gamertag


def find_ark_server() -> ArkServer:
    gamertag = os.getenv('XBOX_GAMERTAG')
    print("\rPlease wait while the bot initializes.", end='')
    for ark in ArkServer.all():
        print(f"\rSearching for {gamertag} in {ark.query.server_name}...", end='')
        for player in ark.players():
            if player.name.lower() == gamertag.lower():
                print(f"\rFound {gamertag} in {ark.query.server_name}.                ")
                print()
                return ark
    raise Exception(f"Could not find {gamertag} in any of the servers.")


def dialogue(domain: str):
    driver_token, gamertag = initialize_nitrado_api(domain)

    commands_per_line = input("How many commands per line should the admin submit at once? Enter a number: ")
    while not commands_per_line.isnumeric():
        print("ERROR: You must input a number.")
        commands_per_line = input("How many commands per line should the admin submit at once? Enter a number: ")

    wait_time = input("How long should the admin wait before submitting another command sequence? Enter number in seconds: ")
    while not wait_time.isnumeric():
        print("ERROR: You must enter a number.")
        wait_time = input("How long should the admin wait before submitting another command sequence? Enter number in seconds: ")
    print()

    Application().open_ark()

    print("Sign into the server and create your character.")
    input("Press enter to continue...")
    print()

    ark = find_ark_server()

    print("Close any menu on the screen.",
          "\nCharacter must be spawned."
          "\nMake sure your character's inventory is closed.",
          "\nThe command prompt should not be open.",
          "\nWait until all cutscenes are over.",
          )
    input("Press enter to continue...\n")

    run(domain, driver_token, gamertag=gamertag, server=ark, interval=int(commands_per_line), wait=int(wait_time))


def main():
    print("[1] Run driver with official API")
    print("[2] Test driver with local API")
    print("[3] Test driver with cloud API")
    print("[4] Ragnarok Presentation")
    print("[0] To exit")
    response = input("What would you like to run? ")
    choices = ['0', '1', '2', '3', '4']
    while response not in choices:
        print(f"ERROR: your response should be a choice of: {choices}")
        print("[1] Run driver with official API")
        print("[2] Test driver with local API")
        print("[3] Test driver with cloud API")
        print("[4] Ragnarok Presentation")
        print("[0] To exit")
        response = input("What would you like to run? ")

    print()

    if response == '0':
        return

    if response == '1':
        assert_nitrado_is_alive()
        assert_api_is_alive(URL)
        dialogue(URL)
    elif response == '2':
        assert_nitrado_is_alive()
        assert_api_is_alive(TEST_URL)
        dialogue(TEST_URL)
    elif response == '3':
        assert_nitrado_is_alive()
        assert_api_is_alive(TEST_CLOUD_URL)
        dialogue(TEST_CLOUD_URL)
    elif response == '4':
        presentation()


if __name__ == "__main__":
    main()
