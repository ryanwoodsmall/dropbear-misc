#!/bin/bash

./configure \
  --prefix=/opt/dropbear/`basename ${PWD}` \
  --disable-lastlog \
  --disable-utmp \
  --disable-utmpx \
  --disable-wtmp \
  --disable-wtmpx \
  --disable-pututline \
  --disable-pututxline \
  --enable-bundled-libtom \
  --disable-pam \
  --disable-zlib \
    CC="/usr/local/musl/bin/musl-gcc" \
    LDFLAGS="-static"
