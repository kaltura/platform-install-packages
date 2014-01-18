%define prefix /opt/kaltura
Summary: LAME Ain't an MP3 Encoder... but it's the best of all
Name: kaltura-lame
Version: 3.99.5
Release: 2
License: LGPL
Group: Applications/Multimedia
URL: http://lame.sourceforge.net/

Source: http://dl.sf.net/project/lame/lame/3.99/lame-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++
BuildRequires: gtk2-devel
BuildRequires: libtool
BuildRequires: libvorbis-devel
BuildRequires: ncurses-devel
%{?!_without_selinux:BuildRequires: prelink}
%ifarch %{ix86} x86_64
BuildRequires: nasm
%endif
Provides: mp3encoder

### Compatibility with ATrpms :-(
Provides: libmp3lame0 = %{version}-%{release}
Obsoletes: libmp3lame0 < %{version}-%{release}

%description
LAME is an educational tool to be used for learning about MP3 encoding.  The
goal of the LAME project is to use the open source model to improve the
psychoacoustics, noise shaping and speed of MP3. Another goal of the LAME
project is to use these improvements for the basis of a patent-free audio
compression codec for the GNU project.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

### Compatibility with ATrpms
Provides: libmp3lame0-devel = %{version}-%{release}
Obsoletes: libmp3lame0-devel < %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -qn lame-%{version}

%build
./configure \
    --prefix=%{prefix} \
    --disable-dependency-tracking \
    --disable-static \
    --program-prefix="%{?_program_prefix}" \
%ifarch %{ix86} x86_64
    --enable-nasm \
%endif
    --enable-analyser="no" \
    --enable-brhist \
    --enable-decoder \
    --with-vorbis
%{__make} test CFLAGS="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/kaltura_lame.sh << EOF
PATH=\$PATH:%{base_prefix}/bin
export PATH
EOF
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/kaltura_lame.conf << EOF
%{base_prefix}-%{version}/lib
EOF

### Some apps still expect to find <lame.h>
%{__ln_s} -f lame/lame.h %{buildroot}%{prefix}/include/lame.h

### Clean up documentation to be included
find doc/html -name "Makefile*" | xargs rm -f
%{__rm} -rf %{buildroot}%{_docdir}/lame/

### Clear not needed executable stack flag bit
execstack -c %{buildroot}%{prefix}/lib/*.so.*.*.* || :

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING INSTALL* doc/html/
%doc LICENSE README TODO USAGE
#%doc %{prefix}/share/man/man1/lame.1*
%doc %{prefix}/share/*
%{prefix}/bin/lame
%{prefix}/lib/libmp3lame.so.*
%config %{_sysconfdir}/ld.so.conf.d/kaltura_lame.conf
%config %{_sysconfdir}/profile.d/kaltura_lame.sh

%files devel
%defattr(-, root, root, 0755)
%doc API DEFINES HACKING STYLEGUIDE
%{prefix}/include/lame/
%{prefix}/include/lame.h
%{prefix}/lib/libmp3lame.so
%exclude %{prefix}/lib/libmp3lame.la

%changelog
* Mon Feb 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.16-2
- Adopted for Kaltura.

* Sun Mar 11 2012 Dag Wieers <dag@wieers.com> - 3.99.5-1
- Updated to release 3.99.5.

* Tue Jan 31 2012 Dag Wieers <dag@wieers.com> - 3.99.4-2
- Added compatibility with ATrpms.

* Sun Jan 29 2012 Dag Wieers <dag@wieers.com> - 3.99.4-1
- Updated to release 3.99.4.

* Tue Jul 06 2010 Steve Huff <shuff@vecna.org> - 3.98.4-1
- Updated to release 3.98.4 (thanks Brandon Ooi!).
- Captured libvorbis and gtk2 dependencies.

* Mon Nov 10 2008 Dag Wieers <dag@wieers.com> - 3.98.2-1
- Updated to release 3.98.2.

* Mon Oct 16 2006 Matthias Saou <http://freshrpms.net/> 3.97-1
- Update to 3.97.

* Wed May 17 2006 Matthias Saou <http://freshrpms.net/> 3.96.1-5
- Clear not needed executable stack flag bit from the library to make it work
  with selinux, add prelink build requirement (need to remove for old distros).

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 3.96.1-4
- Release bump to drop the disttag number in FC5 build.
- Disable/remove static lib.

* Thu Dec 15 2005 Matthias Saou <http://freshrpms.net/> 3.96.1-3
- Remove the use off _smp_mflags, as build fails on i386 with -j4 (but didn't
  on x86_64, strange).

* Fri Nov  5 2004 Matthias Saou <http://freshrpms.net/> 3.96.1-2
- Remove complex CFLAGS, recent compilers already do a grrreat job.

* Mon Sep  6 2004 Matthias Saou <http://freshrpms.net/> 3.96.1-1
- Update to 3.96.1.

* Wed Apr 21 2004 Matthias Saou <http://freshrpms.net/> 3.96-1
- Update to 3.96 w/ spec changes from Dag.

* Tue Jan 13 2004 Matthias Saou <http://freshrpms.net/> 3.95.1-1
- Update to 3.95.1.

* Sun Nov  2 2003 Matthias Saou <http://freshrpms.net/> 3.93.1-3
- Rebuild for Fedora Core 1.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.
- Exclude .la file.

* Mon Jan 13 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.93.1.
- Removed Epoch: tag, upgrade by hand! :-/

* Sat Oct  5 2002 Matthias Saou <http://freshrpms.net/>
- Fix unpackaged doc problem.

* Fri Sep 27 2002 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 8.0.
- Simplified deps as it now builds VBR code fine with default nasm and gcc 3.2.

* Tue Jul 16 2002 Matthias Saou <http://freshrpms.net/>
- Fix to the lamecc stuff.

* Wed Jul 10 2002 Matthias Saou <http://freshrpms.net/>
- Changes to now support ppc with no ugly workarounds.

* Thu May  2 2002 Matthias Saou <http://freshrpms.net/>
- Rebuilt against Red Hat Linux 7.3.
- Added the %%{?_smp_mflags} expansion.

* Wed Apr 24 2002 Matthias Saou <http://freshrpms.net/>
- Update to 3.92.

* Mon Apr  8 2002 Matthias Saou <http://freshrpms.net/>
- Added a symlink from lame.h to lame/lame.h to fix some include file
  detection for most recent programs that use lame.

* Wed Jan  2 2002 Matthias Saou <http://freshrpms.net/>
- Update to 3.91.
- Simplified the compilation optimizations after heavy home-made tests.
- Now build only i386 version but optimized for i686. Don't worry i686
  owners, you loose only 1% in speed but gain about 45% compared to if
  you had no optimizations at all!

* Mon Dec 24 2001 Matthias Saou <http://freshrpms.net/>
- Update to 3.90.1.
- Enabled the GTK+ frame analyzer.
- Spec file cleanup (CVS, man page, bindir are now fixed).

* Fri Nov 16 2001 Matthias Saou <http://freshrpms.net/>
- Rebuilt with mpg123 decoding support.

* Tue Oct 23 2001 Matthias Saou <http://freshrpms.net/>
- Fixed the %pre and %post that should have been %post and %postun, silly me!
- Removed -malign-double (it's evil, Yosi told me and I tested, brrr ;-)).
- Now build with gcc3, VBR encoding gets a hell of a boost, impressive!
  I recommend you now use "lame --r3mix", it's the best.
- Tried to re-enable vorbis, but it's a no-go.

* Thu Jul 26 2001 Matthias Saou <http://freshrpms.net/>
- Build with kgcc to have VBR working.

* Wed Jul 25 2001 Matthias Saou <http://freshrpms.net/>
- Update to 3.89beta : Must be built with a non-patched version of nasm
  to work!

* Mon May  7 2001 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat 7.1.
- Disabled the vorbis support since it fails to build with it.
- Added a big optimisation section, thanks to Yosi Markovich
  <senna@camelot.com> for this and other pointers.

* Sun Feb 11 2001 Matthias Saou <http://freshrpms.net/>
- Split the package, there is now a -devel

* Thu Oct 26 2000 Matthias Saou <http://freshrpms.net/>
- Initial RPM release for RedHat 7.0 from scratch

