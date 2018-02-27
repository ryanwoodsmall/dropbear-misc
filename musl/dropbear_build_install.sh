#!/bin/bash

make \
  -j$(($(nproc)*2+1)) \
  MULTI=1 \
  SCPPROGRESS=1 \
  PROGRAMS="dropbear dbclient dropbearkey dropbearconvert scp" \
    install \
      DESTDIR=${PWD}-built
