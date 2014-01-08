
%define base_prefix /opt/kaltura/
Summary: Tool for HLS segmentation 
Name: kaltura-segmenter
Version: 1.0
Release: 1
License: GPLv2
Group: Applications/Multimedia

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc.

Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:kaltura-ffmpeg-aux-devel
Requires: kaltura-ffmpeg-aux

%description
Tool for HLS segmentation 


%prep
%setup -qn segmenter 

%build
export CFLAGS="%{optflags}"
export LD_LIBRARY_PATH=/opt/kaltura/lib
gcc -Wall -g segmenter.c -o segmenter -lavformat -lavcodec -lavutil -L/opt/kaltura/ffmpeg-0.6/lib -I/opt/kaltura/ffmpeg-0.6/include

%install
%{__mkdir_p} %{buildroot}/opt/kaltura/bin
mv segmenter %{buildroot}/opt/kaltura/bin

%clean
%{__rm} -rf %{buildroot}

%files
/opt/kaltura/bin/segmenter

%changelog
* Wed Jan 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0-1 
- Initial build.
