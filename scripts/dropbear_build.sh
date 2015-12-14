#!/bin/sh

# how many parallel jobs
if `which nproc >/dev/null 2>&1` ; then
  MJOBS=`nproc`
elif `which lscpu >/dev/null 2>&1` ; then
  MJOBS=`lscpu | awk '/^CPU\(s\)/{print $NF}'`
else
# check /proc/cpuinfo (arm format is different)
# check getconf (glibc only)
  MJOBS=1
fi

make \
  -j${MJOBS} \
  MULTI=1 \
  SCPPROGRESS=1 \
  STATIC=1 \
  PROGRAMS="dropbear dbclient dropbearkey dropbearconvert scp"
