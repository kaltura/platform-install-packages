%define prefix /opt/kaltura
%define kaltura_user kaltura
Summary: Kaltura Open Source Video Platform - Media Server 
Name: kaltura-media-server
Version: 3.1.5
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/media-server/releases/download/rel-%{version}/KalturaWowzaServer-install-%{version}.zip 
URL: https://github.com/kaltura/media-server 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: kaltura-base, kaltura-postinst, jre >= 1.7.0, ant
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

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{prefix}/media-server
unzip -d $RPM_BUILD_ROOT/%{prefix}/media-server %{SOURCE0}

%clean
rm -rf %{buildroot}

%pre

%post
if [ "$1" = 1 ];then
	echo "
#####################################################################################################################################
Installation of %{name} %{version} completed
Please run 
# /opt/kaltura/bin/%{name}-config.sh [/path/to/answer/file]
To finalize the setup.
#####################################################################################################################################
"
fi

%preun

%files
%dir %{prefix}/media-server
%{prefix}/media-server/*


%changelog
* Fri Dec 12 2014 Tan-Tan <jonathan.kanarek@kaltura.com> - v3.1.5
- Package jar instead of zip

* Thu May 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 3.0.8.5-1
- Initial release.

