## Authentication portal via API

### Purpose

* Access to resources provided by the Web API using a Web Token obtained from the Authentication Portal.

* Depending on the Identity Provider we choose, i.e either Keycloak or LemonLDAP::NG (e.g INRAE portal), we have to proceed in a different way.

<br><br>

### 1 - Identity Provider managed by keycloak

* We use the service accounts defined by keycloak, i.e. non-interactive accounts with a client_id / client_secret that can obtain a token without user authentication (via client_credentials grant). In this way, we don't need to specify a username with his password.

* A file containing the credentials must be configured with the correct URL and client credentials. Information regarding the corresponding client must be identical in the nginx file (in our example, **_[nginx_ssl.conf](../nginx/nginx_ssl.conf)_**). See [this]( https://github.com/djacob65/maggot-sso/wiki/Single-Sign-On#2---access-to-resources-provided-by-the-web-api-using-a-web-token) for more details.

    ```
    # Authentication portal managed by Keycloak
    OAUTH2=https://mydomain.fr:8443/realms/Maggot/.well-known/openid-configuration

    # Keycloak API-dedicated client
    CLIENT_ID=<client_id>
    CLIENT_SECRET=<client_secret>
    ```

* Here is a simple bash script using [cURL](https://en.wikipedia.org/wiki/CURL) and [./jq](https://jqlang.github.io/jq/download/)

    ```bash
    #!/bin/bash

    # Get credentials (client ID, secret code)
    . .secret/keycloak-credentials

    # Maggot API URL
    API_URL="https://mydomain.fr/maggot/api"
    
    # Default Dataset and Format
    DATASET=frim1
    FORMAT=maggot
    
    # Input arguments, if any
    [ $# -gt 0 ] && DATASET=$1
    [ $# -gt 1 ] && FORMAT=$2
    
    # Get Access Token
    JSON=$(curl -s X POST -H 'Accept: application/json' \
          -d "client_id=$CLIENT_ID" -d "client_secret=$CLIENT_SECRET" \
          -d 'grant_type=client_credentials' $OAUTH2/token)
    echo $JSON | jq 1>&2
    
    # Get the token to make API calls via the SSO layer
    TOKEN=$(echo $JSON | jq -r '.access_token')
    
    # Decode the payload (optional)
    echo $TOKEN | sed -e "s/\./\n/g" | head -2 | tail -1 | base64 --decode 2>/dev/null | jq 1>&2
    
    # Alias CURL_API
    alias CURL_API="curl -s -H 'accept: application/json' -H 'API-KEY: XX' -H \"Authorization: Bearer $TOKEN\" -X GET"
    
    # Make API calls via the SSO layer
    CURL_API  $API_URL/$DATASET/$FORMAT | jq
    ```

* See the example with its outputs : [API-Service-account](https://github.com/djacob65/maggot-sso/blob/main/api/API_Service-account.md)

<br><br>

### 2 - Identity Provider managed by LemonLDAP::NG

* Example with the pre-production INRAE Authentication Portal (INRAE Portal for short). See the [SSO and INRAE Portal](https://github.com/djacob65/maggot-sso/wiki/SSO-and-INRAE-Portal#2---inrae-portal-preproduction-as-a-unique-identity-provider)  section. 

* A script written in python (_sso_oidc_tools.py_) implements the complete workflow simulating authentication as if it had been established via a web browser. It provides a web token which then allows you to call the API while being authenticated. Installation of some packages may be necessary as _requests_, _beautifulsoup4_ and _pyjwt_.

* A file containing the credentials must be configured with the correct URLs and credentials. This information was provided to you by the identity provider administrator. Information regarding the corresponding client must be identical in the nginx file (in our example, **_[nginx_ssl_inrae.conf](../nginx/nginx_ssl_inrae.conf)_**). Unfortunately, the INRAE portal managed by LemonLDAP does not support service accounts like Keycloak. We will therefore need to specify a user's credentials.

    
    ```
    # Authentication portal
    OAUTH2=https://authentification.preproduction.inrae.fr/oauth2
    REDIRECT=https://mydomain.fr/maggot/redirect_uri
    SCOPE=openid+profile+email+supannEntiteAffectation
    
    # Client
    CLIENT_ID=<client_id>
    CLIENT_SECRET=<client_secret>
    
    # User
    USERNAME=<username>
    PASSWORD=<password>
    ```


* Using Python Script on Command Line

    ```bash
    $ python ./sso_oidc_tools.py -h
    usage: sso_oidc_tools.py [-h] --file FILE [--debug]
    
    Get a token to make API calls via the SSO layer
    
    options:
      -h, --help   show this help message and exit
      --file FILE  Crendentials file
      --debug      Enables debug mode

    $ python ./sso_oidc_tools.py --file .secret/inrae-credentials --debug
    Initial URL : https://authentification.preproduction.inrae.fr/oauth2/authorize?response_type=code&client_id=MAGGOT-TEST-WAPNMR&redirect_uri=https://mydomain.fr/maggot/redirect_uri&scope=openid+profile+email+supannEntiteAffectation
    Redirection vers : https://mydomain.fr/maggot/redirect_uri?session_state=T%2Fik97%2BdwIJkYXqQptqSDvRChYr5evvOHJoH4YKx%2FDg%3D.cDQzaG1rREw4L0J5QXE2U0xNTVpTckJ1N2k4anJuZzFyNXpCWVl2N0Rnd284dFV0eGp0WnVobmRJeVl0QlZnakQvMHRQa1lYNnVBdkE2UE5UME9JSG9zeU16Q0x3dnlYVWR5dmp4aGQyRms9&code=2215cf0cda2b6a304335ec7cb82c4bf2a93132789e46c586107126d9ede32aec
    Code = 2215cf0cda2b6a304335ec7cb82c4bf2a93132789e46c586107126d9ede32aec
    {
        "expires_in": 3600,
        "id_token": "eyJraWQiOiJncGpYSHArZFNrdTJ3V2pWeGh0U2tBIiwiYWxnIjoiUlMyNTYifQ.eyJzaWQiOiJWazdtdVpmN0xWRHgvMUNkUkVjM3R1TUx1Z0FTV2M4UWJ6K3RMazNRUm1ZIiwiYWNyIjoiZWlkYXMxIiwiZXhwIjoxNzQ3NTYxMDAzLCJpc3MiOiJodHRwczovL2F1dGhlbnRpZmljYXRpb24ucHJlcHJvZHVjdGlvbi5pbnJhZS5mci8iLCJhdXRoX3RpbWUiOjE3NDc1NTc0MDIsInN1YiI6ImRqYWNvYiIsImlhdCI6MTc0NzU1NzQwMywiYXpwIjoiTUFHR09ULVRFU1QtV0FQTk1SIiwiYXRfaGFzaCI6IjhiRklEREdVcWVtN2RmMXd5dThrZEEiLCJhdWQiOlsiTUFHR09ULVRFU1QtV0FQTk1SIl19.bXv2mSN96FCgm4OujDpLOeYq703Xvi22F3mhw4F3ezu9Zj0bp0bd5cUIuf-A8wocdms24FVkSvci-2PywrZmzI1ZzoI9l5edu1-LrI_Nkp5x7KWJSt-9un2_kyOke3O5vsF4N1F6VrfF6XQbwG5TOGbT4Z_iK9_h1B8ELZ68MY27YUL6O5Pvyn7tPjCpZnvfj9uHRY4fnmER5bI7UImb_9filpbgx8Bgntr_GabXffe-Ve_KV4hnYGfo7i8xCAZXZi_8lxEYdaUs7tOvYSKFlFomsDR-CyViilTeMVUsTCqr7bIQBAahorDjCS4IzzuaNBILlWae3GrmNiPDThsm9w",
        "access_token": "13a2646fdcc4e9b03f56fb636261f779582cbc382b3e3fd77555396468dc7de0",
        "token_type": "Bearer"
    }
    eyJraWQiOiJncGpYSHArZFNrdTJ3V2pWeGh0U2tBIiwiYWxnIjoiUlMyNTYifQ.eyJzaWQiOiJWazdtdVpmN0xWRHgvMUNkUkVjM3R1TUx1Z0FTV2M4UWJ6K3RMazNRUm1ZIiwiYWNyIjoiZWlkYXMxIiwiZXhwIjoxNzQ3NTYxMDAzLCJpc3MiOiJodHRwczovL2F1dGhlbnRpZmljYXRpb24ucHJlcHJvZHVjdGlvbi5pbnJhZS5mci8iLCJhdXRoX3RpbWUiOjE3NDc1NTc0MDIsInN1YiI6ImRqYWNvYiIsImlhdCI6MTc0NzU1NzQwMywiYXpwIjoiTUFHR09ULVRFU1QtV0FQTk1SIiwiYXRfaGFzaCI6IjhiRklEREdVcWVtN2RmMXd5dThrZEEiLCJhdWQiOlsiTUFHR09ULVRFU1QtV0FQTk1SIl19.bXv2mSN96FCgm4OujDpLOeYq703Xvi22F3mhw4F3ezu9Zj0bp0bd5cUIuf-A8wocdms24FVkSvci-2PywrZmzI1ZzoI9l5edu1-LrI_Nkp5x7KWJSt-9un2_kyOke3O5vsF4N1F6VrfF6XQbwG5TOGbT4Z_iK9_h1B8ELZ68MY27YUL6O5Pvyn7tPjCpZnvfj9uHRY4fnmER5bI7UImb_9filpbgx8Bgntr_GabXffe-Ve_KV4hnYGfo7i8xCAZXZi_8lxEYdaUs7tOvYSKFlFomsDR-CyViilTeMVUsTCqr7bIQBAahorDjCS4IzzuaNBILlWae3GrmNiPDThsm9w

    ```

* Here is a simple bash script using [cURL](https://en.wikipedia.org/wiki/CURL) and [./jq](https://jqlang.github.io/jq/download/)

    ```bash
    #!/bin/bash

    # Credentials file (URLs, client ID/secret code, User/Password)
    CREDENTIALS=.secret/inrae-credentials

    # Python script
    SSO_OIDC_SCRIPT="python sso_oidc_tools.py"

    # Maggot API URL
    API_URL="https://mydomain.fr/maggot/api"
    
    # Default Dataset and Format
    DATASET=frim1
    FORMAT=maggot
    
    # Input arguments, if any
    [ $# -gt 0 ] && DATASET=$1
    [ $# -gt 1 ] && FORMAT=$2

    # Get a token to make API calls via the SSO layer
    TOKEN=$($SSO_OIDC_SCRIPT --file $CREDENTIALS)

    # Decode the payload (optional)
    echo $TOKEN | sed -e "s/\./\n/g" | head -2 | tail -1 | base64 --decode 2>/dev/null | jq 1>&2

    # Alias CURL_API
    alias CURL_API="curl -s -H 'accept: application/json' -H 'API-KEY: XX' -H \"Authorization: Bearer $TOKEN\" -X GET"

    # Make API calls via the SSO layer
    CURL_API  $API_URL/$DATASET/$FORMAT | jq
    ```

* See a more detailed example on the python module functions : [INRAE-Portal-python]( https://github.com/djacob65/maggot-sso/blob/main/api/INRAE-Portal-python.md)

