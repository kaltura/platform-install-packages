%define prefix /opt/kaltura
Name:	kaltura-ksr	
Version: v1.0.44
Release: 1 
Summary: Kaltura screen recorder
License: AGPLv3+	
URL: http://kaltura.org
Source0: %{name}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: kaltura-base

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

This package installs the Kaltura screen recorder.

%prep
%setup -qn %{name} 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/ksr
cp -r %{_builddir}/%{name} $RPM_BUILD_ROOT/%{prefix}/web/flash/ksr/%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/ksr


%changelog
* Tue Feb 11 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v1.0.44
- initial package.
