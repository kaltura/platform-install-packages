%define prefix /opt/kaltura
%define html5lib3_base %{prefix}/html5/html5lib/playkitSources/kaltura-ovp-player

Summary: Kaltura Open Source Video Platform 
Name: kaltura-html5lib3
Version: 1.7.5
Release: 2
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.gz 
Source1: create_playkit_uiconf.php

URL: https://github.com/kaltura/kaltura-player-js 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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

This package installs the Kaltura HTML5 v3 player library.

%prep
%setup -q -n %{version} 

%install
mkdir -p $RPM_BUILD_ROOT%{html5lib3_base}/%{version}
cp -r * $RPM_BUILD_ROOT%{html5lib3_base}/%{version} 
cp %{SOURCE1} $RPM_BUILD_ROOT%{html5lib3_base}/

%clean
rm -rf %{buildroot}

%post

%postun

%files
%defattr(-, root, root, 0755)
%{html5lib3_base}

%changelog
* Thu Jul 8 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 1.7.5-2
- New RAPT (0.44)
- New QnA (2.1.2)

* Mon Jun 14 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 1.7.5-1
- FEC-11304: missing entryId on plugins (#453)
- Downgrade playkit.js-ui to v0.66.0
- Update playkit.js to 0.71.0 (b148b26)
- Update playkit.js-dash to 1.25.0 (155d5f3)
- Update playkit.js-hls to 1.26.0 (8305089)
- FEC-10381: sources config need to be passed via setMedia api (#440) (2e91c65)
- FEC-11281: youbora reporting buffering during playback (#450) (fcc7234)
- SUP-26832 - Rapt video player scrubber is the top of the video
- First version of dual screen plugin

* Wed May 5 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 1.7.0-1
- update playkit.js to 0.70.0 (2e8311f)
- update playkit.js-dash to 1.24.2 (4974cf8)
- update playkit.js-hls to 1.25.1 (59e35e2)
- update playkit.js-ui to 0.65.3 (874f0be)
- FEC-11091: add support for XMLHttpRequest.withCredentials in request filter (#438) (5ccdc1a)
- FEC-11126: upgrade Shaka to 3.0.10 (#434) (18bafd6)

* Mon Apr 26 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 1.6.1-1
- FEC-10281: chromecast does not work after playing it once and trying it on another video (#417) (42e7939)
- FEC-10405: set capabilities manually on iOS devices when airplay is configured (#422) (d16d4b1)
- FEC-11057: ima postroll doesn't play when imadai configured before (#424) (a838ea5)
- FEC-11062: ad layout doesn't work when IMA DAI configured (#425) (2251d5f)
- FEC-11089: bumper preroll doesn't play after ima preroll (#428) (cd7a287)
- FEC-11077: expose api for restart the media source (#427) (145f53c)
- FEC-10541: add support on working with bidding, Prebid and IMA (#412) (0f21b24)
- FEC-10941: Use In-Stream DASH thumbnails on the timeline (#423) (33bc80c)
- remove thumbnail height from thumbnail service call (#421) (9611685)
- FEC-11037: multiple decorator exist after destroy plugin with decorator (#418) (9e9685c)
- FEC-11041: player fails in IE11 (#419) (3f16f12)
- FEC-11041: player fails in IE11 (#419) (52f9bc1)
- FEC-11041: player fails in IE11 (#419) (84a37bd)
- FEC-10872: loadMedia returns the provider response instead of the updated one (#405) (d26013d)
- FEC-10995: update Shaka to 3.0.8 (#411) (e40bc1e)
- FEC-10041: playAdsWithMSE with DAI detach the playback and ad (#408) (d7b5e09)
- FEC-10640: add api to get the playlist current working item index (#413) (7e59c37)
- FEC-10768: expose in-stream DASH thumbnails (#415) (9581fa1)
- FEC-10961: show the thumbnail preview in live (#407) (c1ac3fe)
- FEC-10970: expose vpaid field on ad object (#410) (2db9ce8)
- FEC-11013: upgrade to hlsjs latest (0.14.17) (#414) (863b18d)
- ads-controller: sources.startTime isn't always exists and can change from source to source (#399) (3965295)
- FEC-10687: Allow partial config in setMedia API (#394) (aab1eab)
- FEC-10945: ad / bumper isn't paused with autoPause (#404) (6495047)
- update Shaka to fix the memory leak (#396) (f6cc4dd)
- FEC-10686: move startTime config from playback to sources (#398) (bf909e0)
- FEC-10709, FEC-10712: player visibility - Auto-pause when player is out of view, Autoplay only when player is in view (#395) (d1d3feb)

* Mon Feb 1 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 1.3.0-2
- Added `timeline` plug and updated versions for some others

* Wed Jan 20 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 1.3.0-1
- Added the following plugins: live, navigation, qna, hotspot and transript
- FEC-10680: back-end bumper: the app should decide what bumper will be displayed when also set user bumper (#392) (a062427)
- FEC-10729: forceRedirectExternalStreams is reset in playlist (#381) (77e86ec), closes #370
- FEC-10732, FEC-10759: player params are not injected to additional instances config (#385) (8c5a6c7)
- FEC-10776: set the plugins event registration after kaltura player internal events (#383) (4233d9f)
- FEC-10797: back-end bumper config is left from previous media played (#393) (f3905e7)
- FEC-10806: playlist has limitation which configure cause setMedia (#390) (c5caeda)
- FEC-10015: support smart scrubber preview and timeline marker (#359) (ed9606a)
- FEC-10766: create text config section and option for styling (#387) (dac194d)

* Mon Nov 9 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 1.0.5-1
- FEC-10469: pre-roll Ad for playlist displays for each second media instead of for each one (#367) (c3a52cd)

* Wed Oct 21 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 1.0.3-1
- FEC-10161: add kava analytics url from server response (#355) (e4ce3f1)
- FEC-10275: Bumper incorrectly recognised as ad (#352) (716d01a)
- FEC-10417: playlist by sources stuck after press Play button when set IMA or bumper plugins (#349) (b2256f3)
- FEC-10455: incorrect order in reset and destroy process (#353) (fc9bf96)
- FEC-10468: PLAYBACK_START not fired on autoplay (#356) (78c3ed5)
- FEC-10076: add support for dynamic injection (#351) (b9e9a31)
- FEC-10296: upgrade hls.js to 0.14.9 (#348) (2d0ec6e)
- FEC-10435: upgrade shaka for fixing live issue and optimizations for smartTV (#354) (90ce625)
- FEC-10347: expose kaltura player as a global variable instead of UMD (#350) (b6253ff)
- FEC-10347: kaltura-player is not UMD anymore
- DRM doesn't play on edge chromium (#364) (cc4cce4)

* Sun Aug 9 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 0.56.0-1
- New RAPT plugin (0.4.2)
- Downgrade shaka from 3.0.x (#346) (f126796)
- Old browser(IE11) get mehtod in proxy doesn't work (#345) (4d3f69c)
- FEC-10356: 4K DASH HEVC + LIVE doesn't play correctly on LG (#342) (111cdac)
- FEC-10057: move the plugin manager to kaltura player (#332) (66b2f3d)
- FEC-10290: upgrade NPM packages (#335) (07fa73b)
- FEC-10291: migrate analytics plugins injection from kaltura player to server (#337) (1caf168)

* Fri Jun 26 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 0.54.0-2
- New RAPT plugin (0.4.0)

* Wed Jun 10 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 0.54.0-1
- FEC-10053: Subtitle issue for Player with TTML in MP4 container (#316) (c053ac2)
- FEC-10155: text track language is incorrect on cast disconnecting (#318) (75690a3), closes #188
- FEC-9631: add support for out of band text tracks on cast sdk (#319) (16562b6)

* Thu May 21 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 0.53.7-1
- FEC-9109: add DRM Load time metric (#305) (e0b267e)
- Remove French (fr) translation file (5529611)
- FEC-9734: auto play doesn't works, if "playsinline"=false on all platforms (#307) 
- New RAPT plugin (0.2.4)

* Mon Mar 16 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 0.51.3-2
- New RAPT/PATH ver - 0.1.12

* Fri Dec 27 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.51.1-1
- FEC-9471, FEC-8436, FEC-8443: slider progress bar exceeds 100% (#287) (a617eae)
- FEC-9175: cast content coming from external sources (#288) (43a46b2)

* Mon Nov 25 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.49.0-1
- config keySystem isn't boolean (#283) (4280dc5)
- New hasUserInteracted api (#284) (6855309)
- FEC-9307: live issue on LG SDK2 with hls.js (#273) (1ca1b5d)
- FEC-9379: Edge chromium should use playready when exist (#274) (6b87274)
- FEC-9326: report productVersion (#275) (304f9ca)
- FEC-9389: media playing unmuted after unmute fallback (#272) (dafa0d6)

* Mon Sep 16 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.46.0-1
- playkit-js 0.53.0
- playkit-js-dash 1.15.0
- IMA plugin - 0.17.2

* Mon Aug 5 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.45.5-1
- Added the bumper and Youtube plugins

* Fri Apr 12 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.37.3-2
- Added RAPT plugin

* Tue Feb 12 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.37.3-1
- First release
