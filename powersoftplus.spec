Summary:	EVER UPS monitoring utilities
Summary(pl.UTF-8):	Narzędzia do monitorowania zasilaczy awaryjnych UPS firmy EVER
Name:		powersoftplus
Version:	0.1.8
Release:	0.2
License:	GPL
Group:		Daemons
Source0:	http://www.ever.com.pl/pl/pliki/%{name}-%{version}-x86.tar.gz
# Source0-md5:	e39d39335d7168f1fcf473471a50c35d
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-make.patch
URL:		http://www.ever.com.pl/powersoft_prod.php
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	SysVinit
Requires:	rc-scripts
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/psplus

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
Aktualnie obslugiwane typy zasilaczy:
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
Summary:	netclient
Group:		Daemons
Requires:	%{name}

%description netclient
netclient

%package psmain
Summary:	psmain
Group:		X11/Applications
Requires:	qt

%description psmain
psmain

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--bindir=%{_sbindir} \
	--prefix=/usr

sed -i -e 's#CONFIG_PATH.*#CONFIG_PATH	"%{_sysconfdir}"#g' config.h
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	DEBUG="%{rpmcflags} -I/usr/include/ncurses" \
	PIXPATH="%{_datadir}/%{name}" \
	LIBUPATH=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir}}
%{__make} install \
	CONFPATH=$RPM_BUILD_ROOT%{_sysconfdir} \
	PIXPATH=$RPM_BUILD_ROOT%{_datadir}/%{name} \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBUPATH=$RPM_BUILD_ROOT%{_libdir} \
	LIBPATH=$RPM_BUILD_ROOT%{_libdir}

rm $RPM_BUILD_ROOT%{_libdir}/libftd2xx.{so,so.0}
ln -sf %{_libdir}/libftd2xx.so.0.4.10 $RPM_BUILD_ROOT%{_libdir}/ibftd2xx.so
ln -sf %{_libdir}/libftd2xx.so.0.4.10 $RPM_BUILD_ROOT%{_libdir}/ibftd2xx.so.0

rm $RPM_BUILD_ROOT%{_libdir}/ibftd2xx.{so,so.0}

install -d $RPM_BUILD_ROOT{%{_sbindir},/var/{run,log},%{_sysconfdir},/etc/{rc.d/init.d,sysconfig}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/powersoftplus
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/powersoftplus

touch $RPM_BUILD_ROOT/var/log/powersoftplus.log

#mv $RPM_BUILD_ROOT/etc/powersoftplus $RPM_BUILD_ROOT/etc/psplus
ln -sf %{_sbindir}/powersoftplus $RPM_BUILD_ROOT%{_bindir}/powersoftplus

#
# TODO:
#  psmain should be compiled but isn't - sorry I have no time to fix this now, 
#  so I just copy precompiled version
cp psmain/bin/psmain $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add powersoftplus
/sbin/ldconfig
if [ -f /var/lock/subsys/powersoftplus ]; then
	/etc/rc.d/init.d/powersoftplus restart >&2
else
	echo "Run \"/etc/rc.d/init.d/powersoftplus start\" to start powersoftplus daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/powersoftplus ]; then
		/etc/rc.d/init.d/powersoftplus stop >&2
	fi
	/sbin/chkconfig --del powersoftplus
fi
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO Pomoc.pdf
%attr(755,root,root) %{_sbindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_libdir}/*.so*
%attr(754,root,root) /etc/rc.d/init.d/powersoftplus
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/powersoftplus
%{_datadir}/%{name}
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.*
%attr(640,root,root) %ghost /var/log/powersoftplus.log

%files psmain
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/psmain

%files netclient
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/netclient
