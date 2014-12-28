#!/bin/sh

make \
  MULTI=1 \
  SCPPROGRESS=1 \
  STATIC=1 \
  PROGRAMS="dropbear dbclient dropbearkey dropbearconvert scp" \
  install
