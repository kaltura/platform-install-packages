%define prefix /opt/kaltura
%define html5lib3_base %{prefix}/html5/html5lib/playkitSources/kaltura-ovp-player

Summary: Kaltura Open Source Video Platform 
Name: kaltura-html5lib3
Version: 0.45.5
Release: 2
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.gz 
Source1: create_playkit_uiconf.php

URL: https://github.com/kaltura/kaltura-player-js 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: kaltura-base, httpd

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

This package installs the Kaltura HTML5 v3 player library.

%prep
%setup -q -n %{version} 

%install
mkdir -p $RPM_BUILD_ROOT%{html5lib3_base}/%{version}
cp -r * $RPM_BUILD_ROOT%{html5lib3_base}/%{version} 
cp %{SOURCE1} $RPM_BUILD_ROOT%{html5lib3_base}/

%clean
rm -rf %{buildroot}

%post

%postun

%files
%defattr(-, root, root, 0755)
%{html5lib3_base}

%changelog
* Mon Aug 5 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.45.5-1
- Added the bumper and Youtube plugins

* Fri Apr 12 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.37.3-2
- Added RAPT plugin

* Tue Feb 12 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.37.3-1
- First release
