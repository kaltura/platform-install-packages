Name:          libip2location
Version:       8.0.8
Release:       1
Summary:       IP2Location C library enables the user to find the country, region, city, coordinates, etc 
Group:         System/Libraries
URL:           https://github.com/chrislim2888/IP2Location-C-Library 
Source:        %{name}-%{version}.tar.gz
License:	MIT
#BuildRequires: nasm
## AUTOBUILDREQ-BEGIN
BuildRequires: glibc-devel
## AUTOBUILDREQ-END
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
IP2Location C library enables the user to find the country, region, city, 
coordinates, zip code, time zone, ISP, domain name, connection type, area code,
 weather station code, weather station name, mobile, usage types, etc that any IP address or hostname originates from

%package devel
Summary:       Static library, headers and documentation of the IP2Location lib 
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}

%description devel

This package contains the static library, header files and API documentation needed to build applications that will use the IP2location lib 

%prep
%setup -q -n IP2Location-C-Library-%{version} 

%build
autoreconf -i -v --force
%configure
make

%install
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"
%makeinstall
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/ip2location
cp -r data  $RPM_BUILD_ROOT%{_datadir}/ip2location 

# fixup strange shared library permissions
chmod 755 %{buildroot}%{_libdir}/*.so*

%clean
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/*.so.*
%{_datadir}/ip2location
%doc AUTHORS LICENSE.TXT COPYING NEWS 

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%doc ChangeLog README.md Developers_Guide.txt

%changelog
* Wed Jul 31 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 8.0.8-1
- Initial release
