# SSO for Maggot

## Purpose

* Implement [Single Sign-On](https://en.wikipedia.org/wiki/Single_sign-on) (SSO) authentication for a web application without modifying it.
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

* You need to edit the [local.conf](local.conf) file, then adapt parameters, especially the following ones

```shell
# Host
HOST_NAME=10.0.0.106 # Host Name or IP

# Application
APP_NAME=mmdt-web    # container name of Maggot web application
APP_PORT=80          # http port inside the Maggot web application container
APP_BASE_URL=/maggot # Base URL of Maggot web application

# Keycloak - Client
KC_REALM=Maggot
KC_CLIENT=maggot
KC_SECRET=GUWHrrBXnJp3dtT3Nl15olqDgyxaGGx2

# Keycloak - API Client
API_CLIENT=api-Maggot
API_SECRET=FYFBOxpWl6spQ9of62ljGhR7v6NcnBS7

# Network
MYNET=my-net

# Use template
USETMPL=1

# Wait message
WAITMSG=1
```

* You need to also edit the [keycloak.env](keycloak/keycloak.env) file, then change passwords :

```shell
KC_DB_USERNAME=keycloak
KC_DB_PASSWORD=kcpass01
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=adminpass
```

* For Keycloak parameters, see the [Wiki page](https://github.com/djacob65/maggot-sso/wiki/Single-Sign-On)

* You must be careful that the network name ('my-net') is the same as the one declared in Maggot's run and/or local.conf files.

* If USETMPL is equal to 1 then the [nginx.conf](nginx/nginx.conf) file will be automatically generated based on the corresponding template [nginx-conf.template](nginx/nginx-conf.template) file. Otherwise it will be used as it is.

* if WAITMSG is equal to 1 then a waiting message will be appear after starting, indicating when the keycloak will have finished its configuration (~ 15 sec)

* You must first start the SSO layer (see below) to access the keycloak interface (here http://10.0.0.106:8080). Once the different elements are configured, the settings in the local.conf file must be modified to match those entered in Keycloak. A restart of the SSO layer will therefore be necessary to take the new settings into account.

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

