%define prefix /opt/kaltura
%define real_name mcrypt

Summary: Data encryption library
Name: kaltura-libmcrypt
Version: 2.5.8
Release: 2 
License: LGPL
Group: System Environment/Libraries
URL: http://mcrypt.sourceforge.net/

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc. 

Source: http://dl.sf.net/mcrypt/libmcrypt-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Provides: libmcrypt = %{version}

BuildRequires: libtool >= 1.3.4

%description
libmcrypt is a data encryption library. The library is thread safe
and provides encryption and decryption functions. This version of the
library supports many encryption algorithms and encryption modes. Some
algorithms which are supported:
SERPENT, RIJNDAEL, 3DES, GOST, SAFER+, CAST-256, RC2, XTEA, 3WAY,
TWOFISH, BLOWFISH, ARCFOUR, WAKE and more.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Provides: libmcrypt-devel = %{version}
%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -qn libmcrypt-%{version}

%build
./configure \
	--prefix=%{prefix} \
	--program-prefix="%{?_program_prefix}" \
	--disable-dependency-tracking \
	--enable-static \
	--mandir=%{prefix}/share/man
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
%{__make} install DESTDIR="%{buildroot}"
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/kaltura_libmcrypt.conf << EOF
%{prefix}/lib
EOF


%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING.LIB KNOWN-BUGS NEWS README THANKS TODO
%{prefix}/lib/*.so*

%files devel
%defattr(-, root, root, 0755)
%doc doc/README* doc/example.c
%doc %{prefix}/share/man/man?/*
%config %{_sysconfdir}/ld.so.conf.d/kaltura_libmcrypt.conf
%{prefix}/bin/*
%{prefix}/lib/*.a
#%{prefix}/lib/*.so
%{prefix}/include/*
%{prefix}/share/aclocal/*.m4
%exclude %{prefix}/lib/*.la

%changelog
* Mon Dec 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 2.5.8-1
- Bounce to 2.5.8

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 2.5.7-5
- Corrected LD_LIBRARY_PATH

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 2.5.7-4
- Added 'Provides'.

* Wed Dec 25 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 2.5.7-3 
- Adopted for Kaltura.

* Sat Apr 08 2006 Dries Verachtert <dries@ulyssis.org> - 2.5.7-1.2 - 7981/dag
- Rebuild for Fedora Core 5.

* Fri Apr 16 2004 ---
- Updated URL and Source tags. (Russ Herrold)

* Wed Jul 30 2003 Dag Wieers <dag@wieers.com> - 2.5.7-1
- Added static library.

* Thu Apr 17 2003 Dag Wieers <dag@wieers.com> - 2.5.7-0
- Updated to release 2.5.7.

* Fri Feb 21 2003 Dag Wieers <dag@wieers.com> - 2.5.6-0
- Updated to release 2.5.6.
- Fixed the --program-prefix problem.

* Tue Jan 07 2003 Dag Wieers <dag@wieers.com> - 2.5.5-0
- Initial package. (using DAR)
