## SSL certificate files

This directory should host the SSL certificates. The names of the SSL certificate files must be the same as those indicated for the **_SSL_CERIFICATE_** and **_SSL_CERIFICATE_KEY_** fields in the [**_nginx_ssl.conf_**](https://github.com/djacob65/maggot-sso/blob/main/nginx/nginx_ssl.conf) file.

SSL certificates can be generated using the **_getssl_** tool. See [./getssl/getssl.cfg](https://github.com/djacob65/maggot-sso/blob/main/getssl/.getssl/getssl.cfg) and [./getssl/mydomain.fr/getssl.cfg](https://github.com/djacob65/maggot-sso/blob/main/getssl/.getssl/mydomain.fr/getssl.cfg)