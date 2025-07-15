# TODO:
# - maybe convert *.bmp to *.png (needs paths update in src/*.h)
#
# Conditional build:
%bcond_without	qt	# psmain client (qt-dependent)
%bcond_without	usb	# USB support (relies on x86-only library)
#
%ifnarch %{ix86}
%undefine	with_usb
%endif
Summary:	EVER UPS monitoring utilities
Summary(pl.UTF-8):	Narzędzia do monitorowania zasilaczy awaryjnych UPS firmy EVER
Name:		powersoftplus
Version:	0.1.8
Release:	0.3
License:	GPL v2+
Group:		Daemons
Source0:	http://www.ever.com.pl/pl/pliki/%{name}-%{version}-x86.tar.gz
# Source0-md5:	e39d39335d7168f1fcf473471a50c35d
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-make.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-types.patch
Patch3:		%{name}-system-ftd.patch
Patch4:		%{name}-nousb.patch
URL:		http://www.ever.com.pl/pl/prod_psp.php
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_usb:BuildRequires:	libftd2xx-devel >= 0.4.10}
BuildRequires:	libstdc++-devel
%{?with_qt:BuildRequires:	qmake >= 6:3.3}
%{?with_qt:BuildRequires:	qt-devel >= 6:3.3}
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/powersoftplus

%description
This package contains some utilities for EVER UPS monitoring.

Currently supported hardware:
 - NET 500-2200 DPC
 - NET 3000 DPC
 - ECO Pro
 - ECO Pro CDS USB
 - Sinline (all)
 - Sinline USB
 - Sinline XL (all models)
 - Sinline XL USB
 - SNMP card for Sinline XL (year 2002)

%description -l pl.UTF-8
Ten zestaw programów służy do monitorowania pracy zasilaczy awaryjnych
UPS firmy EVER Sp. z o.o..

Aktualnie obsługiwane typy zasilaczy:
 - NET 500-2200 DPC
 - NET 3000 DPC
 - ECO Pro
 - ECO Pro CDS USB
 - Sinline (wszystkie)
 - Sinline USB
 - Sinline XL (wszystkie modele)
 - Sinline XL USB
 - Karta SNMP dla Sinline XL (2002 rok)

%package netclient
Summary:	PowerSoft Plus network client
Summary(pl.UTF-8):	Klient sieciowy oprogramowania PowerSoft Plus
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description netclient
PowerSoft Plus network client allows management of client
workstations from server. When it's installed on workstation, server
can notify client about power failures and eventually shutdown
workstation.

%description netclient -l pl.UTF-8
Klient sieciowy oprogramowania PowerSoft Plus pozwala na zarządzanie
stacjami klienckimi z poziomu serwera. Kiedy jest zainstalowany na
stacji roboczej, serwer może powiadamiać klienta o awariach zasilania
i w razie potrzeby wyłączyć komputer.

%package psmain
Summary:	PowerSoft Plus Control Panel
Summary(pl.UTF-8):	Panel sterowania PowerSoft Plus
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description psmain
PowerSoft Plus Control Panel is a user interface for PowerSoft Plus
monitoring program. It displays all parameters available for selected
UPS type.

%description psmain -l pl.UTF-8
PowerSoft Plus Control Panel to interfejs użytkownika do programu
monitorującego PowerSoft Plus. Wyświetla wszystkie parametry dostępne
dla wybranego typu UPS-a.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--bindir=%{_sbindir} \
	--enable-usb%{!?with_usb:=no}

%{__make}

%if %{with qt}
cd psmain/src
qmake \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags} -DHAVE_CONFIG_H" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"
%{__make} \
	QTDIR=/usr
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	CONFPATH=$RPM_BUILD_ROOT%{_sysconfdir} \
	PIXPATH=$RPM_BUILD_ROOT%{_datadir}/%{name} \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sbindir},/var/{run,log},%{_sysconfdir},/etc/{rc.d/init.d,sysconfig}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/powersoftplus
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/powersoftplus

touch $RPM_BUILD_ROOT/var/log/powersoftplus.log

ln -sf %{_sbindir}/powersoftplus $RPM_BUILD_ROOT%{_bindir}/powersoftplus

%if %{with qt}
install psmain/bin/psmain $RPM_BUILD_ROOT%{_bindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add powersoftplus
%service powersoftplus restart

%preun
if [ "$1" = "0" ]; then
	%service powersoftplus stop
	/sbin/chkconfig --del powersoftplus
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO Pomoc.pdf
%attr(755,root,root) %{_sbindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/powersoftplus
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/powersoftplus
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%attr(640,root,root) %ghost /var/log/powersoftplus.log

%files netclient
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/netclient

%if %{with qt}
%files psmain
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/psmain
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.bmp
%endif
