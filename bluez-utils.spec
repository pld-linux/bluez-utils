Summary: Bluetooth utilities 
Name: bluez-utils
Version: 2.2
Release: 2
Copyright: GPL
Group: Applications/System
Source: http://bluez.sourceforge.net/%{name}-%{version}.tar.gz
Patch: bluez-utils-build.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
URL: http://bluez.sourceforge.net
BuildRequires: bluez-libs-devel >= 2.0
ExcludeArch: s390 s390x

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
%patch -p1

%build
%configure --with-bluez-libs=%{_libdir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README
/etc/rc.d/init.d/bluetooth
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man*/*
%dir %{_sysconfdir}/bluetooth/
%config %{_sysconfdir}/bluetooth/*
%config %{_sysconfdir}/pcmcia/bluetooth.conf
%config %{_sysconfdir}/pcmcia/bluetooth

%changelog
* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Jan 19 2003 Matt Wilson <msw@redhat.com> 2.2-1
- configure with --with-bluez-libs=%%{_libdir}

* Fri Jan 17 2003 Bill Nottingham <notting@redhat.com> 2.2-1
- adapt upstream rpm

* Tue Aug 13 2002 Sebastian Frankfurt <sf@infesto.de>
- Initial RPM
