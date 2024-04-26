#
# XXX - reenable x11 forwarding after DROPBEAR_CHANNEL_PRIO_INTERACTIVE issue is defined
# XXX - disable twofish
# XXX - sha1?
#

%global	debug_package	%{nil}

%define	spname		dropbear
%define	instdir		/opt/%{spname}
%define	profiled	%{_sysconfdir}/profile.d

%define	zlibver		1.3.1
%define	zlibdir		zlib-%{zlibver}
%define	zlibfile	%{zlibdir}.tar.gz

%define	debug_package	%{nil}

Name:		%{spname}-musl-static
Version:	2024.85
Release:	27%{?dist}
Summary:	%{spname} compiled with musl-static

Group:		Applications/Internet
License:	MIT
URL:		https://matt.ucc.asn.au/dropbear/dropbear.html
Source0:	https://matt.ucc.asn.au/dropbear/releases/%{spname}-%{version}.tar.bz2
Source1:	https://raw.githubusercontent.com/ryanwoodsmall/%{spname}-misc/master/options/%{spname}-%{version}_localoptions.h
Source2:	https://github.com/madler/zlib/releases/download/v%{zlibver}/%{zlibfile}

BuildRequires:	musl-static >= 1.2.5-0
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	which

Provides:	%{spname}
Provides:	%{name}

%description

Dropbear is a relatively small SSH server and client.
It runs on a variety of POSIX-based platforms.
Dropbear is open source software, distributed under a MIT-style license.
Dropbear is particularly useful for "embedded"-type Linux (or other Unix) systems, such as wireless routers.


%prep
%setup -q -n %{spname}-%{version}

%build
. /etc/profile
tar -zxf %{SOURCE2}
cd %{zlibdir}
./configure \
  --prefix=`pwd`-built \
  --static
sed -i.ORIG s,=gcc,=musl-gcc,g Makefile
make %{?_smp_mflags} CC=musl-gcc CFLAGS=-Wl,-static LDFLAGS=-static
make install
cd ..
cp %{SOURCE1} localoptions.h
sed -i.ORIG 's#/current/#/#g' localoptions.h
./configure \
  --prefix=%{instdir} \
  --disable-lastlog \
  --disable-utmp \
  --disable-utmpx \
  --disable-wtmp \
  --disable-wtmpx \
  --disable-pututline \
  --disable-pututxline \
  --enable-bundled-libtom \
  --disable-pam \
  --with-zlib=`pwd`/%{zlibdir}-built \
  --enable-static \
    CC="musl-gcc" \
    CFLAGS="-Wl,-static" \
    LDFLAGS="-static"
make %{?_smp_mflags} MULTI=1 SCPPROGRESS=1 PROGRAMS="dropbear dbclient dropbearkey dropbearconvert scp"


%install
. /etc/profile
make install MULTI=1 SCPPROGRESS=1 PROGRAMS="dropbear dbclient dropbearkey dropbearconvert scp" DESTDIR="%{buildroot}"
ln -sf %{instdir}/bin/dbclient %{buildroot}%{instdir}/bin/ssh
mkdir -p %{buildroot}%{instdir}/etc
mkdir -p %{buildroot}%{profiled}
echo 'export PATH="${PATH}:%{instdir}/sbin"' >  %{buildroot}%{profiled}/%{name}.sh
echo 'export PATH="${PATH}:%{instdir}/bin"'  >> %{buildroot}%{profiled}/%{name}.sh


%files
%{instdir}/bin
%{instdir}/etc
%{instdir}/sbin
%{instdir}/share
%{profiled}/%{name}.sh


%changelog
* Thu Apr 26 2024 ryanwoodsmall
- dropbear 2024.85

* Wed Apr 10 2024 ryanwoodsmall
- dropbear 2024.84
- musl 1.2.5
- move to zlib 1.3.1

* Thu May 25 2023 ryanwoodsmall
- musl 1.2.4
- get libz archive from mirror

* Mon Nov 14 2022 ryanwoodsmall
- dropbear 2022.83

* Sat Sep 10 2022 ryanwoodsmall
- enable DROPBEAR_DH_GROUP1 (client only) for old server interop

* Sat Aug 20 2022 ryanwoodsmall
- turn off debug
- fix some date(s)
- remove commented macros, which break in rhel >= 8
- source profile for musl-static

* Fri Apr 29 2022 ryan woodsmall
- release bump for musl 1.2.3

* Tue Apr 5 2022 ryanwoodsmall
- bump release to disable DEBUG_TRACE again

* Sat Apr 2 2022 ryanwoodsmall
- bump release to enable DEBUG_TRACE config

* Fri Apr 1 2022 ryanwoodsmall
- dropbear 2022.82
- disable x11 forwarding for now

* Fri Jan 15 2021 ryan woodsmall
- release bump for musl 1.2.2

* Wed Dec 30 2020 ryan woodsmall
- release bump for musl CVE-2020-28928

* Thu Oct 29 2020 ryan woodsmall
- dropbear 2020.81

* Tue Oct 20 2020 ryan woodsmall
- release bump for musl 1.2.1

* Sat Jun 27 2020 ryan woodsmall
- dropbear 2020.80

* Tue Jun 16 2020 ryan woodsmall
- release bump for new ED25519_PRIV_FILENAME option

* Mon Jun 15 2020 ryan woodsmall
- dropbear 2020.79

* Fri Mar 20 2020 ryan woodsmall
- release bump for sftp-server config

* Sat Oct 26 2019 ryan woodsmall
- release bump for musl 1.1.24

* Wed Jul 17 2019 ryan woodsmall
- release bump for musl 1.1.23

* Thu Apr 11 2019 ryan woodsmall
- release bump for musl 1.1.22

* Wed Mar 27 2019 ryan woodsmall
- dropbear 2019.78
- remove unnecessary patch(es)

* Mon Mar 25 2019 ryan woodsmall
- patch for tty restoration
- https://lists.ucc.gu.uwa.edu.au/pipermail/dropbear/2019q1/002157.html

* Sat Mar 23 2019 ryan woodsmall
- dropbear 2019.77
- release bump for debuginfo disablement

* Tue Jan 22 2019 ryan woodsmall
- release bump for musl 1.1.21

* Thu Dec  6 2018 ryan woodsmall
- disable Obsoletes/Conflicts - cause package-cleanup to report problems

* Thu Nov 29 2018 ryan woodsmall
- libz requires which

* Tue Sep 11 2018 ryan woodsmall
- release bump for musl 1.1.20

* Thu Jul 19 2018 ryan woodsmall
- include symlink for bin/ssh

* Tue Jun 12 2018 ryan woodsmall
- enable twofish and dh group 16 kex/pki/encryption settings
- enable password auth
- add /usr/local/bin and /opt/dropbear/current/bin to default path

* Sat Jun  2 2018 ryan woodsmall
- remove ../current/.. from /opt/dropbear path during rpm build

* Wed May 30 2018 ryan woodsmall
- add static sortix libz for compression support

* Tue Feb 27 2018 ryan woodsmall
- dropbear spec
