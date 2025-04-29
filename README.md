# SSO for Maggot

## Purpose

* Implement [Single Sign-On](https://en.wikipedia.org/wiki/Single_sign-on) (SSO) authentication for the Maggot application.

* For management within a collective that goes beyond a simple intranet, it may be necessary to set up an authentication layer. Setting up such a layer can be done independently of the Maggot tool, i.e. without modifying its code or configuration. The proposed implementation can serve as a basis for a larger configuration.

* See the [Wiki page](https://github.com/djacob65/maggot-sso/wiki/Single-Sign-On) for more details

<br>

## Installation

Requirements:

* a recent Linux OS that support Docker (see https://www.docker.com/)

* You have to create the docker images:

        Step 1: Clone this repository, then `cd` to your clone path.

            $ git clone https://github.com/djacob65/maggot-sso.git sso
            $ cd sso

        Step 2: Create the docker image:

            $ sh ./run build


Then, you should have something like below:

    $ docker images
```
REPOSITORY        TAG           IMAGE ID         CREATED          SIZE
nginx-image       latest        77b4d4887fa7     44 hours ago     398MB
keycloak-image    latest        8cfd3af34d85     5 days ago       459MB
postgres-image    latest        5f01f1db17f8     11 days ago      431MB
```

<br>

## configuration

* You need to edit the [run](run) file, then adapt parameters, especially the following ones

```shell
# Host Name or IP
#HOSTNAME=10.0.0.106
HOSTNAME=mydomain.fr

# Nginx with OIDC
NGINX_IMAGE=nginx-image
NGINX_CONTAINER=nginx
#NGINX_PORT=80
NGINX_PORT=443

# Postgres
PG_IMAGE=postgres-image
PG_CONTAINER=postgres
PG_PORT=5432
PG_VOL=postgres_data

# Keycloak
KC_IMAGE=keycloak-image
KC_CONTAINER=keycloak
#KC_PORT=8080
KC_PORT=8443

# NGINX configuration files
NGINX_SSL=nginx_ssl.conf 
NGINX_SSL_EXT=nginx_ssl_inrae.conf 

# External Identity Provider ?
IP_EXT=0
```

* You need to also edit the [keycloak.env](keycloak/keycloak.env) file, then change passwords :

```shell
KC_DB_USERNAME=keycloak
KC_DB_PASSWORD=kcpass01
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=adminpass
```

* For a secure environment (SSL), you need to specify the domain name in the [keycloak_ssl.env](keycloak/keycloak_ssl.env)
```shell
KC_HOSTNAME=mydomain.fr
```


### Notes

* For a secure environment (SSL), You must have up-to-date SSL certificates. Therefore, we recommend using the certificates provided by [Let's Encrypt](https://letsencrypt.org/) and using the [getssl](https://github.com/srvrco/getssl) tool. See the corresponding [README](getssl/README.md) file.

* You must be careful that the network name ('my-net') is the same as the one defined in Maggot's [run and/or local.conf files.](https://github.com/inrae/pgd-mmdt/blob/main/run).

* The server 'mmdt-web' in the nginx configuration file must be equal to the WEB_CONTAINER parameter defined in Maggot's [run and/or local.conf files.](https://github.com/inrae/pgd-mmdt/blob/main/run).

* In case Maggot must be accessible from outside of your network (internet), you must ensure that the application web port (80) as well as the keycloak web port (8080 or 8443) are open and accessible beyond the various firewalls, starting with the one that is possibly installed on the host machine.

* You must first start the SSO layer (see below) to access the keycloak interface (e.g http://10.0.0.106:8080 or https://mydomain.fr:8443). Once the different elements are configured, the settings in the run file and in the nginx configuration file must be modified to match those entered in Keycloak. A restart of the SSO layer will therefore be necessary to take the new settings into account.

<br>

## Usage

* **Note**: The Maggot application must be started first. Otherwise, an error occurs when starting the nginx container because the server "mmdt-web" will not be recognized as available.

* To start the *SSO* layer 

```shell
sh ./run start
```

* To stop the *SSO* layer 

```shell
sh ./run stop
```

* To restart the *SSO* layer 

```shell
sh ./run restart
```

* To view the container list

```shell
sh ./run ps
```

* To authorize HTTP protocol in case you've got the message :"HTTPS required" in the keycloak admin interface

```shell
sh ./run http
```

<br>

* Based on the default configuration provided (see above):
    
      * The Maggot URL is https://mydomain.fr/maggot/

      * The Keycloak interface URL is https://mydomain.fr:8443

<br>


## License

Copyright (C) 2024  Daniel Jacob - INRAE

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

