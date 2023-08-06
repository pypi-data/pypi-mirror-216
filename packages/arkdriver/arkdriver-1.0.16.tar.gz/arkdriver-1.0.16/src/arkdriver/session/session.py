import requests
import os
import webbrowser
import secrets
from time import sleep
import tempfile
from io import BytesIO


def authenticate(domain: str, security_token: str, timeout=60) -> dict:
    """Returns the driver token and gamertag"""
    data = {'security_token': security_token}
    seconds_wait = 5
    print("Waiting for authentication response...", end='')
    for i in range(timeout // seconds_wait):
        response = requests.post(f"{domain}/session_control/driver_token", data=data)
        if response.status_code == 200 and 'driver_token' in response.json():
            print()
            print("Successfully Signed In.")
            print()
            return response.json()
        sleep(seconds_wait)
        print(".", end='')
    print()
    raise Exception(f"Timeout exhausted, failed to authenticate.")


def nitrado_api_token(domain: str, driver_token: str) -> str:
    """Returns the nitrado api token"""
    data = {'driver_token': driver_token}
    response = requests.post(f"{domain}/session_control/nitrado_api_token", data=data)
    if response.status_code != 200:
        raise Exception(f"[{response.status_code}] Failed to authenticate:", response.text)
    elif 'nitrado_api_token' not in response.json() or response.json()['nitrado_api_token'] is None:
        raise Exception(f"Could not get your nitrado api token:", response.text)
    return response.json()['nitrado_api_token']


def sign_in_dialogue(domain: str) -> tuple[str, str, str]:
    """Returns the nitrado api token"""
    security_token = secrets.token_urlsafe(64)
    webbrowser.open_new(f"{domain}/driver_control/{security_token}")
    data = authenticate(domain, security_token)
    driver_token = data['driver_token']
    os.environ['XBOX_GAMERTAG'] = data['gamertag'].lower()
    nitrado_api_key = nitrado_api_token(domain, driver_token)
    return nitrado_api_key, driver_token, driver_token
