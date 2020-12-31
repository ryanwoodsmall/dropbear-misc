%define	spname		dropbear
%define	instdir		/opt/%{spname}
%define	profiled	%{_sysconfdir}/profile.d

%define	libzver		1.2.8.2015.12.26
%define	libzdir		libz-%{libzver}

%define	debug_package	%{nil}

Name:		%{spname}-musl-static
Version:	2020.81
Release:	19%{?dist}
Summary:	%{spname} compiled with musl-static

Group:		Applications/Internet
License:	MIT
URL:		https://matt.ucc.asn.au/dropbear/dropbear.html
Source0:	https://matt.ucc.asn.au/dropbear/releases/%{spname}-%{version}.tar.bz2
Source1:	https://raw.githubusercontent.com/ryanwoodsmall/%{spname}-misc/master/options/%{spname}-%{version}_localoptions.h
Source2:	https://sortix.org/libz/release/libz-%{libzver}.tar.gz

BuildRequires:	musl-static >= 1.2.1-1
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	which

#Obsoletes:	%{spname}
#Conflicts:	%{spname}

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
tar -zxf %{SOURCE2}
cd %{libzdir}
./configure \
  --prefix=`pwd`-built \
  --enable-shared=no \
  --disable-shared \
  --enable-static \
  --enable-static=yes \
    CC="musl-gcc" \
    CFLAGS="-Wl,-static" \
    LDFLAGS="-static"
make %{?_smp_mflags}
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
  --with-zlib=`pwd`/%{libzdir}-built \
  --enable-static \
    CC="musl-gcc" \
    CFLAGS="-Wl,-static" \
    LDFLAGS="-static"
make %{?_smp_mflags} MULTI=1 SCPPROGRESS=1 PROGRAMS="dropbear dbclient dropbearkey dropbearconvert scp"


%install
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
* Wed Dec 30 2020 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl CVE-2020-28928

* Thu Oct 29 2020 ryan woodsmall <rwoodsmall@gmail.com>
- dropbear 2020.81

* Tue Oct 20 2020 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.2.1

* Fri Jun 27 2020 ryan woodsmall <rwoodsmall@gmail.com>
- dropbear 2020.80

* Tue Jun 16 2020 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for new ED25519_PRIV_FILENAME option

* Mon Jun 15 2020 ryan woodsmall <rwoodsmall@gmail.com>
- dropbear 2020.79

* Fri Mar 20 2020 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for sftp-server config

* Sat Oct 26 2019 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.1.24

* Wed Jul 17 2019 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.1.23

* Thu Apr 11 2019 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.1.22

* Wed Mar 27 2019 ryan woodsmall <rwoodsmall@gmail.com>
- dropbear 2019.78
- remove unnecessary patch(es)

* Mon Mar 25 2019 ryan woodsmall <rwoodsmall@gmail.com>
- patch for tty restoration
- https://lists.ucc.gu.uwa.edu.au/pipermail/dropbear/2019q1/002157.html

* Sat Mar 23 2019 ryan woodsmall <rwoodsmall@gmail.com>
- dropbear 2019.77
- release bump for debuginfo disablement

* Tue Jan 22 2019 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.1.21

* Thu Dec  6 2018 ryan woodsmall <rwoodsmall@gmail.com>
- disable Obsoletes/Conflicts - cause package-cleanup to report problems

* Thu Nov 29 2018 ryan woodsmall <rwoodsmall@gmail.com>
- libz requires which

* Tue Sep 11 2018 ryan woodsmall <rwoodsmall@gmail.com>
- release bump for musl 1.1.20

* Thu Jul 19 2018 ryan woodsmall <rwoodsmall@gmail.com>
- include symlink for bin/ssh

* Tue Jun 12 2018 ryan woodsmall <rwoodsmall@gmail.com>
- enable twofish and dh group 16 kex/pki/encryption settings
- enable password auth
- add /usr/local/bin and /opt/dropbear/current/bin to default path

* Sat Jun  2 2018 ryan woodsmall <rwoodsmall@gmail.com>
- remove ../current/.. from /opt/dropbear path during rpm build

* Wed May 30 2018 ryan woodsmall <rwoodsmall@gmail.com>
- add static sortix libz for compression support

* Tue Feb 27 2018 ryan woodsmall <rwoodsmall@gmail.com>
- dropbear spec
