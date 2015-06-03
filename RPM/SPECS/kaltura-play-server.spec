%define prefix /opt/kaltura/play-server
%define kaltura_user kaltura
Summary: Kaltura Open Source Video Platform - Play Server 
Name: kaltura-play-server
Version: 1.1
Release: 5
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/play-server/archive/kaltura-play-server-v%{version}.zip

URL: https://github.com/kaltura/play-server 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  kaltura-postinst, memcached, npm, nodejs, kaltura-ffmpeg
BuildRequires: memcached-devel, node-gyp, id3lib-devel,npm

%description
Kaltura is the world's first Open Source Online Video Platform, transforming the way people work, 
learn, and entertain using online video. 
The Kaltura platform empowers media applications with advanced video management, publishing, 
and monetization tools that increase their reach and monetization and simplify their video operations. 
Kaltura improves productivity and interaction among millions of employees by providing enterprises 
powerful online video tools for boosting internal knowledge sharing, training, and collaboration, 
and for more effective marketing. Kaltura offers next generation learning for millions of students and 
teachers by providing educational institutions disruptive online video solutions for improved teaching,
learning, and increased engagement across campuses and beyond. 
For more information visit: http://corp.kaltura.com, http://www.kaltura.org and http://www.html5video.org.


The Kaltura platform enables video management, publishing, syndication and monetization, 
as well as providing a robust framework for managing rich-media applications, 
and developing a variety of online workflows for video. 

This package configures the Play Server component. 

%prep
%setup -qn play-server-%{version}

%build
npm install nan
rm %{_builddir}/play-server-%{version}/bin/ffmpeg-*-bin.tar.gz

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/share
mkdir -p $RPM_BUILD_ROOT%{prefix}/log
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/ad_download
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/ad_transcode
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/segments
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/tmp
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/ad_ts
ROOT_CWD=`pwd`
cd %{_builddir}/play-server-%{version}/native/vendor/id3lib-3.8.3
./configure --prefix=%{prefix}
make
%{__make} DESTDIR=$RPM_BUILD_ROOT install
%{__make} clean
cd $ROOT_CWD/native/node_addons/TsPreparer
node-gyp configure
node-gyp build
cd $ROOT_CWD/native/node_addons/TsStitcher
node-gyp configure
node-gyp build

cd $ROOT_CWD/native/node_addons/TsId3Reader
node-gyp configure
node-gyp build
cp -r %{_builddir}/play-server-%{version}/* $RPM_BUILD_ROOT%{prefix}/
find $RPM_BUILD_ROOT%{prefix}/ -name ".gitignore" -exec rm {} \;
find $RPM_BUILD_ROOT%{prefix}/ -name "build" -type d -exec rm -rf {} \; || true
%clean
rm -rf %{buildroot}

%pre

%post
echo "
#####################################################################################################################################
Installation of %{name} %{version} completed
Please run 
# /opt/kaltura/bin/%{name}-config.sh [/path/to/answer/file]
To finalize the setup.
#####################################################################################################################################
"
chmod +x %{prefix}/bin/play-server.sh
if [ $1 -eq 1 ]; then
	ln -sf %{prefix}/bin/play-server.sh %{_initrddir}/kaltura-play-server
	ln -s /opt/kaltura/bin/ffmpeg %{prefix}/bin/
	/sbin/chkconfig --add kaltura-play-server
	npm install -g node-gyp
else
	service kaltura-play-server restart
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service kaltura-play-server stop > /dev/null 2>&1
    /sbin/chkconfig --del kaltura-play-server
fi

%files
%{prefix}

%changelog
* Tue Jun 2 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.1-5
- Precompile needed modules.
- Added build deps
- symlink ffmpeg from kaltura-ffmpeg to /play-server/prefix/bin ffmpeg

* Sun May 31 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.1-3
- Added needed dirs
- Add to init

* Thu May 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.1-1
- Initial release.

