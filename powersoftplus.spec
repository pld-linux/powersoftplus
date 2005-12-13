Summary:	EVER UPS monitoring utilities
Summary(pl):	Narzêdzia do monitorowania zasilaczy awaryjnych UPS firmy EVER
Name:		powersoftplus
Version:	0.1.3
Release:	1
License:	GPL
Group:		Daemons
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	37e700a1f6d918662b2a239570d06111
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

%description -l pl
Ten zestaw programów s³u¿y do monitorowania pracy zasilaczy awaryjnych
UPS firmy EVER Sp. z o.o. o oznaczeniu DPC.

%prep
%setup -q

%build
%configure \
	--bindir=%{_sbindir}

sed -i -e 's#CONFIG_PATH.*#CONFIG_PATH	"%{_sysconfdir}"#g' config.h

%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	DEBUG="%{rpmcflags} -I/usr/include/ncurses" \
	PIXPATH="%{_datadir}/%{name}" \

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	CONFPATH=$RPM_BUILD_ROOT%{_sysconfdir} \
	PIXPATH=$RPM_BUILD_ROOT%{_datadir}/%{name} \
	DESTDIR=$RPM_BUILD_ROOT

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
