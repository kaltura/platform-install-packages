%define prefix /opt/kaltura
Name:	kaltura-kmc-docs	
Version: 9.15.0
Release: 1
Summary: Kaltura Management Console

Group: System Management	
License: AGPLv3+	
URL: https://github.com/kaltura/kmc-docs 
Source0: https://github.com/kaltura/kmc-docs/archive/kmc-docs-%{version}.tar.gz 
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: kaltura-kmc

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

This package installs the KMC HTML documentation. 

%prep
%setup -qn kmc-docs-IX_%{version}

%build
%post

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content/docs
cp -r NetHelp 

%preun
#if [ "$1" = 0 ] ; then
#	rm -f %{prefix}/web/content/uiconf/appstudio
#fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)


%changelog
* Mon Mar 12 Jess Portnoy <jess.portnoy@kaltura.com> - 9.15.0-1
- KMC docs is a different repo so it makes sense to separate it into a different package.
