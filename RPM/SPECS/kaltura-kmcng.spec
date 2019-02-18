%define prefix /opt/kaltura
Name:	kaltura-kmcng
Version: v5.6.4
Release: 1
Summary: Kaltura HTML5 Management Console

Group: System Management	
License: AGPLv3+	
URL: https://github.com/kaltura/kmcng 
Source0: %{name}-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: kaltura-base, httpd, kaltura-html5-studio,php-cli, kaltura-live-analytics-front, kaltura-kmcng-analytics-front	

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

This package installs the KMC HTML5 web interface.

%prep
%setup -q -n %{name}-%{version} 

%build
%post

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/apps/kmcng
cp -r %{_builddir}/%{name}-%{version} $RPM_BUILD_ROOT%{prefix}/apps/kmcng/%{version}

%preun

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/apps/kmcng/%{version}
%config %{prefix}/apps/kmcng/%{version}/deploy/*


%changelog
* Mon Feb 18 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.6.4-1
- entry/captions: Support ordering captions for Youtube entries (701dd3f)
- entry/related: Add support to JSON files in entry related files (bcc05f6)
- syndication: Fix issue in ITunes Syndication feeds with categories containing ampersand (b738b46)

* Mon Feb 4 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.6.3-1
- entry/distribution: fix errors mapping (7e4419f)

* Thu Jan 17 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.6.2-1
- Advertisements: Enable advertisements for entries without Source flavor (e9e29d0)
- Analytics: Fix cdn_host parameter passed to Live-Analytics (c290579)
- Syndication: Syndication feeds are not created for some playlists

* Fri Dec 28 2018 jess.portnoy@kaltura.com <Jess Portnoy> - v5.6.1-1
- content/entry: fix distribution delete message layout + support passing accept and reject button labels to confirm box (2d6303d)
- content/entry: support additional video formats when updating flavour or replacing video (ba5b7ee)
- live-analytics: fix cdn_host for secured protocol (5f8511b)
- Custom metadata - display field system name
- Add support for Sami languages when uploading captions to KMC
- content/entry: fix position of upload settings window on MS Edge when replacing video (e952515)

* Thu Nov 15 2018 jess.portnoy@kaltura.com <Jess Portnoy> - v5.5.2-1
- content/entry: fix position of upload settings window on MS Edge when replacing video (e952515)
- upload: fix position of upload settings window on MS Edge (f5e2453)
- fix create menu icons width in all languages (ebe3262)
- fix Yahoo and iTunes category tags translation in German (4411d2e)
- administration/users: enable KMC access to existing KMS users when creating a new user using a KMS user ID (d57ef34)
- content/category: update entitlements options labels (e4c9fe1)
- content/playlist: remove the "Plays" field from the playlist details info (52d043c)
- contextual-help: update broken links in contextual help system (9b5ee24)

* Mon Oct 8 2018 jess.portnoy@kaltura.com <Jess Portnoy> - v5.4.2-1
- content/category: fix "Move Category" panel height to support other languages (211ba28)
- content/entry: fix entry actions button width on Firefox (058bb95)
- help: add missing help links to settings/account information section (7b75185)
- hide OTT players from VOD Share & Embed players list (561d159)
- settings/account-info: fix form sending error (6affdc3)

* Mon Aug 27 2018 jess.portnoy@kaltura.com <Jess Portnoy> - v5.3.2-1
- content/entries: adjust position of the Youtube icon on entry thumbnails (825d2f3)
- content/entry: disable entry download if user doesn't have the required permissions (872799b)
- upload: fix "Create from URL" upload button label (3439b78)
- upload: set entry name and format for entries created from URL (#798) (b7d3621)

* Fri Aug 10 2018 jess.portnoy@kaltura.com <Jess Portnoy> - v5.2.1
- Custom Data - Some characters entered in custom text fields are displayed with their character reference and break-lines are ignored
- Entries - Scrolling down action isn't smooth in IE11, edge and Firefox

* Wed Jun 27 2018 jess.portnoy@kaltura.com <Jess Portnoy> - v4.5.1
- First release
