### API via the service account


```bash
# Get credentials (client ID, secret code)
. .secret/keycloak-credentials

# Get Access Token
JSON=$(curl -s X POST -H 'Accept: application/json' \
      -d "client_id=$CLIENT_ID" -d "client_secret=$CLIENT_SECRET" \
      -d 'grant_type=client_credentials' $OAUTH2/token)
echo $JSON | jq
```

    {
      "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ0dkRoMXBpOEtJWW9pR0J0YWlCN25hRXRraFhKRURfR0xXWHc5UVRCNEVzIn0.eyJleHAiOjE3NDc2MzY1MjcsImlhdCI6MTc0NzYzNjIyNywianRpIjoiNzJmOWU5NDAtMWQyMS00ZGY3LWI5NjUtZWIyOTY3ODFiMmMzIiwiaXNzIjoiaHR0cHM6Ly93YXBubXIuZnI6ODQ0My9yZWFsbXMvTWFnZ290IiwiYXVkIjpbImFjY291bnQiLCJtYWdnb3QiXSwic3ViIjoiMmNkMDE5OTQtMTI3YS00NDY1LTg0MjUtNGQ5NGZkNWQzMTNiIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYXBpLW1hZ2dvdCIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiLyoiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLW1hZ2dvdCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFwaS1tYWdnb3QiOnsicm9sZXMiOlsidW1hX3Byb3RlY3Rpb24iLCJ1c2VycyJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19LCJtYWdnb3QiOnsicm9sZXMiOlsidXNlcnMiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImNsaWVudEhvc3QiOiIxNTkuMTgwLjIzOS4xNjYiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzZXJ2aWNlLWFjY291bnQtYXBpLW1hZ2dvdCIsImNsaWVudEFkZHJlc3MiOiIxNTkuMTgwLjIzOS4xNjYiLCJjbGllbnRfaWQiOiJhcGktbWFnZ290In0.puQdQcQ4RLo5BxuawW7PW9V5DqV80iVhVskX2IW1ruv-KtCy7-qDfmQmeiYo22ysKadxI0kGoF_vFSrG3LAksRqQ-xv3mp5rDfJ87uoI0H2DfgYWy6Z8gVOs5e4I1E68X370ABUUktCF9q_BQEz481rq71SA71Eb65GIQ3pEyW7avKfYOusOttvKoF9_XFNBeK8em5VFiVkvZruHPmrBgIT24oCtJTxets0HZvv6c67tZp0N_rZSEYFka3RfFiv2dB-dR_KdvyGpoKDyMAxIp3L9XnKbElwa-uWkCiEcJmPhP-b4f8MVmj2c8YLgX932oahq_0KwCE5XbwxBJTKIVw",
      "expires_in": 300,
      "refresh_expires_in": 0,
      "token_type": "Bearer",
      "not-before-policy": 0,
      "scope": "profile email"
    }



```bash
# Payload from the access token
TOKEN=$(echo $JSON | jq -r '.access_token')
echo $TOKEN | sed -e "s/\./\n/g" | head -2 | tail -1 | base64 --decode 2>/dev/null | jq
```

    {
      "exp": 1747636527,
      "iat": 1747636227,
      "jti": "72f9e940-1d21-4df7-b965-eb296781b2c3",
      "iss": "https://wapnmr.fr:8443/realms/Maggot",
      "aud": [
        "account",
        "maggot"
      ],
      "sub": "2cd01994-127a-4465-8425-4d94fd5d313b",
      "typ": "Bearer",
      "azp": "api-maggot",
      "acr": "1",
      "allowed-origins": [
        "/*"
      ],
      "realm_access": {
        "roles": [
          "offline_access",
          "uma_authorization",
          "default-roles-maggot"
        ]
      },
      "resource_access": {
        "api-maggot": {
          "roles": [
            "uma_protection",
            "users"
          ]
        },
        "account": {
          "roles": [
            "manage-account",
            "manage-account-links",
            "view-profile"
          ]
        },
        "maggot": {
          "roles": [
            "users"
          ]
        }
      },
      "scope": "profile email",
      "email_verified": false,
      "clientHost": "159.180.239.166",
      "preferred_username": "service-account-api-maggot",
      "clientAddress": "159.180.239.166",
      "client_id": "api-maggot"
    }



```bash
# Alias CURL_API
alias CURL_API="curl -s -H 'accept: application/json' -H 'API-KEY: XX' -H \"Authorization: Bearer $TOKEN\" -X GET"

# Web API URL
API_URL="https://wapnmr.fr/maggot/metadata"

# Note : Think to set DEV=0 in web/inc/config/config.inc
CURL_API  $API_URL/frim1?format=maggot | jq
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
