import os
import getpass
from dotenv import find_dotenv, load_dotenv
from . import json_quickbase, xml_quickbase
from .qb_errors import QBError

def get_client(json_sdk=False, creds=None, **kwargs):
    if creds:
        url = creds.get('QB_URL')
        user_token = creds.get('QB_USERTOKEN')
        username = creds.get('QB_USERNAME')
        password = creds.get('QB_PASSWORD')
    else:
        load_dotenv(find_dotenv(usecwd=True))
        url = os.environ.get('QB_URL')
        user_token = os.environ.get('QB_USER_TOKEN')
        username = os.environ.get('QB_USERNAME')
        password = os.environ.get('QB_PASSWORD')

        if not url and not user_token and not username and not password:
            raise QBError('No credentials found, your .env file may be missing or in the wrong directory.')
            

    if json_sdk:
        new_qb_client = json_quickbase.JsonQuickbaseClient(
            # realmhost=realmhost, base_url=url, user_token=user_token)
            credentials={'base_url': url, 'user_token': user_token}, **kwargs)
        return new_qb_client
    else:
        qb_client = xml_quickbase.XmlQuickbaseClient(hours=25,
            credentials={'username': username, 'password': password, 'base_url': url}, **kwargs
                # username, password, base_url=url, hours=25
        )
        return qb_client
    
def get_json_client(creds=None, **kwargs):
    return get_client(True, creds, **kwargs)

def get_xml_client(creds=None, **kwargs):
    return get_client(False, creds, **kwargs)
       

def set_qb_info():
    
    path = os.path.join(os.getcwd())
    input_path = input('Enter path to .env file (or leave blank for your cwd): ')
    path = os.path.join(input_path if input_path else path, '.env')
    QB_URL = input('Quickbase URL (include https): ')
    QB_USER_TOKEN = input('User Token: ')
    QB_USERNAME = input('Username: ')
    QB_PASSWORD = getpass.getpass()
    with open(path, "w") as env:
        env.write(f'QB_URL="{QB_URL}"\n')
        env.write(f'QB_USER_TOKEN="{QB_USER_TOKEN}"\n')
        env.write(f'QB_USERNAME="{QB_USERNAME}"\n')
        env.write(f'QB_PASSWORD="{QB_PASSWORD}"')

    print(f'Credentials saved to {path}')