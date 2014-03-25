%define prefix /opt/kaltura
Summary: Reference encoder and encoding library for MPEG2/4 AAC
Name: kaltura-libfaac
Version: 1.26
Release: 1
License: LGPL
Group: Applications/Multimedia
URL: http://www.audiocoding.com/


Source: http://dl.sf.net/faac/faac-%{version}.tar.gz
Patch0: faac-1.25-libmp4v2.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: libmp4v2-devel
BuildRequires: autoconf >= 2.50, automake, libtool, dos2unix, gcc-c++

%description
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

%package devel
Summary: Development libraries of the FAAC AAC encoder
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Provides: faac = %{name}-%{version}

%description devel
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

This package contains development files and documentation for libfaac.

%prep
%setup -n faac 
#patch0 -p1 -b .libmp4v2
# Don't ask...
find . -type f -exec dos2unix {} \;
find . -type f -exec chmod 644 {} \;
find . -type d -exec chmod 755 {} \;

%build
sh bootstrap
./configure --prefix=%{prefix} --disable-static \
    --with-mp4v2
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README TODO docs/*
%{prefix}/bin/faac
%{prefix}/lib/libfaac.so.*

%files devel
%defattr(-, root, root, 0755)
%{prefix}/include/faac.h
%{prefix}/include/faaccfg.h
%{prefix}/lib/libfaac.so
%exclude %{prefix}/lib/libfaac.la

%changelog
* Mon Feb 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.26-2
- Adopted for Kaltura, needed for kaltura-ffmpeg.

* Mon Nov 10 2008 Dag Wieers <dag@wieers.com> - 1.26-1 - 7981/dag
- Updated to release 1.26.

* Wed Dec 20 2006 Matthias Saou <http://freshrpms.net/> 1.25-2
- Include patch to fix external libmp4v2 (Alexandre Silva Lopes).

* Fri Dec 15 2006 Matthias Saou <http://freshrpms.net/> 1.25-1
- Update to 1.25.
- Enable external libmp4v2... but the resulting package doesn't require it...

* Wed Apr 12 2006 Matthias Saou <http://freshrpms.net/> 1.24-3
- Add faad2-devel build requirement to build with MP4 support (Chris Petersen),
  faad2 had to be fixed before it worked, though.

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 1.24-2
- Release bump to drop the disttag number in FC5 build.
- Disable/remove static library.

* Tue Aug 24 2004 Matthias Saou <http://freshrpms.net/> 1.24-1
- Fix license tag, it's LGPL not GPL.

* Mon May  3 2004 Matthias Saou <http://freshrpms.net/> 1.24-1
- Update to 1.24.

* Thu Feb 26 2004 Matthias Saou <http://freshrpms.net/> 1.23.5-1
- Update to 1.23.5.
- Changed license tag to GPL.

* Mon Nov 17 2003 Matthias Saou <http://freshrpms.net/> 1.23.1-1
- Initial rpm release.

