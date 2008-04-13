Summary:	Bluetooth utilities
Summary(pl.UTF-8):	Narzędzia Bluetooth
Name:		bluez-utils
Version:	3.30
Release:	1
Epoch:		0
License:	GPL v2+
Group:		Applications/System
#Source0Download: http://www.bluez.org/download.html
Source0:	http://bluez.sourceforge.net/download/%{name}-%{version}.tar.gz
# Source0-md5:	3d17bb712d243bb1b316f7e8a909fa82
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}-udev.rules
Source4:	%{name}-udev.script
Patch0:		%{name}-etc_dir.patch
URL:		http://www.bluez.org/
BuildRequires:	alsa-lib-devel >= 1.0.10-1
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	bluez-libs-devel >= 3.30
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
BuildRequires:	hal-devel >= 0.5.8
#BuildRequires:	libopensync-devel < 0.30
BuildRequires:	libtool
BuildRequires:	libusb-devel
BuildRequires:	openobex-devel >= 1.1
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	bluez-libs >= 3.30
Requires:	rc-scripts
Obsoletes:	bluez-pan
Obsoletes:	bluez-sdp
Obsoletes:	bluez-utils-init
Conflicts:	bluez-bluefw
ExcludeArch:	s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# currently lib, not %{_lib} (see cups.spec)
%define		cupsdir		/usr/lib/cups/backend
%define		udevdir		/%{_lib}/udev

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

%description -l pl.UTF-8
Narzędzia Bluetooth:
 - hcitool
 - hciattach
 - hciconfig
 - hcid
 - l2ping
 - skrypty startowe (PLD)
 - pliki konfiguracji PCMCIA

Znaki towarowe BLUETOOTH są własnością Bluetooth SIG, Inc. z USA.

%package -n alsa-plugins-bluetooth
Summary:	ALSA plugins for Bluetooth audio devices
Summary(pl.UTF-8):	Wtyczki systemu ALSA dla urządzeń dźwiękowych Bluetooth
Group:		Libraries
# bluetoothd + audio service
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	alsa-lib >= 1.0.10-1

%description -n alsa-plugins-bluetooth
ALSA plugins for Bluetooth audio devices.

%description -n alsa-plugins-bluetooth -l pl.UTF-8
Wtyczki systemu ALSA dla urządzeń dźwiękowych Bluetooth.

%package -n cups-backend-bluetooth
Summary:	Bluetooth backend for CUPS
Summary(pl.UTF-8):	Backend Bluetooth dla CUPS-a
Group:		Applications/Printing
Requires:	bluez-libs >= 3.30
Requires:	cups

%description -n cups-backend-bluetooth
Bluetooth backend for CUPS.

%description -n cups-backend-bluetooth -l pl.UTF-8
Backend Bluetooth dla CUPS-a.

%package -n gstreamer-bluetooth
Summary:	Bluetooth support for gstreamer
Summary(pl.UTF-8):	Obsługa Bluetooth dla gstreamera
Group:		Libraries
Requires:	bluez-libs >= 3.30
Requires:	gstreamer >= 0.10
Requires:	gstreamer-plugins-base >= 0.10

%description -n gstreamer-bluetooth
Bluetooth support for gstreamer.

%description -n gstreamer-bluetooth -l pl.UTF-8
Obsługa Bluetooth dla gstreamera.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-alsa \
	--enable-audio \
	--enable-avctrl \
	--enable-bccmd \
	--enable-cups \
	--enable-dfutool \
	--enable-glib \
	--enable-gstreamer \
	--enable-hal \
	--enable-hid2hci \
	--enable-input \
	--enable-network \
	--enable-obex \
	--enable-pcmciarules \
	--enable-sdpd \
	--enable-serial \
	--disable-sync \
	--enable-test \
	--enable-usb \
	--with-cups=/usr

%{__make} \
	cupsdir=%{cupsdir} \
	udevdir=%{udevdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install -d $RPM_BUILD_ROOT{/etc/udev/rules.d,%{udevdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	cupsdir=%{cupsdir} \
	udevdir=%{udevdir}

# noinst
#install sync/bluetoothd-service-sync $RPM_BUILD_ROOT%{_libdir}/bluetooth

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/bluetooth
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/bluetooth
install %{SOURCE3} $RPM_BUILD_ROOT/etc/udev/rules.d/70-bluetooth.rules
install %{SOURCE4} $RPM_BUILD_ROOT%{udevdir}/bluetooth.sh
install daemon/passkey-agent $RPM_BUILD_ROOT/%{_bindir}
mv $RPM_BUILD_ROOT/etc/udev/bluetooth.rules \
	$RPM_BUILD_ROOT/etc/udev/rules.d/71-bluetooth.rules

rm -f $RPM_BUILD_ROOT%{_libdir}/alsa-lib/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/bluetooth/plugins/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer*/libgstbluetooth.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add bluetooth
%service bluetooth restart

%preun
if [ "$1" = "0" ]; then
	%service bluetooth stop
	/sbin/chkconfig --del bluetooth
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README audio/audio-api.txt daemon/hal-namespace.txt hcid/dbus-api.txt input/input-api.txt network/network-api.txt serial/serial-api.txt
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/bluetooth
%dir %{_libdir}/bluetooth/plugins
%attr(755,root,root) %{_libdir}/bluetooth/plugins/*.so
%dir %{_sysconfdir}/bluetooth
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/hcid.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/rfcomm.conf
%attr(754,root,root) /etc/rc.d/init.d/bluetooth
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/bluetooth
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/bluetooth.conf
%attr(755,root,root) %{udevdir}/bluetooth.sh
%attr(755,root,root) %{udevdir}/bluetooth_serial
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/70-bluetooth.rules
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/71-bluetooth.rules
%{_mandir}/man[18]/*
%{_mandir}/man5/hcid.conf.5*

%files -n alsa-plugins-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/alsa-lib/libasound_module_ctl_bluetooth.so
%attr(755,root,root) %{_libdir}/alsa-lib/libasound_module_pcm_bluetooth.so

%files -n cups-backend-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/lib/cups/backend/bluetooth

%files -n gstreamer-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gstreamer*/libgstbluetooth.so
