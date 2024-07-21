import json
import requests
from requests.auth import HTTPBasicAuth
import urllib.parse

def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

def create_alias(domain, base_name, num_aliases, forward_to, da_user, da_api_key, da_host):
    create_url = f"https://{da_host}:2222/CMD_API_EMAIL_FORWARDERS"

    aliases = []
    if num_aliases == 1:
        aliases.append(base_name)
    else:
        for i in range(1, num_aliases + 1):
            aliases.append(f"{base_name}{i}")

    for alias in aliases:
        create_params = {
            'action': 'create',
            'domain': domain,
            'user': alias,
            'email': forward_to,
        }

        response = requests.get(create_url, params=create_params, auth=HTTPBasicAuth(da_user, da_api_key))

        if response.status_code == 200:
            # Parse the response
            parsed_response = urllib.parse.parse_qs(response.text)
            if parsed_response.get('error', ['1'])[0] == '0':
                print(f"Successfully created alias: {alias}@{domain} forwarding to {forward_to}")
            else:
                error_details = parsed_response.get('details', ['Unknown error'])[0]
                print(f"Failed to create alias: {alias}@{domain}. Details: {error_details}")
        else:
            print(f"Failed to create alias: {alias}@{domain}. Status Code: {response.status_code}. Message: {response.text}")

if __name__ == "__main__":
    config = load_config('config.json')
    
    domain = input("Enter the domain: ")
    base_name = input("Enter the base name for the aliases: ")
    num_aliases = int(input("Enter the number of aliases to create: "))
    forward_to = input("Enter the email address to forward to: ")

    create_alias(domain, base_name, num_aliases, forward_to, config['da_user'], config['da_api_key'], config['da_host'])
