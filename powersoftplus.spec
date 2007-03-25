Summary:	EVER UPS monitoring utilities
Summary(pl.UTF-8):	Narzędzia do monitorowania zasilaczy awaryjnych UPS firmy EVER
Name:		powersoftplus
Version:	0.1.8
Release:	0.1
License:	GPL
Group:		Daemons
Source0:	http://www.ever.com.pl/pl/pliki/%{name}-%{version}-x86.tar.gz
# Source0-md5:	e39d39335d7168f1fcf473471a50c35d
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.ever.com.pl/powersoft_prod.php
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	SysVinit
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%description
This package contains some utilities for EVER UPS monitoring.

%description -l pl.UTF-8
Ten zestaw programów służy do monitorowania pracy zasilaczy awaryjnych
UPS firmy EVER Sp. z o.o. o oznaczeniu DPC.

%prep
%setup -q

%build
%configure \
	--bindir=%{_sbindir} \
	--prefix=/usr

sed -i -e 's#CONFIG_PATH.*#CONFIG_PATH	"%{_sysconfdir}"#g' config.h
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	DEBUG="%{rpmcflags} -I/usr/include/ncurses" \
	PIXPATH="%{_datadir}/%{name}" \
	LIBUPATH=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	CONFPATH=$RPM_BUILD_ROOT%{_sysconfdir} \
	PIXPATH=$RPM_BUILD_ROOT%{_datadir}/%{name} \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBUPATH=$RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT{%{_sbindir},/var/{run,log},%{_sysconfdir},/etc/{rc.d/init.d,sysconfig}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/powersoftplus
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/powersoftplus

touch $RPM_BUILD_ROOT/var/log/powersoftplus.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add powersoftplus
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

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/powersoftplus
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/powersoftplus
%{_datadir}/%{name}
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.*
%attr(640,root,root) %ghost /var/log/powersoftplus.log
