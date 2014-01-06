%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define prefix /opt/kaltura
%define confdir %{prefix}/app/configurations
%define logdir %{prefix}/log
%define webdir %{prefix}/web

Summary: Kaltura Open Source Video Platform 
Name: kaltura-postinst 
Version: 1.0.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.gz
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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

This package includes post install scripts to be run post RPM install as they require user input.

%prep
%setup -qn postinst

%install
mkdir -p $RPM_BUILD_ROOT/%{prefix}/bin
chmod +x *.sh 
mv  *.{sh,rc} $RPM_BUILD_ROOT/%{prefix}/bin

%clean
rm -rf %{buildroot}

%post

%preun

%files
%{prefix}/bin/*


%changelog
* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-1
- initial package. 

