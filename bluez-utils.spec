Summary:	Bluetooth utilities
Name:		bluez-utils
Version:	2.2
Release:	2
License:	GPL
Group:		Applications/System
Source0:	http://bluez.sourceforge.net/download/%{name}-%{version}.tar.gz
#Patch0:		%{name}-build.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
URL:		http://bluez.sourceforge.net
BuildRequires:	bluez-libs-devel >= 2.0
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
#%patch -p1

%build
%configure2_13 --with-bluez-libs=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README
/etc/rc.d/init.d/bluetooth
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
%dir %{_sysconfdir}/bluetooth/
%config %{_sysconfdir}/bluetooth/*
%config %{_sysconfdir}/pcmcia/bluetooth.conf
%config %{_sysconfdir}/pcmcia/bluetooth
