%define	spname		dropbear
%define	instdir		/opt/%{spname}
%define	profiled	%{_sysconfdir}/profile.d

%define	libzver		1.2.8.2015.12.26
%define	libzdir		libz-%{libzver}

Name:		%{spname}-musl-static
Version:	2018.76
Release:	3%{?dist}
Summary:	%{spname} compiled with musl-static

Group:		Applications/Internet
License:	MIT
URL:		https://matt.ucc.asn.au/dropbear/dropbear.html
Source0:	https://matt.ucc.asn.au/dropbear/releases/%{spname}-%{version}.tar.bz2
Source1:	https://raw.githubusercontent.com/ryanwoodsmall/%{spname}-misc/master/options/%{spname}-%{version}_localoptions.h
Source2:	https://sortix.org/libz/release/libz-%{libzver}.tar.gz

BuildRequires:	musl-static >= 1.1.19-0
BuildRequires:	gcc
BuildRequires:	make

Obsoletes:	%{spname}
Conflicts:	%{spname}

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
* Sat Jun  2 2018 ryan woodsmall <rwoodsmall@gmail.com>
- remove ../current/.. from /opt/dropbear path during rpm build

* Wed May 30 2018 ryan woodsmall <rwoodsmall@gmail.com>
- add static sortix libz for compression support

* Tue Feb 27 2018 ryan woodsmall <rwoodsmall@gmail.com>
- dropbear spec