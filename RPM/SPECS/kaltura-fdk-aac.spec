%define prefix /usr

Summary: Library for encoding and decoding H264/AVC video streams
Name: kaltura-fdk-aac
Version: 0.1.3
Release: 1
License: GPL
Group: System Environment/Libraries
URL: http://developers.videolan.org/x264.html
Source: https://github.com/mstorsjo/fdk-aac/archive/v%{version}.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Provides: fdk-aac, libfdk-aac


%description
Funhofer FDK AAC Codec Library - runtime files
The FDK AAC Codec Library For Android contains an encoder implementation of the Advanced Audio Coding (AAC) audio codec.

%package devel
Summary: Development files for the Funhofer FDK AAC Codec Library 
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, pkgconfig

%description devel
The FDK AAC Codec Library For Android contains an encoder implementation of the Advanced Audio Coding (AAC) audio codec.

%prep
%setup -qn fdk-aac-%{version} 
autoconf || true
./autogen.sh

%build
# Force PIC as applications fail to recompile against the lib on x86_64 without
./configure \
    --prefix="%{prefix}" 
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/kaltura_fdk-aac.conf << EOF
%{prefix}/lib
EOF

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc ChangeLog NOTICE MODULE_LICENSE_FRAUNHOFER 
%{prefix}/lib/libfdk*.so*
%config %{_sysconfdir}/ld.so.conf.d/kaltura_fdk-aac.conf

%files devel
%defattr(-, root, root, 0755)
%{prefix}/include/fdk-aac
%{prefix}/lib/pkgconfig/*.pc
%{prefix}/lib/*.a
%{prefix}/lib/libfdk-aac.la

%changelog
* Wed Jan 22 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 0.1.3-1
- initial release.
