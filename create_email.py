import json
import requests
from requests.auth import HTTPBasicAuth

def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

def create_email_account(domain, email_name, email_password, email_password2, da_user, da_api_key, da_host):
    create_url = f"https://{da_host}:2222/CMD_API_EMAIL_POP"

    create_params = {
        'action': 'create',
        'domain': domain,
        'user': email_name,
        'passwd': email_password,
        'passwd2': email_password2,  # Confirm password
        'quota': 0,  # Set to 0 for unlimited quota
        'limit': 7200,  # Set to 0 for unlimited send/receive limit
    }

    response = requests.post(create_url, data=create_params, auth=HTTPBasicAuth(da_user, da_api_key))

    if response.status_code == 200:
        parsed_response = response.text
        if "error=0" in parsed_response:
            print(f"Successfully created email account: {email_name}@{domain}")
        else:
            print(f"Failed to create email account: {email_name}@{domain}. Message: {parsed_response}")
    else:
        print(f"Failed to create email account: {email_name}@{domain}. Status Code: {response.status_code}. Message: {response.text}")

if __name__ == "__main__":
    config = load_config('config.json')
    
    domain = input("Enter the domain: ")
    email_name = input("Enter the name for the email address: ")
    email_password = input("Enter the password for the email address: ")
    email_password2 = input("Enter the password again: ")

    create_email_account(domain, email_name, email_password, email_password2, config['da_user'], config['da_api_key'], config['da_host'])
