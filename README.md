dropbear-misc
=============

Dropbear SSH scripts and assorted stuff.

todo
====
* pick between centos 6, centos 7, chrome/chromium os
  * c6 doesn't need pam, can be static
  * c7 requires pam, doesn't work well/at all with static
  * chromium is key-auth only
* setup custom known hosts file in **cli-kex.c** (```dbear_hosts```?)
* move bundled sortix libz to zlib-ng from github
