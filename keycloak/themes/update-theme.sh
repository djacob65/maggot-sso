#!/bin/bash

THEME=maggot
[ $# -gt 0 ] && THEME=$1

[ ! -f ./${THEME}-theme.tar.gz ] && "Error: the ${THEME}-theme.tar.gz file do not exist !!" && exit 1

[ -d ./$THEME ] && rm -rf ./$THEME
tar xvzf ./${THEME}-theme.tar.gz

find ./$THEME -type d -exec  chmod 755 {} \;
find ./$THEME -type f -exec  chmod 644 {} \;

[ -f ./${THEME}-theme.tar.gz ] && rm -f ./${THEME}-theme.tar.gz

sh /opt/wapnmr/sso/run restart
