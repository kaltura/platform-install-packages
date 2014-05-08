%define prefix /opt/kaltura
%define kaltura_user kaltura
Summary: Kaltura Open Source Video Platform - Media Server 
Name: kaltura-media-server
Version: 3.0.8
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/media-server/archive/%{version}.zip 
URL: https://github.com/kaltura/media-server 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: kaltura-base, kaltura-postinst 
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

This package configures the Media Server component. 

%prep
%setup -qn media-server-%{version} 

%build

%install

%clean
rm -rf %{buildroot}

%pre

%post

%preun

%files


%changelog
