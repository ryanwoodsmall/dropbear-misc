#!/bin/sh

echo ${UID} | grep -q ^0$
if [ $? -ne 0 ] ; then
    echo "you need to be root" 1>&2
    exit 1
fi

make \
  MULTI=1 \
  SCPPROGRESS=1 \
  PROGRAMS="dropbear dbclient dropbearkey dropbearconvert scp" \
  install

test -e /opt/dropbear/etc || mkdir /opt/dropbear/etc
test -e /opt/dropbear/previous && rm -f /opt/dropbear/previous
test -e /opt/dropbear/current && mv /opt/dropbear/current /opt/dropbear/previous
ln -s /opt/dropbear/`basename ${PWD}` /opt/dropbear/current
