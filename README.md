# SSO for Maggot

## Purpose

* Implement [Single Sign-On](https://en.wikipedia.org/wiki/Single_sign-on) (SSO) authentication through a web application without modifying it.
* See the [Wiki page](https://github.com/djacob65/maggot-sso/wiki/Single-Sign-On)

<br>

## Installation

Requirements:

* a recent Linux OS that support Docker (see https://www.docker.com/)

* You have to create the docker images:

        Step 1: Clone this repository, then `cd` to your clone path.

            $ git clone https://github.com/djacob65/maggot-sso.git
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

* You need to edit the [local.conf](#) file, then adapt parameters, especially the following ones

```shell
# Host 
HOST_IP=10.0.0.106
APP_PORT=8000

# Keycloak : realm, clients & Secret Codes
KC_REALM=myrealm
NGINX_CLIENT=nginx
NGINX_SECRET=<secret code for nginx>
API_CLIENT=api-client
API_SECRET=<secret code for api-client>
```

* You need to also edit the [Keycloak/keycloak.env](#) file, then change passwords :

```shell
KC_DB_USERNAME=keycloak
KC_DB_PASSWORD=kcpass01
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=adminpass
```

* You must first start the SSO layer (see below) to access the keycloak interface (here http://10.0.0.106:8080). Once the different elements are configured, the settings in the run file must be modified to match those entered in Keycloak. A restart of the SSO layer will therefore be necessary to take the new settings into account.

* <b>Note</b>: the [nginx.conf](#) file is automatically generated based on the corresponding template [nginx-conf.template](#) file.

<br>

## Usage

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

