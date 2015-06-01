%define prefix /opt/kaltura/play-server
%define kaltura_user kaltura
Summary: Kaltura Open Source Video Platform - Play Server 
Name: kaltura-play-server
Version: 1.1
Release: 2
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/play-server/archive/kaltura-play-server-v%{version}.zip

URL: https://github.com/kaltura/play-server 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  jre >= 1.7.0, kaltura-postinst, ant >= 1.7.0, memcached, npm, nodejs
BuildArch: noarch

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

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}
mv  %{_builddir}/play-server-%{version}/* $RPM_BUILD_ROOT%{prefix}/

%clean
rm -rf %{buildroot}

%pre

%post
npm install -g node-gyp
echo "
#####################################################################################################################################
Installation of %{name} %{version} completed
Please run 
# /opt/kaltura/bin/%{name}-config.sh [/path/to/answer/file]
To finalize the setup.
#####################################################################################################################################
"

%preun

%files
%dir %{prefix}
%{prefix}
%dir %{prefix}/bin/
%{prefix}/bin/*

%changelog
* Thu May 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.1-1
- Initial release.

