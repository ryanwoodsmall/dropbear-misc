#!/bin/sh

# default to only one parallel make job
MJOBS=1
# XXX - check getconf (glibc only)
# how many parallel jobs
if `which nproc >/dev/null 2>&1` ; then
  MJOBS=`nproc`
elif `which lscpu >/dev/null 2>&1` ; then
  MJOBS=`lscpu | awk '/^CPU\(s\)/{print $NF}'`
elif [ `xargs < /proc/cpuinfo | grep -o 'processor : ' | wc -l` -gt 1 ] ; then
  MJOBS=`xargs < /proc/cpuinfo | grep -o 'processor : ' | wc -l`
fi

make \
  -j${MJOBS} \
  MULTI=1 \
  SCPPROGRESS=1 \
  PROGRAMS="dropbear dbclient dropbearkey dropbearconvert scp"
