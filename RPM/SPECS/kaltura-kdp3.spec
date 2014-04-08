%define prefix /opt/kaltura
Name:	kaltura-kdp3	
Version: v3.9.8
Epoch: 1 
Release: 2 
Summary: Kaltura Dynamic Player
License: AGPLv3+	
URL: https://github.com/kaltura/kdp/releases/tag/%{version}
Source0: %{name}-%{version}.zip
Source1: %{name}-v3.9.7.zip
Source2: %{name}-v3.9.2.zip
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
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

This package installs the KDP Flash player.

%prep
%setup -qn %{version} 
unzip -qn %{SOURCE1} 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/kdp3
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content
	cp -r %{_builddir}/%{version} $RPM_BUILD_ROOT/%{prefix}/web/flash/kdp3/
	cp -r %{SOURCE1} $RPM_BUILD_ROOT/%{prefix}/web/flash/kdp3/
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/kdp3


%changelog
* Sun Mar 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v3.9.8-1
- SUP-1430 - Closed Captions won't show in livestream + prerolls 
- SUP-1498 - Video is not Auto played After Ad served. 
- SUP-1508 - [Internet Broadcasting] Closed Captioning won't work with flashvar. 

* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v3.9.7-3
- Since these widgets typically reside on NFS and served from another machine there is not need for the Apache dep.

* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 3.9.7-1
- Added support in "allowUserPauseAds" flashvar that will allow the user to pause ad playback.
- Fix DFXP styling: now subtitles will inherit the body style if no inlina style was set.
- SUP-1355 - Pass "AdParameters" value to VPAID SWF
- FEC-833 - Fix "Live" button functionality

* Wed Jan 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 3.0.0-3
- Added uiconf.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 3.0.0-2
- KDP v3.9.3 added.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 3.0.0-1
- initial package.
