Summary:	Bluetooth utilities
Name:		bluez-utils
Version:	2.2
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	http://bluez.sourceforge.net/download/%{name}-%{version}.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
URL:		http://bluez.sourceforge.net
BuildRequires:	bluez-libs-devel >= 2.0
Requires(post,preun):	/sbin/chkconfig
ExcludeArch:	s390 s390x

%description
Bluetooth utilities (bluez-utils):
 - hcitool
 - hciattach
 - hciconfig
 - hcid
 - l2ping
 - start scripts (RedHat)
 - pcmcia configuration files

The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.


%prep
rm -rf $RPM_BUILD_ROOT

%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--enable-pcmcia
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT \
	confdir=%{_sysconfdir}/bluetooth \
	mandir=%{_mandir}
%{__make} -C scripts \
	DESTDIR=$RPM_BUILD_ROOT \
	redhat

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add bluetooth

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/bluetooth ]; then
		/etc/rc.d/init.d/bluetooth stop 1>&2
	fi
	/sbin/chkconfig --del bluetooth
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
/etc/rc.d/init.d/bluetooth
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
%dir %{_sysconfdir}/bluetooth/
%config %{_sysconfdir}/bluetooth/*
%config %{_sysconfdir}/pcmcia/bluetooth.conf
%config %{_sysconfdir}/pcmcia/bluetooth
