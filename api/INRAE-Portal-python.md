## INRAE authentication portal via API

* https://am.wiki.intranet.inrae.fr/doku.php?id=public:corpus:protocole:oidc:informationtechnique:start
* https://test-oidc.recette.inrae.fr/prod/
* https://test-saml.recette.inrae.fr/prod/

### 1 - Generates an authentication code (valid for 1 min)


```python
import sso_oidc_tools as sso

# Load credentials from file
credentials_path = '.secret/credentials'
credentials = sso.load_credentials(credentials_path)

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

# Enables/Disables debug mode
debug = 1

# Generate an authentication code
code_value = sso.get_auth_code(pars, debug)
```

    Initial URL : https://authentification.preproduction.inrae.fr/oauth2/authorize?response_type=code&client_id=MAGGOT-TEST-WAPNMR&redirect_uri=https://wapnmr.fr/maggot/redirect_uri&scope=openid+profile+email+supannEntiteAffectation
    Redirection vers : https://wapnmr.fr/maggot/redirect_uri?session_state=V%2FHaPYgCmrE7c%2Bre6VKLJ%2BTZhBtQO2DMlqXe1moIobw%3D.YndpempRdUduZlM3cHI0UjQwZnorbWxiRmE3Q1M2SVhDb3plWkIrSG8reVF3ZXBDb3l2eDV0VFp0dEtUZE9oV3FTUkVxbUdObitsK1V1cnpZVXhMbkpqOGt1RHREZ2hpeFB1WXkyZEthd289&code=486320e5a6b7937631551cdc2aecdace2e4e826c396319838e12a77120d21f92
    Code = 486320e5a6b7937631551cdc2aecdace2e4e826c396319838e12a77120d21f92


### 2 - Collects the token (valid for 1 hour)


```python
token = sso.get_token(pars, code_value, debug)
```

    {
        "expires_in": 3600,
        "id_token": "eyJraWQiOiJncGpYSHArZFNrdTJ3V2pWeGh0U2tBIiwiYWxnIjoiUlMyNTYifQ.eyJzaWQiOiJ4d1ZBa3dyZjFsQUhmVE5mQmV2OGxhLzFYZUhFK2RTdWhOdTVPeXFTLzJrIiwiYWNyIjoiZWlkYXMxIiwiZXhwIjoxNzQ3NDk3OTY2LCJpc3MiOiJodHRwczovL2F1dGhlbnRpZmljYXRpb24ucHJlcHJvZHVjdGlvbi5pbnJhZS5mci8iLCJhdXRoX3RpbWUiOjE3NDc0OTQzNjYsInN1YiI6ImRqYWNvYiIsImlhdCI6MTc0NzQ5NDM2NiwiYXpwIjoiTUFHR09ULVRFU1QtV0FQTk1SIiwiYXRfaGFzaCI6InhOclE0cFFRSk4xNHJ2Q1p5NTlGeXciLCJhdWQiOlsiTUFHR09ULVRFU1QtV0FQTk1SIl19.F1MoD_X0_H3xRZF49NrC2XQTjI2V6J8KBGSXBUwsNv_JYvLSb73GdRAoKci47IFS5_hgWW82d3xQBdTnumJw3QcTwLKx55k1IT7aAwxg_4zE0MPHOIJhHQUXP7lfd6IxmrTdzF6EYYnK4fmZ4WEGZOE98EoNejS45-_Fm4YXGYIf9M8oFR8iBXTYnXCGOfxHaD9ZOxtZPzNQh408t_Sxrx6zAo1RC5ZZTDafVf9I3VEd6lHw3uQP16fPravWnhR0coY6WP3_CkcjG7f1rtDXzA-kuuCoV6gizSie2RNpkkEBDe1C-Ov8as608lx4IHDIIMMqevKFKf7T9HDH_jW2Tw",
        "access_token": "60b3dc1b72200483a57c6f3b1ab26bad3a2a35bc910bf6a1683bc32cd13d348f",
        "token_type": "Bearer"
    }


### 3 - Parses the JSON-Web-Token (JWT) payload


```python
id_token = sso.get_json_field(token, "id_token")
payload = sso.get_payload(pars, id_token, debug)
```

    {
        "sid": "xwVAkwrf1lAHfTNfBev8la/1XeHE+dSuhNu5OyqS/2k",
        "acr": "eidas1",
        "exp": 1747497966,
        "iss": "https://authentification.preproduction.inrae.fr/",
        "auth_time": 1747494366,
        "sub": "djacob",
        "iat": 1747494366,
        "azp": "MAGGOT-TEST-WAPNMR",
        "at_hash": "xNrQ4pQQJN14rvCZy59Fyw",
        "aud": [
            "MAGGOT-TEST-WAPNMR"
        ]
    }


### 4 - Retrieves user information (useinfo)


```python
access_token = sso.get_json_field(token, "access_token")
userinfo = sso.get_data_with_bearer(pars['oauth2_url']+'/userinfo', access_token, debug)
```

    {
        "email": "daniel.jacob@inrae.fr",
        "preferred_username": "djacob",
        "sub": "djacob",
        "supannEntiteAffectation": [
            "1332",
            "CENTRE_22",
            "AUTORITE_81"
        ],
        "family_name": "Jacob",
        "given_name": "Daniel"
    }


### 5 - Makes the API request with the Token


```python
api_url = 'https://wapnmr.fr/maggot/metadata/frim1?format=maggot'
metadata = sso.get_data_with_bearer(api_url, id_token, debug)
```

    {
        "profile": "https://pmb-bordeaux.fr/maggot/conf/maggot-schema.json",
        "title": "frim1",
        "fulltitle": "FRIM - Fruit Integrative Modelling",
        "license": "Etalab V2.0 license",
        "depositor": "Jacob Daniel",
        "publication_idnumber": "10.1104/pp.113.231241",
        "publication_url": "https://doi.org/10.1104/pp.113.231241",
        "description": "The project aimed to build a virtual tomato fruit that enables the prediction of metabolite levels given genetic and environmental inputs, by an iterative process between laboratories which combine expertise in fruit biology, ecophysiology, theoretical and experimental biochemistry, and biotechnology.",
        "publication_citation": "Biais B, Bénard C, Beauvoit B, Colombié S, Prodhomme D, Ménard G, Bernillon S, Gehl B, Gautier H, Ballias P, Mazat J-P, Sweetlove L, Génard M, Gibon Y. 2014. Remarkable reproducibility of enzyme activity profiles in tomato fruits grown under contrasting environments provides a roadmap for studies of fruit metabolism. Plant Physiology 164, 1204-1221",
        "status": "Processed",
        "access_rights": "Public",
        "publication_idtype": "doi",
        "contacts": [
            "Gibon Yves"
        ],
        "authors": [
            "Bénard Camille",
            "Biais Benoit",
            "Beauvoit Bertrand",
            "Colombié Sophie"
        ],
        "collectors": [
            "Bénard Camille",
            "Biais Benoit",
            "Ballias Patricia",
            "Maucourt Mickaël"
        ],
        "curators": [
            "Moing Annick",
            "Jacob Daniel"
        ],
        "leader": [
            "Gibon Yves"
        ],
        "wpleader": [
            "Vercambre Gilles"
        ],
        "producer": [
            "Bordeaux Metabolome"
        ],
        "grantNumbers": [
            "MetaboHub",
            "Phenome"
        ],
        "keywords": [
            "tomato",
            "fruit growth",
            "experimental measurement",
            "plant trait"
        ],
        "topics": [
            "fruit growth",
            "plant health",
            "omics",
            "computer analysis"
        ],
        "experimentfactor": [
            "fruit development stage",
            "plant treatment",
            "response to water",
            "response to stress"
        ],
        "measurement": [
            "metabolite",
            "biochemical composition",
            "enzyme activity",
            "lipid Metabolism",
            "plant trait"
        ],
        "technology": [
            "NMR spectroscopy assay",
            "liquid chromatography mass spectrometry assay"
        ],
        "lifeCycleStep": [
            "Study design",
            "Data collection"
        ],
        "subject": [
            "Computer and Information Science",
            "Medicine Health and Life Sciences"
        ],
        "language": [
            "English"
        ],
        "kindOfData": [
            "Dataset"
        ],
        "dataOrigin": [
            "experimental data"
        ],
        "resources": [
            {
                "datatype": "Collection",
                "description": "ODAM dataexplorer",
                "location": "https://pmb-bordeaux.fr/dataexplorer/?ds=frim1"
            },
            {
                "datatype": "Other",
                "media": "application/json",
                "description": "Dataset's structural metadata",
                "location": "https://identifiers.org/odam:frim1"
            },
            {
                "datatype": "Other",
                "media": "application/json",
                "description": "metadata",
                "location": "datapackage.json"
            },
            {
                "datatype": "Other",
                "media": "text/plain",
                "description": "README",
                "location": "README.txt"
            },
            {
                "datatype": "JournalArticle",
                "description": "Beauvoit et al (2014) Plant Cell 26: 3224–3242 ",
                "location": "https://doi.org/10.1105/tpc.114.127761"
            },
            {
                "datatype": "JournalArticle",
                "description": "Bénard et al (2015) Journal of Experimental Botany Vol. 66, No. 11 pp. 3391–3404",
                "location": "https://doi.org/10.1093/jxb/erv151"
            },
            {
                "datatype": "JournalArticle",
                "description": "Colombié el al (2015) Plant Physiology 180, 1709–1724 ",
                "location": "https://doi.org/10.1104/pp.19.00086"
            },
            {
                "datatype": "Collection",
                "description": "Access to data via cloud-like software",
                "location": "https://pmb-bordeaux.fr/fb/share/SPyaNWJR"
            }
        ]
    }



```python

```
