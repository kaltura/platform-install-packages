%define prefix /opt/kaltura
%define snap_date 20140104

Summary: Library for encoding and decoding H264/AVC video streams
Name: kaltura-x264
Version: 0.140
Release: 2.%{snap_date}
License: GPL
Group: System Environment/Libraries
URL: http://developers.videolan.org/x264.html
Source: http://downloads.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-%{snap_date}-2245.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gettext
BuildRequires: nasm
BuildRequires: yasm
BuildRequires: perl-Digest-MD5-File
#BuildRequires: kaltura-ffmpeg-devel
%{?_with_visualize:%{!?_without_modxorg:BuildRequires: libXt-devel}}
%{?_with_visualize:%{?_without_modxorg:BuildRequires: XFree86-devel}}
Provides: x264, libx264

Obsoletes: x264-gtk <= %{version}-%{release}

%description
Utility and library for encoding H264/AVC video streams.

%package devel
Summary: Development files for the x264 library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, pkgconfig
Obsoletes: x264-gtk-devel <= %{version}-%{release}

%description devel
This package contains the files required to develop programs that will encode
H264/AVC video streams using the x264 library.

%prep
%setup -qn x264-snapshot-%{snap_date}-2245
# configure hardcodes X11 lib path
sed -i 's|/usr/X11R6/lib |/usr/X11R6/%{prefix}/lib |g' configure


%build
# Force PIC as applications fail to recompile against the lib on x86_64 without
./configure \
    --prefix="%{prefix}" \
%{?_without_asm:--disable-asm} \
    --enable-debug \
    --enable-pic \
    --enable-pthread \
    --enable-shared \
%{?_with_visualize:--enable-visualize} \
    --extra-cflags="%{optflags}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/kaltura_x264.conf << EOF
%{prefix}/lib
EOF

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING
%{prefix}/bin/x264
%{prefix}/lib/libx264.so.*
%config %{_sysconfdir}/ld.so.conf.d/kaltura_x264.conf

%files devel
%defattr(-, root, root, 0755)
%doc doc/*.txt
%{prefix}/include/x264.h
%{prefix}/include/x264_config.h
%{prefix}/lib/pkgconfig/x264.pc
%{prefix}/lib/libx264.so

%changelog
* Sun Jan 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> 0.140-2.20140104 
- Added %%{_sysconfdir}/ld.so.conf.d/kaltura_x264.conf
* Sun Jan 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> 0.140-1.20140104 
- Adopted for Kaltura. Required for kaltura-ffmpeg. 

* Mon Nov 15 2010 Dag Wieers <dag@wieers.com> - 0.0.0-0.4.20101111
- Updated to git release 20101111 (soname .107).

* Wed Jul 08 2009 Dag Wieers <dag@wieers.com> - 0.0.0-0.4.20090708
- Updated to git release 20090708 (soname .68).

* Wed May 30 2007 Matthias Saou <http://freshrpms.net/> 0.0.0-0.4.20070529
- Update to 20070529 snasphot for F7 (soname .54 bump to .55).
- Add missing ldconfig calls for the gtk sub-package.

* Fri Dec 15 2006 Matthias Saou <http://freshrpms.net/> 0.0.0-0.3.20061214
- Update to 20061214 snapshot (same soname, no rebuilds required).

* Tue Oct 24 2006 Matthias Saou <http://freshrpms.net/> 0.0.0-0.3.20061023
- Update to 20061023 snapshot, the last was too old for MPlayer 1.0rc1.
- Remove no longer needed gtk patch.

* Mon Sep 18 2006 Matthias Saou <http://freshrpms.net/> 0.0.0-0.2.20060731
- Update to 20060917 snapshot.

* Tue Aug  1 2006 Matthias Saou <http://freshrpms.net/> 0.0.0-0.2.20060731
- Update to 20060731 snapshot.
- Require the main package from the devel since we have a shared lib now.
- Remove no longer needed symlink patch.
- Enable gtk, include patch to have it build, and split off sub-packages.

* Thu Jun  8 2006 Matthias Saou <http://freshrpms.net/> 0.0.0-0.2.20060607
- Switch to using the official snapshots.
- Remove no longer needed UTF-8 AUTHORS file conversion.
- Simplify xorg build requirement.
- Switch from full %%configure to ./configure with options since no autotools.
- Enable shared library at last.
- Add our %%{optflags} to the build.
- Include patch to make the *.so symlink relative.

* Thu Mar 16 2006 Matthias Saou <http://freshrpms.net/> 0.0.0-0.1.svn468
- Update to svn 468.
- Lower version from 0.0.svn to 0.0.0 since one day 0.0.1 might come out,
  this shouldn't be much of a problem since the lib is only statically linked,
  thus few people should have it installed, and build systems which aren't
  concerned about upgrade paths should get the latest available package.

* Thu Feb 23 2006 Matthias Saou <http://freshrpms.net/> 0.0.439-1
- Update to svn 439.

* Thu Jan 12 2006 Matthias Saou <http://freshrpms.net/> 0.0.396-2
- Enable modular xorg conditional build.

* Mon Jan  9 2006 Matthias Saou <http://freshrpms.net/> 0.0.396-1
- Update to svn 396.

* Tue Nov 29 2005 Matthias Saou <http://freshrpms.net/> 0.0.380-2
- Also force PIC for the yasm bits, thanks to Anssi Hannula.

* Tue Nov 29 2005 Matthias Saou <http://freshrpms.net/> 0.0.380-1
- Update to svn 380.
- Force PIC as apps fail to recompile against the lib on x86_64 without.
- Include new pkgconfig file.

* Tue Oct  4 2005 Matthias Saou <http://freshrpms.net/> 0.0.315-1
- Update to svn 315.
- Disable vizualize since otherwise programs trying to link without -lX11 will
  fail (cinelerra in this particular case).

* Mon Aug 15 2005 Matthias Saou <http://freshrpms.net/> 0.0.285-1
- Update to svn 285.
- Add yasm build requirement (needed on x86_64).
- Replace X11 lib with lib/lib64 to fix x86_64 build.

* Tue Aug  2 2005 Matthias Saou <http://freshrpms.net/> 0.0.281-1
- Update to svn 281.

* Mon Jul 11 2005 Matthias Saou <http://freshrpms.net/> 0.0.273-1
- Initial RPM release.

