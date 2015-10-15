
%define base_prefix /opt/kaltura
Summary: Tool for HLS segmentation 
Name: kaltura-segmenter
Version: 1.0
Release: 2
License: GPLv2
Group: Applications/Multimedia

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc.

Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:kaltura-ffmpeg-aux-devel
Requires: kaltura-ffmpeg-aux = 0.6

%description
Tool for HLS segmentation 


%prep
%setup -q 

%build
#export CFLAGS="%{optflags}"
#export LD_LIBRARY_PATH=%{base_prefix}/lib
#gcc -Wall -g segmenter.c -o segmenter -lavformat -lavcodec -lavutil -L%{base_prefix}/ffmpeg-0.6/lib -I%{base_prefix}/ffmpeg-0.6/include

%install
%{__mkdir_p} %{buildroot}%{base_prefix}/bin %{buildroot}%{base_prefix}/lib
mv segmenter %{buildroot}%{base_prefix}/bin
cp %{base_prefix}/ffmpeg-0.6/lib/libavformat.so.52 %{base_prefix}/ffmpeg-0.6/lib/libavcodec.so.52 %{base_prefix}/ffmpeg-0.6/lib/libavutil.so.50 %{buildroot}%{base_prefix}/lib

%clean
%{__rm} -rf %{buildroot}

%files
%{base_prefix}/bin/segmenter
%{base_prefix}/lib/libavformat.so.52
%{base_prefix}/lib/libavcodec.so.52
%{base_prefix}/lib/libavutil.so.50

%changelog
* Thu Oct 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0-2
- Since kaltura-ffmpeg-aux is now of v2.1.3 and segmenter need 0.6, package the needed libs as part of this RPM.

* Wed Jan 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0-1 
- Initial build.
