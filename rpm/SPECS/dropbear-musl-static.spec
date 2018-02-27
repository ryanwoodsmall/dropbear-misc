%define	spname		dropbear
%define	instdir		/opt/%{spname}
%define	profiled	%{_sysconfdir}/profile.d

Name:		%{spname}-musl-static
Version:	2018.76
Release:	1%{?dist}
Summary:	%{spname} compiled with musl-static

Group:		Applications/Internet
License:	MIT
URL:		https://matt.ucc.asn.au/dropbear/dropbear.html
Source0:	https://matt.ucc.asn.au/dropbear/releases/%{spname}-%{version}.tar.bz2
Source1:	https://raw.githubusercontent.com/ryanwoodsmall/%{spname}-misc/master/options/%{spname}-%{version}_localoptions.h

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
cp %{SOURCE1} localoptions.h
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
  --disable-zlib \
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
* Tue Feb 27 2018 ryan woodsmall <rwoodsmall@gmail.com>
- dropbear spec
