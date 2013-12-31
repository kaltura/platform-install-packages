Summary: Kaltura Open Source Video Platform - frontend server 
Name: kaltura-front
Version: 9.7.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/server/archive/IX-%{version}.zip 
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: httpd, php, kaltura-base, kaltura-ffmpeg, ImageMagick, mencoder, memcached, php-pecl-memcached, php-mysql, php-pecl-apc, php-mcrypt

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

This package sets up a server as a front node.

%prep
%setup -q

%build


%clean
rm -rf %{buildroot}

%files
%config(noreplace,missingok) %{_sysconfdir}/php.d/kaltura.ini
%config(noreplace,missingok) %{prefix}/app/configurations/apache/conf.d/*.conf
%config(noreplace,missingok) %{_sysconfdir}/php.d/kaltura-front.ini
%config(noreplace,missingok) %{prefix}/app/configurations/apache/conf.d/api.conf
%config(noreplace,missingok) %{prefix}/app/configurations/apache/conf.d/kmc.conf
%config(noreplace,missingok) %{prefix}/app/configurations/apache/conf.d/admin-console.conf

%changelog
* Mon Dec  23 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 8.0-1
- First package
