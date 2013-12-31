Summary: Kaltura Open Source Video Platform - batch server 
Name: kaltura-batch
Version: 9.7.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/server/archive/IX-%{version}.zip 
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: kaltura-base, kaltura-ffmpeg, kaltura-ffmpeg-aux, php, httpd, sox, mencoder, ImageMagick, sshpass, php-pecl-memcached, php-mcrypt

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

This package sets up a node to be a batch server.


%prep
%setup -q

%build

%install

%clean
rm -rf %{buildroot}

%post
if [ "$1" = 1 ];
then
    /sbin/chkconfig --add kaltura-batch
fi

%preun
if [ "$1" = 0 ] ; then
    /sbin/service kaltura-batch stop >/dev/null 2>&1
    /sbin/chkconfig --del kaltura-batch
fi
# create user/group, and update permissions
chown -R %{sphinx_user}:%{sphinx_group} %{prefix}-%{version}/batch 

%files


%changelog
* Mon Dec  23 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 8.0-1
- First package
