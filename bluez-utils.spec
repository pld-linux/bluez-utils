# TODO:
# - check init script, add support for rfcomm bind on startup
#
Summary:	Bluetooth utilities
Summary(pl):	Narzêdzia Bluetooth
Name:		bluez-utils
Version:	2.17
Release:	2
Epoch:		0
License:	GPL v2
Group:		Applications/System
Source0:	http://bluez.sourceforge.net/download/%{name}-%{version}.tar.gz
# Source0-md5:	42be19b0029a83824358baa0106da947
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-etc_dir.patch
Patch1:		%{name}-dbus.patch
Patch2:		%{name}-dbuslate.patch
URL:		http://bluez.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	bluez-libs-devel >= 2.15
BuildRequires:	dbus-devel >= 0.33
BuildRequires:	libtool
BuildRequires:	libusb-devel
# alsa-lib-devel, openobex-devel - currently only checked for, not used
PreReq:		rc-scripts
Requires:	bluez-libs >= 2.15
Obsoletes:	bluez-pan
Obsoletes:	bluez-sdp
Conflicts:	bluez-bluefw
ExcludeArch:	s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# currently lib, not %{_lib} (see cups.spec)
%define		cupsdir		/usr/lib/cups/backend

%description
Bluetooth utilities:
 - hcitool
 - hciattach
 - hciconfig
 - hcid
 - l2ping
 - start scripts (PLD)
 - PCMCIA configuration files

The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%description -l pl
Narzêdzia Bluetooth:
 - hcitool
 - hciattach
 - hciconfig
 - hcid
 - l2ping
 - skrypty startowe (PLD)
 - pliki konfiguracji PCMCIA

%package -n cups-backend-bluetooth
Summary:	Bluetooth backend for CUPS
Summary(pl):	Backend Bluetooth dla CUPS-a
Group:		Applications/Printing
Requires:	bluez-libs >= 2.11
Requires:	cups

%description -n cups-backend-bluetooth
Bluetooth backend for CUPS.

%description -n cups-backend-bluetooth -l pl
Backend Bluetooth dla CUPS-a.

%package init
Summary:	Init script for Bluetooth subsystem
Summary(pl):	Skrypt init dla podsystemu Bluetooth
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires(post,preun):	/sbin/chkconfig

%description init
Init script for Bluetooth subsystem.

%description init -l pl
Skrypt init dla podsystemu Bluetooth.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-bcm203x \
	--enable-cups \
	--enable-pcmcia \
	--with-cups=/usr
%{__make} \
	cupsdir=%{cupsdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	cupsdir=%{cupsdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/bluetooth
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/bluetooth

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add bluetooth
if [ -f /var/lock/subsys/bluetooth ]; then
	/etc/rc.d/init.d/bluetooth restart >&2
else
	echo "Run \"/etc/rc.d/init.d/bluetooth\" to start bluetooth." >&2
fi

%postun init
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/bluetooth ]; then
		/etc/rc.d/init.d/bluetooth stop 1>&2
	fi
	/sbin/chkconfig --del bluetooth
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/bluetooth
%dir %{_sysconfdir}/bluetooth
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bluetooth/*
%attr(755,root,root) %{_sysconfdir}/hotplug/usb/bcm203x
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hotplug/usb/bcm203x.usermap
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/bluetooth.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/bluetooth

%files -n cups-backend-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/lib/cups/backend/bluetooth

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/bluetooth
