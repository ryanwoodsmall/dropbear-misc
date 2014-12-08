#!/bin/sh

./configure \
  --prefix=/opt/dropbear/`basename ${PWD}` \
  --enable-bundled-libtom \
  --disable-pam
