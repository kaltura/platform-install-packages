%define prefix /opt/kaltura
Summary: Library for decoding ATSC A/52 (aka AC-3) audio streams
Name: kaltura-a52dec
Version: 0.7.4
Release: 10 
License: GPL
Group: Applications/Multimedia
URL: http://liba52.sourceforge.net/
Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://liba52.sourceforge.net/files/a52dec-%{version}.tar.gz
Patch0: a52dec-0.7.4-PIC.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc-c++
BuildRequires: autoconf >= 2.52, automake, libtool
Provides: a52dec = %{version}

%description
liba52 is a free library for decoding ATSC A/52 streams. It is released
under the terms of the GPL license. The A/52 standard is used in a
variety of applications, including digital television and DVD. It is
also known as AC-3.


%package devel
Summary: Development header files and static library for liba52
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
liba52 is a free library for decoding ATSC A/52 streams. It is released
under the terms of the GPL license. The A/52 standard is used in a
variety of applications, including digital television and DVD. It is
also known as AC-3.

These are the header files and static libraries from liba52 that are needed
to build programs that use it.


%prep
%setup -qn a52dec-%{version}
%patch0 -p1 -b .PIC


%build
%{__libtoolize} --force
%{__aclocal}
%{__automake} -a
%{__autoconf}
./configure --enable-shared --prefix=%{prefix}
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.conf.so.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.conf.so.d/kaltura_a52dec.conf << EOF
%{prefix}/lib
EOF


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING doc/liba52.txt HISTORY NEWS README TODO
%config %{_sysconfdir}/ld.conf.so.d/kaltura_a52dec.conf
%{prefix}/bin/*
%{prefix}/lib/*.so*
%{prefix}/share/man/man1/*


%files devel
%defattr(-, root, root, 0755)
%{prefix}/include/*
%{prefix}/lib/*.a
%exclude %{prefix}/lib/*.la


%changelog
* Sun Jan 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> 0.7.4-10
- Create a file under /etc/ld.conf.so.d so.
 
* Sun Jan 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> 0.7.4-9
- Adopted for Kaltura. Required for kaltura-ffmpeg. 

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 0.7.4-8 - 7981+/dag
- Release bump to drop the disttag number in FC5 build.

* Thu Nov  4 2004 Matthias Saou <http://freshrpms.net/> 0.7.4-7
- Enable -fPIC on all architectures.

* Sat May 29 2004 Dag Wieers <dag@wieers.com> - 0.7.4-7
- Added -fPIC patch for non ix86 architectures.

* Tue May 18 2004 Matthias Saou <http://freshrpms.net/> 0.7.4-7
- Rebuilt for Fedora Core 2.

* Thu Mar  4 2004 Matthias Saou <http://freshrpms.net/> 0.7.4-6
- Rebuilt.

* Thu Feb 26 2004 Matthias Saou <http://freshrpms.net/> 0.7.4-5
- Added the building of the shared library.

* Sun Nov  2 2003 Matthias Saou <http://freshrpms.net/> 0.7.4-4
- Rebuild for Fedora Core 1.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.
- Exclude .la file.

* Thu Sep 26 2002 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 8.0.
- Added SMP build macro.

* Mon Jul 29 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.7.4.

* Sun Mar 24 2002 Matthias Saou <http://freshrpms.net/>
- Fixed the devel file ownership error.

* Tue Mar 19 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.7.3.

* Mon Dec 17 2001 Matthias Saou <http://freshrpms.net/>
- Update to 0.7.2.

* Mon Oct 29 2001 Matthias Saou <http://freshrpms.net/>
- Spec file cleanup and fixes.

* Thu Sep 20 2001 Martin Norbäck <d95mback@dtek.chalmers.se>
- Added missing .la files
- Building statically

* Thu Sep 20 2001 Martin Norbäck <d95mback@dtek.chalmers.se>
- Initial version

