%define prefix /opt/kaltura

Summary: Kaltura Open Source Video Platform 
Name: kaltura-html5lib
Version: v2.21
Release: 2
Epoch:0 
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/mwEmbed/tarball/%{name}-%{version}.tar.gz 
Source1: LocalSettings.php
Source2: kaltura-html5lib-v2.1.1.tar.gz
Source3: kaltura-html5lib-v2.3.tar.gz
Source4: kaltura-html5lib-v2.4.tar.gz
Source5: kaltura-html5lib-v2.6.tar.gz
Source6: kaltura-html5lib-v2.9.tar.gz
Source7: kaltura-html5lib-v2.14.tar.gz
Source8: kaltura-html5lib-v2.15.tar.gz
Source9: kaltura-html5lib-v2.18.5.tar.gz
URL: https://github.com/kaltura/mwEmbed 
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

This package installs the Kaltura HTML5 library.

%prep
%setup -q
tar zxf %{SOURCE2} -C %{_builddir}/
tar zxf %{SOURCE3} -C %{_builddir}/
tar zxf %{SOURCE4} -C %{_builddir}/
tar zxf %{SOURCE5} -C %{_builddir}/
tar zxf %{SOURCE6} -C %{_builddir}/
tar zxf %{SOURCE7} -C %{_builddir}/
tar zxf %{SOURCE8} -C %{_builddir}/


%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib
cp -r %{_builddir}/%{name}-%{version} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/%{version}
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/%{version}
cp -r %{_builddir}/%{name}-v2.1.1 $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.1.1
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.1.1
cp -r %{_builddir}/%{name}-v2.3 $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.3
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.3
cp -r %{_builddir}/%{name}-v2.4 $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.4
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.4
cp -r %{_builddir}/%{name}-v2.6 $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.6
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.6
cp -r %{_builddir}/%{name}-v2.9 $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.9
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.9
cp -r %{_builddir}/%{name}-v2.14 $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.14
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.14
cp -r %{_builddir}/%{name}-v2.15 $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.15
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.15
cp -r %{_builddir}/%{name}-v2.18.5 $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.18.5
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/v2.18.5

%clean
rm -rf %{buildroot}

%post

%postun

%files
%defattr(-, root, root, 0755)
%doc COPYING README.markdown 
%{prefix}/web/html5/html5lib
%config %{prefix}/web/html5/html5lib/%{version}/LocalSettings.KalturaPlatform.php

%changelog
* Mon Nov 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.21-1
- SUP-2939 - Request cookies are missing in header 
- SUP-2423 - Thumbnail in full screen looks bad due to resize
- SUP-2429 - V2 player, maximize/minimize full screen pause issue
- SUP-2808 - Set max # of clips for V2 playlist player via UIVar
- SUP-2926 - Video overlays ads when using "Share"
- SUP-3044 - Vast overlay ads issue

* Sun Nov 2 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.20-1
- FEC-1012 - Player v2: Playlist component support
- FEC-1837 - Add disable mouse hover controls during ad playback controls
- SUP-2317 - Preferred downloaded flavor for download button doesn't persist from V1 to V2
- SUP-2549 - V2 player stuck when "adBlock" is enabled | VAST plugin
- SUP-2802 - Download specific flavor v2 player
- SUP-2833 - Enable initial playlist player poster and disable between videos
- SUP-3038 - autoMute flashvar doesn't always work
- SUP-2841 - V2 LiveRail Countdown Timer Non-Functiona
- SUP-2549 - V2 player stuck when "adBlock" is enabled | VAST plugin


* Sun Sep 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.18.5-1
- ver bounce.

* Sun Aug 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.15-1
- SUP-2413 - window.setInterval cause hTML5 player failure
- SUP-2459 - Multiple "Pause" events
- SUP-2499 - V2 with ad gets stuck before playing the video | Prod site | VAST | pre-roll
- SUP-2292 - 'Expand Player' icon overlaps with video content frame
- FEC-1611 - Video doesn't play when adblock is enabled (vast&Tremor&Doubleclick)
- FEC-1249 - KDP event mapping had mapping to non-existant html5 player events

* Thu Jul 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.14-1
- SUP-2464 - Ellentube V2 Player Issue - Doubleclick plugin is not working when using chromeless
- SUP-2212 - playlist with restricted entries
- SUP-2291 - Thumbnail not displayed when clicking share
- SUP-2317 - Preferred downloaded flavor for download button doesn't persist from V1 to V2
- SUP-2323 - Playlist on V2 player
- SUP-2337 - black rectangle on share screen
- SUP-2381 - NielsenCombined plugin in HTML5 v2 player sends "ci=undefined" instead of clientId
- SUP-2386 - Send Notification "changeMedia" is not working in HTML5 player
- SUP-2427 - Ellentv.com V2 Player - "matchMedia is null" Error (Firefox)
- SUP-2431 - V2 player in iframe embed - close full screen is not working
- SUP-2440 - Player not sending playbackComplete when playback ends
- FEC-1394 - Error An error was experienced when playing the video on Chrome on fullscreen
- FEC-1517 - Need to add the option to navigate from related to a new window instead of switch-media
- FEC-1396 - needless fields in Widevine plugin
- FEC-1531 - imageDefaultDuration=2 is set by default in ui variables plugin 
- PS-988 - Browsers- Volume is always in full when page is refreshed. Doesn't remember last used volume level

* Sat Jun 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.11-1
- SUP-2306 - Bumper Click URL Not Working
- SUP-2198 - Related plugin go into infinite loop
- SUP-1983 - HTML5 v2 - HTTPS embed will not load on HTTP page

* Thu May 22 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.9-2
- Add repo URL to metadata.

* Wed May 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.9-1
- SUP-2048 - Omniture tracking issue on mobile devices
- SUP-2108 - HTML5 V2 player - incorrect display in Share screen
- FEC-1371 - IE9:The alert of missing Widevine Video Optimizer plugin is twisted.
- FEC-1375 - Can't install widevine media optimizer on Firefox Mac.
- FEC-1373 - FF:When pressing on Widevine Video Optimizer plugin link error occurs.

* Thu Apr 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.7-1
- SUP-1856 - [postmedia] sound turned off when next video plays after preroll
- SUP-1884 - changeMedia autoPlay issue
- SUP-1875 - Critical VAST bug for Postmedia
- SUP-1917 - SF 43560 - Postmedia - critical bug in FF
- SUP-1892 - Share URL of HTML5 player does not interpret "magic" substitution
- FEC-1125 - Omniture plugin should support Ad Events
- FEC-1172 - KDP API should remain active during ad playback
- FEC-1189 - PostMedia -- KM-38 : autoMute should not be used on "next" video
- FEC-1195 - Share fails in IE browsers in bad window.open call
- FEC-1196 - PostMedia: first image of video appearing after video is complete
- FEC-1197 - Share url text field is not evaluated in player v2
- FEC-1199 - [ postmedia ] IE9 Browser freezes with the attempt to replay the video
- FEC-1260 - Error on Firefox when changing media after vast pre-roll (with/without auto-play)
- FEC-1257 - ChangeMedia with autoplay does not hide large play button
- FEC-1219 - Custom share link cannot be copied from the link URL because it renders {mediaProxy.entry.id}

* Sun Apr 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.6-1
- FEC-1029 - TAR - JAWS reading buttons twice
- FEC-1173 - "Replay" button needs to be pressed twice for staring to play
- FEC-1160 - merge api fix for related videos failure on identical requests

* Sun Mar 30 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.5-6
- Copy the LocalSettings.php to all packaged HTML5 vers.

* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.5-1
- SUP-1608 - V2 player - Play From Start Time To End Time function not working 
- SUP-1426 - HTML5 v2.0.2 Error message displays when leaving webpage 
- SUP-1580 - Kaltura colored loading wheel showing up instead of custom (IE 8, 9, 10)
- SUP-1717 - share plugin - social networks configurations 
- SUP-1720 - V2 player - Loop uiVar get stuck

* Sun Mar 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.4-1
- SUP-1393 - Player 2.1 with leadwithhtml5 does not work on a secure MediaSpace instance on Safari 
- SUP-1556 - HTML5 Player freezing when playing using Safari. 

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.3-1
  Fixes:
  - Studio V2 support
  - supporting offline download kms app
  - SUP-1365 pass vpaid params to flash as vpaidAdParameter flashvar with encoded value
  - SUP-1461 captions does not work in IE8

* Sun Feb 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.1.1-6
- Fixed https://github.com/kaltura/platform-install-packages/issues/24

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.1.1-5
- LocalSettings.php is ALWAYS the same, it has no custom data, why not just bring it as part of the package??

* Wed Jan 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.1.1-3
- Moved root dir to %{prefix}/web.

* Tue Jan 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.1.1-2
- Added %%doc.

* Tue Jan 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.1.1-1
- initial package.
