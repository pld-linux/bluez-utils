# TODO:
# - check init script, add support for rfcomm bind on startup
#
Summary:	Bluetooth utilities
Summary(pl):	Narzêdzia Bluetooth
Name:		bluez-utils
Version:	2.7
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://bluez.sourceforge.net/download/%{name}-%{version}.tar.gz
# Source0-md5:	5b67e008efa785175cdbc3c8dcdebab2
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-opt.patch
Patch1:		%{name}-etc_dir.patch
Patch2:		%{name}-cups.patch
URL:		http://bluez.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	bluez-libs-devel >= 2.7
BuildRequires:	libtool
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	bluez-libs >= 2.7
Obsoletes:	bluez-sdp
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
Narzêdzia Bluetooth (bluez-utils):
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
Requires:	bluez-libs >= 2.7
Requires:	cups

%description -n cups-backend-bluetooth
Bluetooth backend for CUPS.

%description -n cups-backend-bluetooth -l pl
Backend Bluetooth dla CUPS-a.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# fix path (default prefix was /)
sed -e "s@pin_helper.*bluepin;@pin_helper %{_bindir}/bluepin;@" \
	hcid/hcid.conf > hcid.conf.tmp
mv -f hcid.conf.tmp hcid/hcid.conf

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-pcmcia \
	--with-cups=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/bluetooth
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/bluetooth

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
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
%attr(754,root,root) /etc/rc.d/init.d/bluetooth
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/bluetooth
%dir %{_sysconfdir}/bluetooth
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bluetooth/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/bluetooth.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/bluetooth

%files -n cups-backend-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/lib/cups/backend/bluetooth
