%global libzen_version  0.4.37
%define prefix /opt/kaltura
%define libname libmediainfo

Name:           kaltura-libmediainfo
Version:        0.7.61
Release:        9
Summary:        Library for supplies technical and tag information about a video or audio file

Group:          System Environment/Libraries
License:        BSD
URL:            http://mediaarea.net/MediaInfo
Source0:        http://mediaarea.net/download/source/%{libname}/%{version}/%{libname}_%{version}.tar.bz2

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libzen) >= %{libzen_version}
BuildRequires:  pkgconfig(zlib)
BuildRequires:  doxygen
BuildRequires:  pkgconfig(libcurl)
#BuildRequires:  pkgconfig(tinyxml2)
Requires: libzen >= %{libzen_version}

Provides:       bundled(md5-plumb)

%description
This package contains the shared library for MediaInfo.
MediaInfo supplies technical and tag information about a video or
audio file.

What information can I get from MediaInfo?
* General: title, author, director, album, track number, date, duration...
* Video: codec, aspect, fps, bitrate...
* Audio: codec, sample rate, channels, language, bitrate...
* Text: language of subtitle
* Chapters: number of chapters, list of chapters

DivX, XviD, H263, H.263, H264, x264, ASP, AVC, iTunes, MPEG-1,
MPEG1, MPEG-2, MPEG2, MPEG-4, MPEG4, MP4, M4A, M4V, QuickTime,
RealVideo, RealAudio, RA, RM, MSMPEG4v1, MSMPEG4v2, MSMPEG4v3,
VOB, DVD, WMA, VMW, ASF, 3GP, 3GPP, 3GP2

What format (container) does MediaInfo support?
* Video: MKV, OGM, AVI, DivX, WMV, QuickTime, Real, MPEG-1,
  MPEG-2, MPEG-4, DVD (VOB) (Codecs: DivX, XviD, MSMPEG4, ASP,
  H.264, AVC...)
* Audio: OGG, MP3, WAV, RA, AC3, DTS, AAC, M4A, AU, AIFF
* Subtitles: SRT, SSA, ASS, SAMI



%package        devel
Summary:        Include files and mandatory libraries for development
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libzen-devel%{?_isa} >= %{libzen_version}

%description    devel
Include files and mandatory libraries for development.


%prep
%setup -q -n MediaInfoLib

cp           Release/ReadMe_DLL_Linux.txt ReadMe.txt
mv           History_DLL.txt History.txt
sed -i 's/.$//' *.txt Source/Example/*

#find . -type f -exec chmod 644 {} ';'

rm -rf Project/MSCS20*
#rm -rf Source/ThirdParty/tinyxml2

%build
pushd Source/Doc/
    doxygen -u Doxyfile
    doxygen Doxyfile
popd
cp Source/Doc/*.html ./

pushd Project/GNU/Library
    sh ./autogen
    ./configure --prefix=%{prefix} --enable-shared
    make %{?_smp_mflags}
popd

%install
pushd Project/GNU/Library
    %make_install
popd
mkdir -p %{buildroot}%{prefix}/include/MediaInfoDLL
install -m 644 -p Source/MediaInfoDLL/MediaInfoDLL.cs %{buildroot}%{prefix}/include/MediaInfoDLL
install -m 644 -p Source/MediaInfoDLL/MediaInfoDLL.JNA.java %{buildroot}%{prefix}/include/MediaInfoDLL
install -m 644 -p Source/MediaInfoDLL/MediaInfoDLL.JNative.java %{buildroot}%{prefix}/include/MediaInfoDLL
install -m 644 -p Source/MediaInfoDLL/MediaInfoDLL.py %{buildroot}%{prefix}/include/MediaInfoDLL
install -m 644 -p Source/MediaInfoDLL/MediaInfoDLL3.py %{buildroot}%{prefix}/include/MediaInfoDLL
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/%{name}.conf << EOF
%{prefix}/lib
EOF

rm -f %{buildroot}%{prefix}/lib/%{libname}.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc History.txt ReadMe.txt
#%license License.html
%{prefix}/lib/*.so.*
%config %{_sysconfdir}/ld.so.conf.d/%{name}.conf

%files    devel
%doc Changes.txt Documentation.html Doc Source/Example
%{prefix}/include/MediaInfoDLL
%{prefix}/lib/%{libname}.so
%{prefix}/lib/%{libname}.a

%changelog
* Fri Oct 27 2017 Jess Portnoy <jess.portnoy@kaltura.com> 0.7.61-9
- Be more lenient about the libzen version (>= rather than =).

* Fri Sep 29 2017 Jess Portnoy <jess.portnoy@kaltura.com> 0.7.61-8
- Build against new libzen [0.4.37]

* Wed Sep 6 2017 Jess Portnoy <jess.portnoy@kaltura.com> 0.7.61-7
- Build against new libzen [0.4.36]

* Thu May 3 2017 Jess Portnoy <jess.portnoy@kaltura.com> 0.7.61-6
- Build against new libzen [0.4.35]

* Sat Sep 3 2016 Jess Portnoy <jess.portnoy@kaltura.com> 0.7.61-2
- Custom build for Kaltura CE, adopted from EPEL's mediainfo

* Tue Oct 23 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.61-1
- Update to 0.7.61

* Mon Sep 03 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.60-1
- Update to 0.7.60

* Tue Jun 05 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.58-1
- Update to 0.7.58

* Fri May 04 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.57-1
- Update to 0.7.57

* Wed Apr 11 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.56-1
- Update to 0.7.56

* Tue Mar 20 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.54-1
- Update to 0.7.54

* Thu Feb 09 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.53-1
- Update to 0.7.53

* Thu Dec 22 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.52-1
- Update to 0.7.52

* Tue Nov 22 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.51-2
- Added description in russian language

* Mon Nov 14 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.51-1
- Update to 0.7.51

* Tue Sep 27 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.50-1
- Update to 0.7.50

* Mon Sep 19 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.49-1
- Update to 0.7.49

* Fri Aug 19 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.48-1
- Update to 0.7.48

* Tue Aug 09 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.47-2
- Removed 0 from name

* Fri Aug 05 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.47-1
- Initial release
