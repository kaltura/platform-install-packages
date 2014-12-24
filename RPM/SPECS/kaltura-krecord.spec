%define prefix /opt/kaltura
%define widget_name krecord
Name:	kaltura-%{widget_name}
Version: v1.7 
Epoch: 1
Release: 2
Summary: Kaltura kRecord - used for recording from web cam
License: AGPLv3+	
URL: http://kaltura.org
Source0: %{name}-%{version}.zip
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

This package installs the Kaltura kRecord - used for recording from web cam.

%prep
%setup -qn %{version} 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/%{widget_name}
#for i in %{krecord_vers};do
	cp -r %{_builddir}/%{version} $RPM_BUILD_ROOT/%{prefix}/web/flash/%{widget_name}
	find $RPM_BUILD_ROOT/%{prefix}/web/flash/%{widget_name} -name ".project" -exec rm {} \;
#done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/%{widget_name}


%changelog
* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v1.7.0-2
- Since these widgets typically reside on NFS and served from another machine there is not need for the Apache dep.

* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v1.7.0-1
- Publish Live Streams
  Use the following flashvars to publish live streams:
	isLive: "true"
	rtmpHost : address of a server that holds the app that handles publishing live streams (can be retrieved by parsing KalturaLiveStreamEntry.primaryBroadcastingUrl)
	fmsApp: name of the application that will handle live streaming (can be retrieved by parsing KalturaLiveStreamEntry.primaryBroadcastingUrl)
	streamName: name of the published stream (KalturaLiveStreamEntry.streamName)

- NOTE: KRecord GUI doesn't support live streaming gracefully. This feature is planned to be used without UI (via JS API).
- KRecord GUI doesn't stop you from publishing a live stream, but it doesn't hide irrelevant features like preview of published stream after publish is done.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-1
- initial package.
