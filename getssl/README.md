## Obtain SSL certificates from the letsencrypt.org ACME server

* See https://github.com/srvrco/getssl

* Edit ~/.getssl/getssl.cfg to set the values you want as the default for the majority of your certificates.

* Then edit ~/.getssl/mydomain.fr/getssl.cfg to have the values you want for this specific domain (make sure to uncomment and specify correct ACL option, since it is required). 'mydomain.fr' is only an example for illustration. You have to change with the rigth domain name.

* Create the getssl script under /usr/local/bin

```shell
#!/bin/bash

MYDIR=`dirname $0` && [ ! `echo "$0" | grep '^\/'` ] && MYDIR=`pwd`/$MYDIR

LOGFILE=/tmp/getssl.log

/opt/mydomain/getssl/getssl $1 1>$LOGFILE 2>$LOGFILE

exit 0
```

* Add a line into the crontab (with sudo crontab -e)

```shell
# Update the SSL certificate (Let's encrypt) if necessary
00 0 * * 7   root    /usr/local/bin/getssl -a
```
