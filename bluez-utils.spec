Summary:	Bluetooth utilities
Summary(pl):	Narz�dzia Bluetooth
Name:		bluez-utils
Version:	2.2
Release:	3
License:	GPL v2
Group:		Applications/System
Source0:	http://bluez.sourceforge.net/download/%{name}-%{version}.tar.gz
Patch0:		%{name}-etc_dir.patch
URL:		http://bluez.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bluez-libs-devel >= 2.0
BuildRequires:	libtool
Requires(post,preun):	/sbin/chkconfig
ExcludeArch:	s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bluetooth utilities (bluez-utils):
 - hcitool
 - hciattach
 - hciconfig
 - hcid
 - l2ping
 - start scripts (PLD)
 - PCMCIA configuration files

The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%description -l pl
Narz�dzia Bluetooth (bluez-utils):
 - hcitool
 - hciattach
 - hciconfig
 - hcid
 - l2ping
 - skrypty startowe (PLD)
 - pliki konfiguracji PCMCIA
 
%prep
%setup -q
%patch0 -p1

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
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	confdir=%{_sysconfdir}/bluetooth \
	mandir=%{_mandir}

%{__make} -C scripts \
	DESTDIR=$RPM_BUILD_ROOT \
	redhat

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add bluetooth
if [ -f /var/lock/subsys/bluetooth ]; then
	/etc/rc.d/init.d/bluetooth restart >&2
else
	echo "Run \"/etc/rc.d/init.d/bluetooth\" to start bluetooth." >&2
fi

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
%attr(754,root,root) /etc/rc.d/init.d/bluetooth
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
%dir %{_sysconfdir}/bluetooth
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bluetooth/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/bluetooth.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/bluetooth
