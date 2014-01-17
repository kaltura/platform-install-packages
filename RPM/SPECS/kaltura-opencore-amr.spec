%define prefix /opt/kaltura
Summary: Adaptive Multi-Rate Floating-point (AMR) Speech Codec
Name: kaltura-libopencore-amr
Version: 0.1.2
Release: 1
License: Apache License V2.0
Group: System Environment/Libraries
URL: http://opencore-amr.sourceforge.net/

Source: http://dl.sf.net/project/opencore-amr/opencore-amr/%{version}/opencore-amr-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++

%description
Library of OpenCORE Framework implementation of 3GPP Adaptive Multi-Rate
Floating-point (AMR) Speech Codec (3GPP TS 26.104 V 7.0.0) and 3GPP AMR
Adaptive Multi-Rate - Wideband (AMR-WB) Speech Codec (3GPP TS 26.204
V7.0.0).

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -qn opencore-amr-%{version}

%build
./configure --disable-static --prefix=%{prefix}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/kaltura-libopencore-amrnb.conf << EOF
%{prefix}/lib
EOF

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%config %{_sysconfdir}/ld.so.conf.d/kaltura-libopencore-amrnb.conf
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING LICENSE README
%{prefix}/lib/libopencore-amrnb.so.*
%{prefix}/lib/libopencore-amrwb.so.*

%files devel
%defattr(-, root, root, 0755)
%doc test/*
%{prefix}/include/opencore-amrnb/
%{prefix}/include/opencore-amrwb/
%{prefix}/lib/libopencore-amrnb.so
%{prefix}/lib/libopencore-amrwb.so
%{prefix}/lib/pkgconfig/opencore-amrnb.pc
%{prefix}/lib/pkgconfig/opencore-amrwb.pc
%exclude %{prefix}/lib/libopencore-amrnb.la
%exclude %{prefix}/lib/libopencore-amrwb.la

%changelog
* Sun Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 0.9.11-2
- Initial package.
