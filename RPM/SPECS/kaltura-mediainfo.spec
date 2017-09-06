%global libzen_version  0.4.36
%define prefix /opt/kaltura

Name:           kaltura-mediainfo
Version:        0.7.61
Release:        7
Summary:        Supplies technical and tag information about a video or audio file (CLI)

License:        BSD
Group:          Applications/Multimedia
URL:            http://mediaarea.net/MediaInfo
Source0:        http://mediaarea.net/download/source/mediainfo/%{version}/mediainfo_%{version}.tar.bz2

BuildRequires:  kaltura-libmediainfo-devel >= %{version}
BuildRequires:  pkgconfig(libzen) >= %{libzen_version}
BuildRequires:  pkgconfig(zlib)
BuildRequires:  libtool
BuildRequires:  automake
BuildRequires:  autoconf
Requires:  kaltura-libmediainfo = %{version}
Requires: libzen = %{libzen_version}

%description
MediaInfo CLI (Command Line Interface).

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


%prep
%setup -q -n MediaInfo
#%patch0 -p1
#%patch1 -p1

sed -i 's/.$//' *.txt *.html Release/*.txt

#find Source -type f -exec chmod 644 {} ';'
chmod 644 *.html *.txt Release/*.txt

#https://fedorahosted.org/FedoraReview/wiki/AutoTools
sed -i 's/AC_PROG_LIBTOOL/LT_INIT/' Project/GNU/*/configure.ac


%build
# build CLI
pushd Project/GNU/CLI
    ./autogen
    ./configure --enable-static=no --prefix=%{prefix}
    LIBRARY_PATH=/opt/kaltura/lib make %{?_smp_mflags}
popd


%install
pushd Project/GNU/CLI
    %make_install
popd


%files
%doc Release/ReadMe_CLI_Linux.txt History_CLI.txt
#%license License.html
%{prefix}/bin/mediainfo


%changelog
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

* Fri May 04 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.57-2
- Clean spec

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
