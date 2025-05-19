import requests
import re
import json
import os
import jwt
import argparse
import sys

from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

"""
Installation of some packages may be necessary :
* pip install requests beautifulsoup4 pyjwt
"""

# -----

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# -----

def load_credentials(file_path):
    """
    Loads variables from a credentials file
    :param file_path: Path to the credentials file
    :return: A dictionary containing the key variables
    """
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                credentials[key] = value.strip(' "')
    return credentials

# -----

def get_json_field(data, key_path):
    """
    Extracts a value from a nested JSON dictionary with a path like 'user.id' or 'user.roles[0]'.
    :param data: dict - JSON data as a Python dictionary.
    :param key_path: str - Path of dot-separated keys, with support for list indexes[i].
    :return: The extracted value or None if not found.
    """
    try:
        current = data
        for part in key_path.split('.'):
            match = re.match(r'^(\w+)(\[(\d+)\])?$', part)
            if not match:
                return None
            key = match.group(1)
            index = match.group(3)
            current = current[key]
            if index is not None:
                current = current[int(index)]
        return current
    except (KeyError, IndexError, TypeError):
        return None

# -----

def get_session():
    # Creates a Session to manage cookies, headers, persistent connections
    session = requests.Session()
    
    # Simulates Google Chrome via User-Agent
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": 'gzip, deflate, br',
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://example.com"
    })
    return session

# -----

def get_auth_code(pars, debug=0):
    # Creates a Session to manage cookies, headers, persistent connections
    session = get_session()

    # Build the initial query
    initial_url = pars['oauth2_url']+"/authorize?response_type=code&client_id="+pars['client_id']+"&redirect_uri="+pars['redirect_uri']+"&scope="+pars['scope']
    if debug:
        eprint(f"Initial URL : {initial_url}")
    
    # Makes a GET request to the initial URL
    response = session.get(initial_url, allow_redirects=False)
    response.raise_for_status()  # Ensures the response is 200 OK
    
    # Parses the response to find <form> and extract 'url' and 'token'
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find('form', {'id': 'lform'})
    
    if not form:
        raise ValueError("No <form> found in the page.")
    
    # Extracts the 'url' and 'token' fields
    token_input = form.find('input', {'name': 'token'})
    url_input = form.find('input', {'name': 'url'})
    timezone_input = form.find('input', {'name': 'timezone'})
    skin_input = form.find('input', {'name': 'skin'})
    
    if not token_input:
        raise ValueError("The 'token' field was not found in the form.")
    
    token_value = token_input.get('value')
    url_value = url_input.get('value')
    skin_value = skin_input.get('value')
    timezone_value = "2"
    
    # Prepares the form data to be submitted
    form_data = {
        'token': token_value,
        'url': url_value,
        'skin': skin_value,
        'timezone': timezone_value,
        'user': pars['user'],
        'password': pars['password']
    }
    
    # Submits the request in POST mode
    post_response = session.post(pars['oauth2_url']+'/authorize', data=form_data, allow_redirects=False)
    post_response.raise_for_status()
    
    # Retrieves the 'Location' field in the headers
    location_url = post_response.headers.get('Location')
    
    if not location_url:
        raise ValueError("The 'Location' field was not found in the response.")
    
    if debug:
        eprint(f"Redirection vers : {location_url}")
    
    # Extracts query parameters as a dict
    parsed_url = urlparse(location_url)
    query_params = parse_qs(parsed_url.query)
    
    # Retrieves the value of the 'code' parameter
    code_value = query_params.get('code', [None])[0]
    if not code_value:
        raise ValueError("Parameter 'code' not found in URL.")
    if debug:
        eprint(f"Code = {code_value}")
    return code_value

# -----

def get_token(pars, code, debug=0):
    # Creates a Session to manage cookies, headers, persistent connections
    session = get_session()

    # Prepares the form data to be submitted
    form_data = {
        'grant_type': 'authorization_code',
        'redirect_uri': pars['redirect_uri'],
        'client_id': pars['client_id'],
        'client_secret': pars['client_secret'],
        'code': code
    }

    # Submits the request in POST mode
    post_response = session.post(pars['oauth2_url']+'/token', data=form_data, allow_redirects=True)
    post_response.raise_for_status()

    token = post_response.json()
    if debug:
        eprint(json.dumps(token, indent=4, ensure_ascii=False))
    return token

# -----

def get_payload(pars, id_token, debug=0):
    # Decode the JWT and get its payload
    payload = jwt.decode(id_token, options={"verify_signature": False})  # Ignorer la signature
    if debug:
        eprint(json.dumps(payload, indent=4, ensure_ascii=False))
    return payload

# -----

# Function to make a GET request with Bearer authorization
def get_data_with_bearer(url, bearer_token, debug=0):
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "API-KEY": "XX" # Required for API calls
    }

    # Performs the GET request with Bearer authorization
    response = requests.get(url, headers=headers)

    # Check the response and return the data
    content=None
    if response.status_code == 200:
        content=response.json()
        if debug:
            eprint(json.dumps(content, indent=4, ensure_ascii=False))
    return content

# -----

def api_maggot(pars, api_url, debug):
    # Generates an authentication code
    code_value = get_auth_code(pars, debug)

    # Collects the token
    token = get_token(pars, code_value, debug)

    # Makes the API request with the Token
    id_token = get_json_field(token, "id_token")
    return get_data_with_bearer(api_url, id_token, debug=0)

# -----

def main():
    # Definition of arguments
    parser = argparse.ArgumentParser(description="Get a token to make API calls via the SSO layer")
    parser.add_argument('--file', type=str, help='Crendentials file', required=True)
    parser.add_argument('--debug', action='store_true', help='Enables debug mode')
    args = parser.parse_args()

    # Debug indicator
    debug = 0
    if args.debug:
        debug = 1

    if args.file:
        credentials = load_credentials(args.file)
        # Authentication Portal Settings
        pars = {
            'oauth2_url': credentials.get('OAUTH2'),
            'redirect_uri': credentials.get('REDIRECT'),
            'scope': credentials.get('SCOPE'),
            'client_id': credentials.get('CLIENT_ID'),
            'client_secret': credentials.get('CLIENT_SECRET'),
            'user': credentials.get('USERNAME'),
            'password': credentials.get('PASSWORD')
        }

        # Generates an authentication code
        code_value = get_auth_code(pars, debug)

        # Collects the token
        token = get_token(pars, code_value, debug)

        # Makes the API request with the Token
        id_token = get_json_field(token, "id_token")
        print(id_token)

if __name__ == "__main__":
    main()
