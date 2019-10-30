%define prefix /opt/kaltura
Name:	kaltura-kmcng
Version: v5.18.0
Release: 1
Summary: Kaltura HTML5 Management Console

Group: System Management	
License: AGPLv3+	
URL: https://github.com/kaltura/kmcng 
Source0: %{name}-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: kaltura-base, httpd, kaltura-html5-studio,php-cli, kaltura-live-analytics-front, kaltura-html5-analytics 

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
* Thu Oct 24 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.18.0-1
- content/entry: open live analytics for manual live entries (614c63e)
- Upgrade to Angular 8 (#853) (82e506c)
- Add the ability to toggle captions (#869) (6319b3d)

* Mon Oct 7 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.17.0-1
- login: direct users to login with SSO page (22e9505)
- administration/users: add user analytics drill-down action (#862) (035e7e1) 

* Mon Sep 16 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.16.0
- Support SSO login (#866) (51156ee)

* Wed Sep 4 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.15.0
- Multi account menu style fixes (#861) (d6b823b)
- content/drop-folders: Add drop folders filter by folder name (#863) (fffa4c4)
 
* Tue Sep 3 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.14.0
- content/entry: In scheduling tab: display entry end date even if entry start date is not specified (45985ea)
- entries/filters: fix refine filter custom scheduling date picker behavior (d231b8e)
- content/entries: Load thumbnails restricted by KS

* Tue Aug 20 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.13.1-1
- entries/metadata: Fix custom metadata search in refine filter (#858) (8f16be3)

* Mon Aug 5 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.13.0-1
- entry-live: Add SIP user details for entry drill-down live tab (#857) (a2ff592)
- entry/preview: pass admin ks to player (0cc2566)
- settings/transcoding-profiles: allow saving new profiles (b813909)

* Tue Jul 16 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.12.0-1
- analytics: allow real-time analytics player to toggle full screen (fc2483e)
- Fix caption request not working on Mac Safari (b4c4461)
- entries/bulk-actions: prevent app crash on bulk edit (#852) (67c3172)
- entry/details: hide old analytics link if not available (#849) (b4d77bb)
- entry/live: update go live button status upon polling (#850) (2ce5741)
- login: Clear error message after restoring password fails (bfee611)
- preview: support DRM playback in all KMC preview players (e3d1dcc)
- settings/my-user-settings: remove email edit option (a7bd6a1)
- settings/transcoding-settings: prevent removal of default flavorParamId when saving profile flavors list (27ac9b8)
- share & embed: Refresh player when switching embed types to properly render thumbnail embed (#847) (e0a0a0c)
- upload: update client lib to support minimumChunkSize specification when creating a new uploadToken (537526e)
- analytics: provide date format in analytics config (#854) (82d31f4)
- entry(captions): support SCC caption type

* Mon Jul 1 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.11.0-1
- login: fix update password to work when the user is not logged in (03bc2ee)
- Two factor authentication support (#844) (4b809f4)

* Mon Jun 10 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.10.0-1
- administration/multi-account: allow only active accounts to be used as templates (3107050)
- administration/multi-account: disable "Create" button until data loads (24e9d2e)
- administration/multi-account: disregard removed templates for new account creation (542a01c)
- administration/multi-account: Multi-account management
- content/entries: Bulk add/remove of co-viewers (4e24b9b)

* Wed May 22 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.9.1-1
- prevent passwords auto filling (#831) (d853051)
- administration/multi-account: disable create button on error state (462881c)
- administration/multi-account: fix adding website info when creating new account (cfbb7d4)
- administration/multi-account: fix available accounts calculation (f270218)
- entry/captions: support Luxembourgish captions (9cae1a9)

* Thu Apr 25 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.8.0-1
- Server poll invalid KS handling (#827) (6215876)
- content/category: Allow editing entitlements of categories which owner was deleted (72219ae)
- content/syndication: Handle Syndication feeds which use a playlist which is not loaded in the first 500 playlists (#826) (21a1bcc)
- entry/users: Add co-viewers form field (#828) (d4222fd)
- Let the user choose the date format (#829) (a163026)

* Mon Apr 15 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.7.1-1
- Content interactions dashboard in the analytics dashboards
- Export to csv functionality in the analytics dashboard

* Thu Mar 28 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.7.0-1
- entry/contribution: Fix entry size calculation (eb82ba2)
- entry/preview: Support Youtube entries playback in mini-preview (9c18060)

* Thu Mar 14 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v5.6.5-1
- categories: Show up to 100 sub-categories in the category details panel (2bb1467)
- login: fix password expiration message (56517e1)

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
