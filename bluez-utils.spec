Summary:	Bluetooth utilities
Summary(pl):	Narzêdzia Bluetooth
Name:		bluez-utils
Version:	3.5
Release:	1
Epoch:		0
License:	GPL v2
Group:		Applications/System
#Source0Download: http://www.bluez.org/download.html
Source0:	http://bluez.sourceforge.net/download/%{name}-%{version}.tar.gz
# Source0-md5:	1816753771a9949e0589a3e8631d46b5
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}-udev.rules
Source4:	%{name}-udev.script
Patch0:		%{name}-etc_dir.patch
URL:		http://www.bluez.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	bluez-libs-devel >= 3.5
BuildRequires:	dbus-glib-devel >= 0.35
BuildRequires:	libtool
BuildRequires:	libusb-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
# for future use (ALSA plugins not finished)
#BuildRequires:	alsa-lib-devel >= 0.9
# for future use (fuse module is just testing stub now)
#BuildRequires:	libfuse-devel
#BuildRequires:	openobex-devel >= 1.1
Requires:	bluez-libs >= 3.5
Requires:	rc-scripts
Obsoletes:	bluez-pan
Obsoletes:	bluez-sdp
Obsoletes:	bluez-utils-init
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
Requires:	bluez-libs >= 3.5
Requires:	cups

%description -n cups-backend-bluetooth
Bluetooth backend for CUPS.

%description -n cups-backend-bluetooth -l pl
Backend Bluetooth dla CUPS-a.

%package init
Summary:	Init script for Bluetooth subsystem
Summary(pl):	Skrypt init dla podsystemu Bluetooth
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description init
Init script for Bluetooth subsystem.

%description init -l pl
Skrypt init dla podsystemu Bluetooth.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-avctrl \
	--enable-bccmd \
	--enable-cups \
	--enable-dfutool \
	--enable-pcmciarules \
	--with-cups=/usr
%{__make} \
	cupsdir=%{cupsdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install -d $RPM_BUILD_ROOT{/etc/udev/rules.d,/lib/udev}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	cupsdir=%{cupsdir} \
	udevdir=/lib/udev

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/bluetooth
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/bluetooth
install %{SOURCE3} $RPM_BUILD_ROOT/etc/udev/rules.d/70-bluetooth.rules
install %{SOURCE4} $RPM_BUILD_ROOT/lib/udev/bluetooth.sh

mv $RPM_BUILD_ROOT/etc/udev/bluetooth.rules \
	$RPM_BUILD_ROOT/etc/udev/rules.d/71-bluetooth.rules

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add bluetooth
%service bluetooth restart

%preun init
if [ "$1" = "0" ]; then
	%service bluetooth stop
	/sbin/chkconfig --del bluetooth
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*

%attr(754,root,root) /etc/rc.d/init.d/bluetooth
%attr(755,root,root) /lib/udev/bluetooth.sh
%attr(755,root,root) /lib/udev/bluetooth_serial
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/70-bluetooth.rules
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/71-bluetooth.rules

%dir /etc/bluetooth
%dir /etc/sysconfig/bluetooth
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/bluetooth
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/*

%files -n cups-backend-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/lib/cups/backend/bluetooth
