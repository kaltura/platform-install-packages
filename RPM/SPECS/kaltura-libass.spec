%define prefix /opt/kaltura
Summary: Portable library for SSA/ASS subtitles rendering
Name: kaltura-libass
Version: 0.9.11
Release: 2 
License: GPLv2+
Group: System Environment/Libraries
URL: http://code.google.com/p/libass/

Source0: http://libass.googlecode.com/files/libass-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

#BuildRequires: enca-devel
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: libpng-devel

%description
Libass is a portable library for SSA/ASS subtitles rendering.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -qn libass-%{version}

%build
./configure --disable-static --disable-enca --prefix=%{prefix}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/kaltura_libass.conf << EOF
%{prefix}/lib
EOF

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%config %{_sysconfdir}/ld.so.conf.d/kaltura_libass.conf
%defattr(-, root, root, 0755)
%doc Changelog COPYING
%{prefix}/lib/libass.so.*

%files devel
%defattr(-, root, root, 0755)
%{prefix}/include/ass/
%{prefix}/lib/libass.so
%{prefix}/lib/pkgconfig/libass.pc
%exclude %{prefix}/lib/libass.la

%changelog
* Sun Jan 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 0.9.11-2
- Initial package.
