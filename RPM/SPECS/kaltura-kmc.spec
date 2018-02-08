%define prefix /opt/kaltura
Name:	kaltura-kmc
Version: v5.43.12
Release: 1
Summary: Kaltura Management Console

Group: System Management	
License: AGPLv3+	
URL: https://github.com/kaltura/kmc 
Source0: %{name}-%{version}.tar.bz2
Source1: kmc_config.ini
Source2: kmc_preview_dark.json
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: kaltura-base, httpd, kaltura-html5-studio,php-cli	

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

This package installs the KMC Flash web interface.

%prep
%setup -q 

%build
%post
if [ -L %{prefix}/web/content/uiconf ];then
	rm %{prefix}/web/content/uiconf
fi
# remove link and resym.
if [ -L %{prefix}/web/content/uiconf/kaltura/kmc ];then
	rm %{prefix}/web/content/uiconf/kaltura/kmc
fi

mkdir -p %{prefix}/web/content/uiconf/kaltura
cp -r %{prefix}/web/flash/kmc/%{version}/uiconf/kaltura/kmc %{prefix}/web/content/uiconf/kaltura
#if [ -r "%{prefix}/app/configurations/local.ini" -a -r "%{prefix}/app/configurations/system.ini" ];then
#	php %{prefix}/app/deployment/uiconf/deploy_v2.php --ini=%{prefix}/web/flash/kmc/%{version}/config.ini >> %{prefix}/log/deploy_v2.log  2>&1
#fi

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/login
mkdir -p $RPM_BUILD_ROOT%{prefix}/app/alpha/web/lib
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content/docs/pdf
#cp doc/pdf/KMC_User_Manual.pdf $RPM_BUILD_ROOT%{prefix}/web/content/docs/pdf
cp -r doc/* $RPM_BUILD_ROOT%{prefix}/web/content/docs/
mv doc/pdf $RPM_BUILD_ROOT%{prefix}/app/alpha/web/lib/ 
mv %{_builddir}/%{name}-%{version}/login/%{kmc_login_version} $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/login/ 
mkdir $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/%{version}
cp -r %{_builddir}/%{name}-%{version}/%{version}/* $RPM_BUILD_ROOT/%{prefix}/web/flash/kmc/%{version}/
mv %{_builddir}/%{name}-%{version}/uiconf $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/%{version}/
cp %{SOURCE1} $RPM_BUILD_ROOT/%{prefix}/web/flash/kmc/%{version}/config.ini
cd $RPM_BUILD_ROOT/%{prefix}/web/flash/kmc/%{version} 
for i in "*.xml" "*.template" "*.ttf" "*.xsl" "*.xsd" "*.yml" "*.smil" "*.srt" "*.sql" "*.orig" "*.patch" "*.po" "*.pdf" "*.otf" "*.txt" "*.php" "*.phtml" "*.
project" "*.png" "*.properties" "*.sample" "*.swf" "*.sf" "*.swz" "*.uad" "*.prefs" "*.psd" "*.rvmrc" "*.sln" "*.ini" "*.log" ;do
	find . -iname "$i" -exec chmod 644 {} \;
done
cp %{SOURCE2} $RPM_BUILD_ROOT/%{prefix}/web/flash/kmc/%{version}/xml/content/

%preun
#if [ "$1" = 0 ] ; then
#	rm -f %{prefix}/web/content/uiconf/appstudio
#fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/kmc
%doc %{prefix}/web/content/docs/
%doc %{prefix}/app/alpha/web/lib/pdf/*
#%{prefix}/web/content/uiconf/kaltura/kmc
%config %{prefix}/web/flash/kmc/%{version}/config.ini


%changelog
* Tue Feb 6 2018 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.12-1
- PLAT-8413 - add two types of Chinese subtitles

* Mon Jan 29 2018 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.11-2
- Ver bounce of HTML5 player to v2.65.2

* Thu Jan 25 2018 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.11-1
- PLAT-7249 - Expose RTSP URLs in KMC
- PLAT-8467 - advertising url per content should be optional in the KMC - requires PLAT-8468

* Tue Jan 15 2018 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.10-3
- Ver bounce of HTML5 player to v2.65

* Tue Jan 2 2018 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.10-2
- Ver bounce of HTML5 player to v2.64.4

* Fri Dec 29 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.10-1
- SUP-12502 - Fix Google structured data errors

* Mon Dec 18 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.9-1
- PLAT-8367 - Explicit KMC: if publisher presses Save in just created entry, its Auto-start is changed to enabled automatically
- Ver bounce of HTML5 player to v2.64

* Wed Nov 29 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.6-1
- Ver bounce of HTML5 player to v2.63.3
- SUP-11685 - Bulk unpublish from multiple categories produce error #1010

* Mon Nov 20 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.5-2
- Ver bounce of HTML5 player to v2.63.2

* Fri Nov 17 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.5-1
- SUP-11848 - Youtube entries display in KMC - unresponsive
- Ver bounce of HTML5 player to v2.63.1

* Thu Oct 19 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.4-3
- Ver bounce of HTML5 player to v2.62

* Mon Oct 9 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.4-1
- PLAT-8070 - re-enable live dashboard shortcut in the old KMC
- Ver bounce of HTML5 player to v2.61.4

* Sun Sep 24 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.3-1
- SUP-10756 - Cannot download XML file from the Bulk menu - re-fix
- Ver bounce of HTML5 player to v2.61.1
- Change the built in EmailValidator to support new TLDs

* Wed Sep 6 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.43.1-1
- hide live dashboard link (not yet ready)
- Ver bounce of HTML5 player to v2.61

* Thu Aug 17 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.42.3-3
- Ver bounce of HTML5 to v2.60.2

* Fri Aug 11 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.42.3-2
- Ver bounce of HTML5 to v2.60

* Fri Jul 28 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.42.3-1
- PLAT-7173 - KMC ADV tab: When changing duration at cuepoint2 ->Duration at cuepoint1 is updated.
- Ver bounce of HTML5 to v2.59

* Mon Jul 17 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.42.1-1
- Ver bounce of HTML5 to v2.58.2
- PLAT-7659 - Change Opera Syndication Feed Name

* Mon Jul 3 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.42.0-3
- Ver bounce of HTML5 to v2.58.1

* Thu Jun 1 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.42.0-2
- Ver bounce of HTML5 to v2.57

* Thu May 18 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.42.0-1
- Ver bounce of HTML5 to v2.56
- PLAT-7022 - New Syndication Feeds

* Wed Apr 25 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.41.2-9
- Added kmc_preview_dark.json to KMC's config.ini so that, in preview and embed, an HTML5 player will be loaded when selecting "KDP3 Dark"

* Tue Apr 24 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.41.2-8
- Ver bounce of HTML5 to v2.55.2

* Tue Apr 20 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.41.2-7
- Ver bounce of HTML5 to v2.55

* Tue Mar 29 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.41.2-6
- Ver bounce of HTML5 to v2.54.1

* Thu Mar 9 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.41.2-4
- Ver bounce of HTML5 to v2.54

* Mon Feb 26 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.41.2-4
- Ver bounce of HTML5 to v2.53.2

* Mon Feb 13 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.41.2-3
- Ver bounce of HTML5 to v2.53

* Mon Jan 30 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.41.2-2
- Ver bounce of HTML5 to v2.52

* Wed Jan 4 2017 Jess Portnoy <jess.portnoy@kaltura.com> - v5.41.2-1
- PLAT-6669 - Change the default value of the recording status from "append Recording" to "New Per Session"
- PLAT-6634 - Changes to "Publishers Bandwidth and Storage Report" - front end
- PLAT-6656 - Changes to "Publishers Bandwidth and Storage Report" - front end

* Mon Dec 19 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.41.1-3
- Ver bounce of HTML5 to v2.51

* Tue Dec 6 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.41.1-1
- PLAT-6257 - Add Average Accumulative Storage to Publisher Bandwidth and Storage Report
- PLAT-6211 - create "re-generate token" button in KMC

* Tue Nov 22 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.3-6
- Ver bounce of HTML5 to v2.50

* Thu Nov 3 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.3-5
- Ver bounce of HTML5 to v2.49

* Mon Sep 26 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.3-4
- Ver bounce of HTML5 to v2.48.1

* Fri Sep 23 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.3-3
- Ver bounce of HTML5 to v2.48

* Mon Sep 5 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.3-2
- Ver bounce of HTML5 to v2.47

* Tue Aug 2 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.3-1
- PLAT-5729 - Hide RTSP links from KMC as they are not supported
- PLAT-5667 - Support Trimming & Clipping on Remote Storage
- PLAT-5639 - Distributor connector k2k issue
- PLAT-5753 - Adopt KMC for iCal ingestion from dropfolder and bulk upload

* Tue Jul 19 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.2-5
- Ver bounce of HTML5 to v2.45.1

* Tue Jul 5 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.2-3
- Ver bounce of HTML5 to v2.45

* Fri Jun 3 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.2-2
- Ver bounce of HTML5 to v2.44

* Sun May 8 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.2-1
- PLAT-5420 - Export FMLE XML in KMC/KMS: key frame interval should be 2 seconds instead of 3 seconds

* Sun Apr 10 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.1-5
- Ver bounce of HTML5 to v2.42

* Fri Mar 11 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.1-4
- Ver bounce of HTML5 to v2.41

* Sun Feb 14 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.1-3
- Ver bounce of HTML5 to v2.40

* Tue Feb 2 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.1-2
- Drop exec bit where unneeded.

* Sun Jan 31 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40.1-1
- New release.

* Sun Jan 17 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v5.40-1
- SUP-5740 - Co-editor/Co-publisher in the KMC
- PLAT-3962 - Core QA for VPaaS Usage Dashboard

* Mon Dec 21 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.11-6
- Ver bounce of HTML5 to v2.38.1

* Sat Dec 19 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.11-5
- Ver bounce of HTML5 to v2.38

* Sun Dec 6 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.11-4
- Ver bounce of HTML5 to v2.37.3

* Fri Nov 20 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.11-3
- Ver bounce of HTML5 to v2.37.1

* Wed Nov 18 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.11-1
- SUP-4977 - Administration tab in KMC does not load on Mac in chrome, safari, or firefox

* Thu Nov 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.10-1
- SUP-5939 - Missing players when listing players for syndication

* Fri Oct 23 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.9-3
- Ver bounce of HTML5 to v2.36

* Fri Oct 9 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.9-2
- Ver bounce of HTML5 to v2.35.5
 
* Thu Sep 17 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.9-1
- Update KMC listing of live streaming ingest points to use _1 instead of _%i
- Version bounce to align with kaltura-html5lib v2.35.

* Thu Aug 20 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.8-2
- Version bounce to align with kaltura-html5lib v2.34.

* Thu Aug 6 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.8-1
- Version bounce to align with server 10.17.0.

* Fri Jul 24 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.6-1
- PLAT-3409 - CustomData.System name with underscore is not supported by KMC->Mapping fields fail.

* Sun Jun 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.3-4
- Ver bounce of HTML5 to v2.32.1

* Sun Jun 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.3-3
- Ver bounce of HTML5 to v2.32

* Sun Jun 14 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.1-3
- SUP-4926 - Wrong KMC owner accounts - change to right account not saved

* Sun May 31 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.1-3
- New HTML5 lib - v2.31.

* Mon May 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.1-2
- New HTML5 lib.

* Sat Apr 25 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.1-1
- SUP-4303 - A redundant message when creating or editing a conversion profile
- PLAT-2796 - User get error messages on transcoding setting screen when user role sets with "transcoding setting-view only"
- PLAT-2815 - Cannot save current transcoding profile without flavors

* Sun Apr 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.38.11-1
- SUP-3963 - Issue with Date time field in the Video Metadata
- SUP-4105 - Error is thrown when accessing upload center
- SUP-4009 - Unable to change account owner
- PLAT-2608 - Link to live analytics exits on content tab when user dont have permissions to analytics

* Mon Mar 9 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-2
- new HTML5 lib ver.

* Sat Feb 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-1
- Ver bounce.

* Sun Feb 8 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.9-1
- SUP-3658 - KMC Error Message and Crash
- SUP-3681 - KMC doesn't set required tags when logging as a "Content Moderator" role
- FEC-2653 - KMC: after click on Studio tab, the flash studio appears for 1-2 seconds and after U.studio loaded
- FEC-2654 - KMC: If select Flash Studio, after U. Studio and refresh the web page - Flash studio loaded

* Sun Jan 25 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.8-1
- SUP-3531 - Analytic data inconsistency in certain scenario

* Wed Jan 7 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.7-4
- Copy the entire doc tree to web/content/docs.

* Wed Jan 7 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.7-1
- PLAT-2243 - kmc - kms categories Bulk delete Warning message is incorrect
- PLAT-2242 - KMS \ KMC _edit warning category- Warning is not provided when changing between catrgoried 

* Sun Dec 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.4-2
- Bounce versions in config.

* Sun Dec 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.4-1
- Support for Live Analytics
- Prevent player v2 from throwing live events from KMC
- PLAT-2157 - Akamai live streaming exported XML should specify video format 
- PLAT-1703 - Add a warning in KMC when user trying to edit/delete one of KMS native categories 

* Thu Dec 11 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.30-1
- PLAT-2157 - Akamai live streaming exported XML should specify video format
- PLAT-1703 - Add a warning in KMC when user trying to edit/delete one of KMS native categories
- FEC-2282 - Lead with Universal studio ( instead of flash ) when pressing studio in KMC
- SUP-3269 - Edit Entry window of live entry with Manager KMC role
- PLAT-2081 - New live transcording profile is added to new streaming window just after refreshing KMC browser
- PLAT-1908 - Missing exception on approve content when user does not have permission
- PLAT-2223 - KMC - New Transcoding Profile - The creation of a new transcoding profile redirects the KMC to the Content tab (once per session) 

* Mon Dec 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.27-4
- HTML5lib bounce to v2.22.

* Tue Nov 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.27-3
- Bounce HTML5 lib ver in config.ini to v2.21.

* Sun Nov 2 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.27-2
- Bounce HTML5 lib ver in config.ini to v2.20.

* Sun Oct 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.27-1
- PLAT-1681 - KMC- Manual livestream entry has "hdnetworkmanifest" livestream configuration though no HDS url was configured
- SUP-2392 - Disable editing of existing webvtt captions as well as not allow adding new ones (was "Webvtt upload from the KMC is not working")
- SUP-2817 - KMC Date/Time bug

* Sun Sep 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.24-1
- ver bounce.

* Sun Aug 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.22-2
- Upped HTML5 version

* Thu Jul 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.22-1
- PLAT-1342 - Reflect replacement ERROR status in the KMC
- PLAT-1389 - New Access Control Profiles are missing "Allow All" settings for IPs (the default access control profile is missing it too)
- FEC-1463 - on line help - broken links to live reports and live transcoding profiles' pages
- PLAT-340 - B&S report is cut in KMC while using resolution low then 1400 * 1050 

* Sat Jun 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.21-1
- PLAT-974 - add partner Reference ID to KMC and Multi-Account console

* Wed May 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.20-2
- Bounce the HTML5 and KMC versions in config.

* Wed May 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.20-1
- PLAT-671 - KMC - Bulk Action - Remove Tags - Causes popup when opening category
- FEC-1302 - security-fix (Oracle) - KMC support form does not validate input on GET parameters (XSS)
- FEC-1402 - CLONE - security-fix (Oracle) - KMC support form does not validate input on GET parameters (XSS)

* Wed May 7 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.17-6
- Added URL pointing to GIT repo.

* Sat Apr 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.17-3
- Bounce KMC and HTML5lib vers in config.ini.

* Thu Apr 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.17-1
- PLAT-1242 - Uploading a "m4a" file from desktop - the file media type is not automatically chosen
- PLAT-1265 - KMC online guide broken link on submitbulkoptions.htm

* Sun Apr 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.16-1
- Live Reports in Analytics (phase 0)
- Legacy embed code removed from Preview & Embed page for Players falling back to HTML5 v2
- SUP-1713 - Analytics categories filter is not needed 
- FEC-1131 - When only universal studio is enabled for partner - the main studio menu is not displayed at all in KMC 

* Wed Mar 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.14-3
- kmc_config.ini updated with new kmc ver.

* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.14-1
- SUP-1581 - Remix feature is exposed to customers in Old KDP templates
- KMC - After closing the "Support" page, the KMC is not usable
- PLAT-1038 - Closing the "Preview & Embed" page is causing a change in the KMC's layout

* Sun Mar 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.12-1
- Upgrade to 5.37.12, fixes:
  SUP-1634 - KMC will not alert when the user is uploading a file that is larger than 2GB using upload from desktop 
  PLAT-994 - enable use of draft entries in playlists - when video media is not expected 
  PLAT-985 - "Copy" button in "Preview & Embed" page is not working 
- Removed the limitation of not being able to create a transcoding profile with no flavors.
- Added the ability to choose transcoding profile for draft entry based on the permission "Enable KMC transcoding profile selection for draft entries".

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.11-1
- Upgrade to 5.37.11, fixes:
  SUP-1491 - Cannot configure content distribution role Ready for Deployment
  SUP-1265 - SEO values not populating Ready for Deployment
  SUP-1382 - KMC Return 2 Source flavors Ready for Deployment 

* Fri Feb 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v3.37.10-17
- Yet another symlink needed in %%post

* Wed Feb 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v3.37.10-16
- Fix preun error.

* Wed Feb 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v3.37.10-14
- docs added

* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v3.37.10-11
- Since these widgets typically reside on NFS and served from another machine there is not need for the Apache dep.

* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-10
- Moving to KDP3 v3.9.7.

* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-9
- Added nab UI confs.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-7
- Added dep on kaltura-html5-studio

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-4
- Replace version in base.ini

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-2
- Added the login dir.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-1
- Ver bounce.

* Fri Jan 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.36.10-1
- initial package.
