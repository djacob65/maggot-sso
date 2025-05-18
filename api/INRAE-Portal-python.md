## INRAE authentication portal via API

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
    Redirection vers : https://wapnmr.fr/maggot/redirect_uri?session_state=%2BCl4%2FNePOo%2BQJbdUBg6UuCLJ0xmHKqdm2y6GvVqNUbI%3D.K1grUE5BMTRCdDJxK1JBZy90MlRpZUJXNy9TWXFlRDNSekFRUy95clNOdUMvNmhhQm9XNUNTaHVmVjU3eWpPZDlwM0hlWGNuRi96UEJoWVRlbm9hRiswamVPWW5GQmV0TDNsVmpMcHFDbUU9&code=c153c9336b766268a4f88cc877be5160da3b955bd720aeeaf7f07e910f8bcff1
    Code = c153c9336b766268a4f88cc877be5160da3b955bd720aeeaf7f07e910f8bcff1


### 2 - Collects the token (valid for 1 hour)


```python
token = sso.get_token(pars, code_value, debug)
```

    {
        "expires_in": 3600,
        "id_token": "eyJraWQiOiJncGpYSHArZFNrdTJ3V2pWeGh0U2tBIiwiYWxnIjoiUlMyNTYifQ.eyJzaWQiOiJ0dkh3UE1JK2JiZzE4VUQwWm9WZHFtQXRTVk84NDdMMU84aHVMMzM4RklrIiwiYWNyIjoiZWlkYXMxIiwiZXhwIjoxNzQ3NTY0MTc2LCJpc3MiOiJodHRwczovL2F1dGhlbnRpZmljYXRpb24ucHJlcHJvZHVjdGlvbi5pbnJhZS5mci8iLCJhdXRoX3RpbWUiOjE3NDc1NjA1NzUsInN1YiI6ImRqYWNvYiIsImlhdCI6MTc0NzU2MDU3NiwiYXpwIjoiTUFHR09ULVRFU1QtV0FQTk1SIiwiYXRfaGFzaCI6IjJzZHJ6Z01tcTlkVzNteFotTmVWbWciLCJhdWQiOlsiTUFHR09ULVRFU1QtV0FQTk1SIl19.YfF4GKDT61_VSv8SK9saljFZnXQjIy-3y92Qrtv8CPXS2KT4t5VbSQvktiM0tZ-CDF7GPa3vklPeVhS1HaYsbG0fnyETpa5upNWg5VX5LXZWlp7sg-1QqT_HGCpdMxGkzY1A02__M3tnEReunXm-1Y4gRk3IdPZH2Kilh8MqHD2KXeDkgvdDqcy64Pj240zL97iTkdYsWz2H-xaCe0-P-kzXIrZ2CqkaXNOUNfAsGU782fpnhgFtj4-qPug7zLHm-mIZB1irurAqXSqIMKQ8Rvaz5wnq081q7aVrrKZaxPD3yg7rq1wV-bY8cbLsXkYecRGyu1IIKoh4105RfWBaKw",
        "access_token": "c38581bb7c45d64133522725679c6b5b37fa024286097aba4cb0994e9fab8527",
        "token_type": "Bearer"
    }


### 3 - Parses the JSON-Web-Token (JWT) payload


```python
id_token = sso.get_json_field(token, "id_token")
payload = sso.get_payload(pars, id_token, debug)
```

    {
        "sid": "tvHwPMI+bbg18UD0ZoVdqmAtSVO847L1O8huL338FIk",
        "acr": "eidas1",
        "exp": 1747564176,
        "iss": "https://authentification.preproduction.inrae.fr/",
        "auth_time": 1747560575,
        "sub": "djacob",
        "iat": 1747560576,
        "azp": "MAGGOT-TEST-WAPNMR",
        "at_hash": "2sdrzgMmq9dW3mxZ-NeVmg",
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
api_url = 'https://wapnmr.fr/maggot/metadata/frim1?format=jsonld'
metadata = sso.get_data_with_bearer(api_url, id_token, debug=1)
```

    {
        "@context": {
            "schema": "http://schema.org/",
            "name": "http://schema.org/name",
            "identifier": "http://schema.org/identifier",
            "description": "http://schema.org/description",
            "email": "http://schema.org/email",
            "url": "http://schema.org/url",
            "affiliation": "http://schema.org/affiliation",
            "memberOf": "http://schema.org/memberOf",
            "funder": "http://schema.org/funder",
            "inDefinedTermSet": "http://schema.org/inDefinedTermSet",
            "additionalType": "http://schema.org/additionalType",
            "encodingFormat": "http://schema.org/encodingFormat",
            "accessRights": "http://purl.org/dc/terms/accessRights",
            "citation": "https://dataverse.org/schema/citation/",
            "contributor": "http://purl.org/dc/terms/contributor",
            "contributorType": "http://purl.org/datacite/v4.4/ContributorType",
            "subject": "http://purl.org/dc/terms/subject",
            "kindOfData": "http://rdf-vocabulary.ddialliance.org/discovery#kindOfData",
            "publication": "http://purl.org/dc/terms/isReferencedBy",
            "publicationCitation": "http://purl.org/dc/terms/bibliographicCitation",
            "publicationIDType": "http://purl.org/spar/datacite/ResourceIdentifierScheme",
            "publicationIDNumber": "http://purl.org/spar/datacite/ResourceIdentifier",
            "publicationURL": "https://schema.org/URL"
        },
        "@type": "schema:Dataset",
        "@id": "https://pmb-bordeaux.fr/maggot/metadata/frim1",
        "schema:version": "1.0",
        "schema:identifier": "maggot:frim1",
        "schema:name": "FRIM - Fruit Integrative Modelling",
        "schema:description": "The project aimed to build a virtual tomato fruit that enables the prediction of metabolite levels given genetic and environmental inputs, by an iterative process between laboratories which combine expertise in fruit biology, ecophysiology, theoretical and experimental biochemistry, and biotechnology.",
        "schema:license": "https://spdx.org/licenses/etalab-2.0.html",
        "accessRights": "Public",
        "schema:creator": [
            {
                "@type": "schema:Person",
                "name": "Gibon, Yves",
                "identifier": "https://orcid.org/0000-0001-8161-1089",
                "email": "yves.gibon@inrae.fr",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/00ccpdp17",
                    "name": "UMR 1332 BFP INRAE"
                }
            }
        ],
        "schema:author": [
            {
                "@type": "schema:Person",
                "name": "Bénard, Camille",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/00ccpdp17",
                    "name": "UMR 1332 BFP INRAE"
                }
            },
            {
                "@type": "schema:Person",
                "name": "Biais, Benoit",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/00ccpdp17",
                    "name": "Biologie du Fruit et Pathologie"
                }
            },
            {
                "@type": "schema:Person",
                "name": "Beauvoit, Bertrand",
                "identifier": "https://orcid.org/0000-0002-7666-6429",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/057qpr032",
                    "name": "University of Bordeaux"
                }
            },
            {
                "@type": "schema:Person",
                "name": "Colombié, Sophie",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/00ccpdp17",
                    "name": "UMR 1332 BFP INRAE"
                }
            }
        ],
        "contributor": [
            {
                "@type": "schema:Person",
                "contributorType": "http://purl.org/datacite/v4.4/DataCollector",
                "name": "Bénard, Camille",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/00ccpdp17",
                    "name": "UMR 1332 BFP INRAE"
                }
            },
            {
                "@type": "schema:Person",
                "contributorType": "http://purl.org/datacite/v4.4/DataCollector",
                "name": "Biais, Benoit",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/00ccpdp17",
                    "name": "Biologie du Fruit et Pathologie"
                }
            },
            {
                "@type": "schema:Person",
                "contributorType": "http://purl.org/datacite/v4.4/DataCollector",
                "name": "Ballias, Patricia",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/00ccpdp17",
                    "name": "Biologie du Fruit et Pathologie"
                }
            },
            {
                "@type": "schema:Person",
                "contributorType": "http://purl.org/datacite/v4.4/DataCollector",
                "name": "Maucourt, Mickaël",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/057qpr032",
                    "name": "Université de Bordeaux"
                }
            },
            {
                "@type": "schema:Person",
                "contributorType": "http://purl.org/datacite/v4.4/DataCurator",
                "name": "Moing, Annick",
                "identifier": "https://orcid.org/0000-0003-1144-3600",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/00ccpdp17",
                    "name": "UMR 1332 BFP INRAE"
                }
            },
            {
                "@type": "schema:Person",
                "contributorType": "http://purl.org/datacite/v4.4/DataCurator",
                "name": "Jacob, Daniel",
                "identifier": "https://orcid.org/0000-0002-6687-7169",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/00ccpdp17",
                    "name": "UMR 1332 BFP INRAE"
                }
            },
            {
                "@type": "schema:Person",
                "contributorType": "http://purl.org/datacite/v4.4/ProjectLeader",
                "name": "Gibon, Yves",
                "identifier": "https://orcid.org/0000-0001-8161-1089",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/00ccpdp17",
                    "name": "UMR 1332 BFP INRAE"
                }
            },
            {
                "@type": "schema:Person",
                "contributorType": "http://purl.org/datacite/v4.4/WorkPackageLeader",
                "name": "Vercambre, Gilles",
                "identifier": "https://orcid.org/0000-0001-6486-9547",
                "affiliation": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/003vg9w96",
                    "name": "INRAE Avignon"
                }
            }
        ],
        "schema:funding": [
            {
                "@type": "schema:Grant",
                "name": "MetaboHub",
                "identifer": "ANR-11-INBS-0010",
                "funder": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/03t0t6y08",
                    "name": "ANR"
                }
            },
            {
                "@type": "schema:Grant",
                "name": "Phenome",
                "identifer": "ANR-11-INBS-0012",
                "funder": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/03t0t6y08",
                    "name": "ANR"
                }
            }
        ],
        "schema:keywords": [
            {
                "@type": "schema:DefinedTerm",
                "name": "tomato",
                "url": "http://purl.jp/bio/4/id/200906080909032148",
                "inDefinedTermSet": "IOBC"
            },
            {
                "@type": "schema:DefinedTerm",
                "name": "fruit growth",
                "url": "http://purl.obolibrary.org/obo/TO_0000929",
                "inDefinedTermSet": "PTO"
            },
            {
                "@type": "schema:DefinedTerm",
                "name": "experimental measurement",
                "url": "http://edamontology.org/data_3108",
                "inDefinedTermSet": "EDAM"
            },
            {
                "@type": "schema:DefinedTerm",
                "name": "plant trait",
                "url": "http://purl.obolibrary.org/obo/TO_0000387",
                "inDefinedTermSet": "PTO"
            }
        ],
        "citation:topicClassification": [
            {
                "@type": "schema:DefinedTerm",
                "name": "fruit growth",
                "url": "http://purl.obolibrary.org/obo/TO_0000929",
                "inDefinedTermSet": "PTO"
            },
            {
                "@type": "schema:DefinedTerm",
                "name": "plant health",
                "url": "http://purl.jp/bio/4/id/201406082741614190",
                "inDefinedTermSet": "IOBC"
            },
            {
                "@type": "schema:DefinedTerm",
                "name": "omics",
                "url": "http://purl.jp/bio/4/id/201306053666021113",
                "inDefinedTermSet": "IOBC"
            },
            {
                "@type": "schema:DefinedTerm",
                "name": "computer analysis"
            }
        ],
        "schema:variableMeasured": [
            {
                "@type": "schema:PropertyValue",
                "name": "metabolite"
            },
            {
                "@type": "schema:PropertyValue",
                "name": "biochemical composition"
            },
            {
                "@type": "schema:PropertyValue",
                "name": "enzyme activity"
            },
            {
                "@type": "schema:PropertyValue",
                "name": "lipid Metabolism"
            },
            {
                "@type": "schema:PropertyValue",
                "name": "plant trait"
            }
        ],
        "schema:measurementTechnique": [
            {
                "@type": "schema:DefinedTerm",
                "name": "NMR spectroscopy assay"
            },
            {
                "@type": "schema:DefinedTerm",
                "name": "liquid chromatography mass spectrometry assay"
            }
        ],
        "subject": [
            "Computer and Information Science",
            "Medicine Health and Life Sciences"
        ],
        "kindOfData": [
            "Dataset"
        ],
        "citation:dataOrigin": [
            "experimental data"
        ],
        "citation:producer": [
            {
                "@type": "schema:Organization",
                "name": "Bordeaux Metabolome",
                "url": "https://metabolome.cgfb.u-bordeaux.fr/",
                "memberOf": {
                    "@type": "schema:Organization",
                    "identifier": "https://ror.org/003vg9w96",
                    "name": "INRAE"
                }
            }
        ],
        "publication": {
            "@type": "schema:CreativeWork",
            "publicationCitation": "Biais B, Bénard C, Beauvoit B, Colombié S, Prodhomme D, Ménard G, Bernillon S, Gehl B, Gautier H, Ballias P, Mazat J-P, Sweetlove L, Génard M, Gibon Y. 2014. Remarkable reproducibility of enzyme activity profiles in tomato fruits grown under contrasting environments provides a roadmap for studies of fruit metabolism. Plant Physiology 164, 1204-1221",
            "publicationIDType": "doi",
            "publicationIDNumber": "10.1104/pp.113.231241",
            "publicationURL": "https://doi.org/10.1104/pp.113.231241"
        },
        "citation:lifeCycleStep": [
            "Study design",
            "Data collection"
        ],
        "schema:hasPart": [
            {
                "@type": "schema:CreativeWork",
                "additionalType": "http://purl.org/datacite/v4.4/Collection",
                "description": "ODAM dataexplorer",
                "url": "https://pmb-bordeaux.fr/dataexplorer/?ds=frim1"
            },
            {
                "@type": "schema:CreativeWork",
                "additionalType": "http://purl.org/datacite/v4.4/Other",
                "encodingFormat": "application/json",
                "description": "Dataset's structural metadata",
                "url": "https://identifiers.org/odam:frim1"
            },
            {
                "@type": "schema:CreativeWork",
                "additionalType": "http://purl.org/datacite/v4.4/JournalArticle",
                "description": "Beauvoit et al (2014) Plant Cell 26: 3224–3242 ",
                "url": "https://doi.org/10.1105/tpc.114.127761"
            },
            {
                "@type": "schema:CreativeWork",
                "additionalType": "http://purl.org/datacite/v4.4/JournalArticle",
                "description": "Bénard et al (2015) Journal of Experimental Botany Vol. 66, No. 11 pp. 3391–3404",
                "url": "https://doi.org/10.1093/jxb/erv151"
            },
            {
                "@type": "schema:CreativeWork",
                "additionalType": "http://purl.org/datacite/v4.4/JournalArticle",
                "description": "Colombié el al (2015) Plant Physiology 180, 1709–1724 ",
                "url": "https://doi.org/10.1104/pp.19.00086"
            },
            {
                "@type": "schema:CreativeWork",
                "additionalType": "http://purl.org/datacite/v4.4/Collection",
                "description": "Access to data via cloud-like software",
                "url": "https://pmb-bordeaux.fr/fb/share/SPyaNWJR"
            }
        ],
        "sdDatePublished": "2025-05-18 11:29:51"
    }



```python

```
