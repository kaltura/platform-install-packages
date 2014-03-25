%define prefix /opt/kaltura
Name:	kaltura-media-server	
Version: 2.2.2 
Epoch: 1
Release: 1 
Summary: Kaltura Media Server 
License: AGPLv3+	
URL: https://github.com/kaltura/media-server/tree/%{version}
Source0: %{name}-%{version}.zip
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

This package installs the Kaltura Media Server which can integrate with either Red5 [see kaltura-red5 RPM] and Wowza.

%prep
%setup -qn media-server-%{version} 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/media-server
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content
cp -r %{_builddir}/media-server-%{version} $RPM_BUILD_ROOT/%{prefix}/web/flash/media-server/%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/media-server


%changelog
* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 2.2.2-1
- initial package.
