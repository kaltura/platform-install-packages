%define base_prefix /opt/kaltura/ffmpeg
%define _without_gsm 1
%define _without_nut 1

### No package yet
%define _without_vpx 1

### Use native vorbis
%define _without_vorbis 1

### Use native xvid
%define _without_xvid 1

### Disabled speex support as ffmpeg needs speex 1.2 and RHEL5 ships with 1.0.5


%{?el6:%define _without_dc1394 1}
%{?el6:%define _without_schroedinger 1}
#%{?el6:%define _without_speex 1}
%{?el6:%define _without_theora 1}

%{?el5:%define _without_dc1394 1}
%{?el5:%define _without_schroedinger 1}
%{?el5:%define _without_speex 1}
%{?el5:%define _without_theora 1}

%{?el4:%define _without_dc1394 1}
%{?el4:%define _without_speex 1}
%{?el4:%define _without_texi2html 1}
%{?el4:%define _without_theora 1}
%{?el4:%define _without_v4l 1}

%{?el3:%define _without_dc1394 1}
%{?el3:%define _without_schroedinger 1}
%{?el3:%define _without_speex 1}
%{?el3:%define _without_texi2html 1}
%{?el3:%define _without_theora 1}

Summary: Utilities and libraries to record, convert and stream audio and video
Name: kaltura-ffmpeg-aux
Version: 0.6 
Release: 2 
License: GPL
Group: Applications/Multimedia
URL: http://ffmpeg.org/

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc.

Source: http://www.ffmpeg.org/releases/ffmpeg-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: SDL-devel
BuildRequires: freetype-devel
BuildRequires: imlib2-devel
BuildRequires: zlib-devel
%{!?_without_a52dec:BuildRequires: kaltura-a52dec-devel}
%{!?_without_dc1394:BuildRequires: libdc1394-devel}
%{!?_without_faac:BuildRequires: faac-devel}
%{!?_without_gsm:BuildRequires: gsm-devel}
%{!?_without_lame:BuildRequires: kaltura-lame-devel}
%{!?_without_nut:BuildRequires: libnut-devel}
%{!?_without_opencore_amr:BuildRequires: opencore-amr-devel}
%{!?_without_openjpeg:BuildRequires: openjpeg-devel}
%{!?_without_rtmp:BuildRequires: librtmp-devel}
%{!?_without_schroedinger:BuildRequires: schroedinger-devel}
%{!?_without_texi2html:BuildRequires: texi2html}
%{!?_without_theora:BuildRequires: libogg-devel, libtheora-devel}
%{!?_without_vorbis:BuildRequires: libogg-devel, libvorbis-devel}
%{!?_without_vpx:BuildRequires: libvpx-devel}
%{!?_without_x264:BuildRequires: kaltura-x264-devel}
%{!?_without_xvid:BuildRequires: xvidcore-devel}
%{!?_without_a52dec:Requires: a52dec}
BuildRequires: yasm-devel
BuildRequires: libass-devel 
BuildRequires: kaltura-x264-devel 
BuildRequires: openjpeg-devel
Requires:kaltura-a52dec,kaltura-libfaac,kaltura-x264

%description
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

%package devel
Summary: Header files and static library for the ffmpeg codec library
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: imlib2-devel, SDL-devel, freetype-devel, zlib-devel, pkgconfig,kaltura-x264
%{!?_without_a52dec:Requires: kaltura-a52dec-devel}
%{!?_without_dc1394:Requires: libdc1394-devel}
%{!?_without_faac:Requires: faac-devel}
%{!?_without_faad:Requires: faad2-devel}
%{!?_without_gsm:Requires: gsm-devel}
%{!?_without_lame:Requires: kaltura-lame-devel}
%{!?_without_openjpeg:Requires: openjpeg-devel}
%{!?_without_rtmp:Requires: librtmp-devel}
%{!?_without_schroedinger:Requires: schroedinger-devel}
%{!?_without_vorbis:Requires: libogg-devel, libvorbis-devel}
%{!?_without_vpx:Requires: libvpx-devel}
%{!?_without_x264:Requires: kaltura-x264-devel}
%{!?_without_xvid:Requires: xvidcore-devel}

%description devel
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

Install this package if you want to compile apps with ffmpeg support.

%prep
%setup -qn ffmpeg-%{version}

sed -i 's|gsm.h|gsm/gsm.h|' configure libavcodec/libgsm.c

%build
export CFLAGS="%{optflags}"
./configure \
    --prefix="%{base_prefix}-%{version}" \
    --libdir="%{base_prefix}-%{version}/lib" \
    --shlibdir="%{base_prefix}-%{version}/lib" \
%{?_without_v4l:--disable-demuxer=v4l --disable-demuxer=v4l2} \
%ifarch %ix86
    --extra-cflags="%{optflags}" \
%endif
%ifarch x86_64
    --extra-cflags="%{optflags} -fPIC" \
%endif
    --enable-avfilter \
%{!?_without_schroedinger:--enable-libschroedinger} \
%{!?_without_dc1394:--enable-libdc1394} \
%{!?_without_faac:--enable-libfaac} \
%{!?_without_gsm:--enable-libgsm} \
%{!?_without_lame:--enable-libmp3lame} \
%{!?_without_nut:--enable-libnut} \
%{!?_without_opencore_amr:--enable-libopencore-amrnb --enable-libopencore-amrwb} \
%{!?_without_rtmp: --enable-librtmp} \
%{!?_without_speex:--enable-libspeex} \
%{!?_without_theora:--enable-libtheora} \
%{!?_without_vorbis: --enable-libvorbis} \
%{!?_without_vpx: --enable-libvpx} \
%{!?_without_x264:--enable-libx264} \
%{!?_without_xvid:--enable-libxvid} \
    --enable-gpl \
    --enable-nonfree \
%{!?_without_openjpeg:--enable-libopenjpeg} \
    --enable-postproc \
    --enable-pthreads \
    --enable-shared \
    --enable-swscale \
    --enable-vdpau \
    --enable-version3 \
    --enable-bzlib \
    --disable-devices \
    --enable-filter=movie \
    --enable-x11grab

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot} _docs
%{__make} install DESTDIR="%{buildroot}"

# Remove unwanted files from the included docs
%{__cp} -a doc _docs
%{__rm} -rf _docs/{Makefile,*.texi,*.pl}

# The <postproc/postprocess.h> is now at <ffmpeg/postprocess.h>, so provide
# a compatibility symlink
%{__mkdir_p} %{buildroot}%{_includedir}/postproc/
#%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
#cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/kaltura_ffmpeg-aux.sh << EOF
#PATH=$PATH:%{base_prefix}-%{version}/bin
#export PATH
#EOF

%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/kaltura_ffmpeg_aux.conf << EOF
%{base_prefix}-%{version}/lib
EOF

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig
chcon -t textrel_shlib_t %{prefix}/lib/libav{codec,device,format,util}.so.*.*.* &>/dev/null || :
ln -fs %{base_prefix}-%{version}/bin/ffmpeg /opt/kaltura/bin/ffmpeg-aux 

%postun 
/sbin/ldconfig
if [ "$1" = 0 ] ; then
	rm -f /opt/kaltura/bin/ffmpeg-aux
fi

%files
%defattr(-, root, root, 0755)
%doc Changelog COPYING* CREDITS INSTALL MAINTAINERS README
%doc %{base_prefix}-%{version}/share/man/man1
#%config %{_sysconfdir}/profile.d/kaltura_ffmpeg-aux.sh
%config %{_sysconfdir}/ld.so.conf.d/kaltura_ffmpeg_aux.conf
%{base_prefix}-%{version}/bin/*
%{base_prefix}-%{version}/share/ffmpeg/
%{base_prefix}-%{version}/lib/*.so*
%{base_prefix}-%{version}/lib/pkgconfig/
%exclude %{base_prefix}-%{version}/lib/*.a
%exclude %{base_prefix}-%{version}/include

%files devel
%defattr(-, root, root, 0755)
%doc _docs/*
%{base_prefix}-%{version}/include/libavcodec/
%{base_prefix}-%{version}/include/libavdevice/
%{base_prefix}-%{version}/include/libavfilter/
%{base_prefix}-%{version}/include/libavformat/
%{base_prefix}-%{version}/include/libavutil/
%{base_prefix}-%{version}/include/libswscale/
%{base_prefix}-%{version}/lib/libavcodec.a
%{base_prefix}-%{version}/lib/libavdevice.a
%{base_prefix}-%{version}/lib/libavfilter.a
%{base_prefix}-%{version}/lib/libavformat.a
%{base_prefix}-%{version}/lib/libavutil.a
%{base_prefix}-%{version}/lib/libswscale.a
%{base_prefix}-%{version}/lib/libavcodec.so
%{base_prefix}-%{version}/lib/libavdevice.so
%{base_prefix}-%{version}/lib/libavfilter.so
%{base_prefix}-%{version}/lib/libavformat.so
%{base_prefix}-%{version}/lib/libavutil.so
%{base_prefix}-%{version}/lib/libswscale.so
%{base_prefix}-%{version}/lib/pkgconfig/libavcodec.pc
%{base_prefix}-%{version}/lib/pkgconfig/libavdevice.pc
%{base_prefix}-%{version}/lib/pkgconfig/libavfilter.pc
%{base_prefix}-%{version}/lib/pkgconfig/libavformat.pc
%{base_prefix}-%{version}/lib/pkgconfig/libavutil.pc
%{base_prefix}-%{version}/lib/pkgconfig/libswscale.pc

%changelog
* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.1.1-2
- Remove symlink to /opt/kaltura/bin at %%postun.

* Wed Dec 25 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 0.6-1
- Initial build.
