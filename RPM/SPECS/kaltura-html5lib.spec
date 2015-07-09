%define prefix /opt/kaltura

Summary: Kaltura Open Source Video Platform 
Name: kaltura-html5lib
Version: v2.32.1
Release: 1
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
Source10: kaltura-html5lib-v2.20.tar.gz
Source11: kaltura-html5lib-v2.21.tar.gz
Source12: kaltura-html5lib-v2.22.tar.gz
Source13: kaltura-html5lib-v2.23.tar.gz
Source14: kaltura-html5lib-v2.24.tar.gz
Source15: kaltura-html5lib-v2.25.tar.gz
Source16: kaltura-html5lib-v2.26.tar.gz
Source17: kaltura-html5lib-v2.27.tar.gz
Source18: kaltura-html5lib-v2.28.tar.gz
Source19: kaltura-html5lib-v2.29.tar.gz
Source20: kaltura-html5lib-v2.30.tar.gz
Source21: kaltura-html5lib-v2.31.tar.gz
Source22: kaltura-html5lib-v2.32.tar.gz

URL: https://github.com/kaltura/mwEmbed 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: php

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
tar zxf %{SOURCE9} -C %{_builddir}/
tar zxf %{SOURCE10} -C %{_builddir}/
tar zxf %{SOURCE11} -C %{_builddir}/
tar zxf %{SOURCE12} -C %{_builddir}/
tar zxf %{SOURCE13} -C %{_builddir}/
tar zxf %{SOURCE14} -C %{_builddir}/
tar zxf %{SOURCE15} -C %{_builddir}/
tar zxf %{SOURCE16} -C %{_builddir}/

tar zxf %{SOURCE17} -C %{_builddir}/
tar zxf %{SOURCE18} -C %{_builddir}/
tar zxf %{SOURCE19} -C %{_builddir}/
tar zxf %{SOURCE20} -C %{_builddir}/
tar zxf %{SOURCE21} -C %{_builddir}/
tar zxf %{SOURCE22} -C %{_builddir}/

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib
for i in v2.1.1 v2.3 v2.4 v2.6 v2.9 v2.14 v2.15 v2.18.5 v2.20 v2.21 v2.22 v2.23 v2.24 v2.25 v2.26 v2.27 v2.28 v2.29 v2.30 v2.31 v2.32.1 %{version};do
	cp -r %{_builddir}/%{name}-$i $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/$i
	cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/$i
done
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
* Sun Jun 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.32-1
- FEC-3632 - Supprot all tremor ad substitutions
- FEC-3640 - Support large play button when DFP ads are paused.
- SUP-4897 - Download button leads to error
- SUP-4856 - SRT files with Mac line endings do not load
- SUP-4845 - YouTubePlayer should forceIframe by default
- SUP-4843 - Low quality in bumper ads
- SUP-4825 - SRT captions color change dynamically
- SUP-4277 - Mediahuis - Windows Phone 8.1 black screen on playback
- SUP-4182 - Firefox issue with right click menu
- SUP-4564 - Image while broadcasting live audio stream
- SUP-3568 - Change Iframe title from "Kaltura Embed Player iFrame" to the player's title
- SUP-4998 - Query - Defining one thumbnail URL for all entries while using thumbnail embed
- SUP-5070 - abChecker plugin not working
- SUP-4857 - Accessibility issue
- SUP-5051 - Universal Player probes for Java's runtime
- SUP-5002 - Captions issue with player version 2.31 in Desktop and Android
- SUP-3590 - Translating error message from English to Dutch


* Sun May 31 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.31-1
- FEC-3185 - Add paging ability to core playlist
- FEC-3504 - Add playSessionId to each playmanifest
- FEC-3502 - Do not display slides, scubber or chapters when no DVR info is avalaible
- FEC-2412 - Support configuration on flavor selector to display bitrate instead of size
- SUP-4030 - Letterboxing bug when setting player for live stream
- SUP-4589 - GroovyGecko - Google Analytics urchinCode plugin
- SUP-4509 - Downloading a specific flavor
- SUP-4237 - Rate Selector - speed conversion not working properly 
- SUP-3568 - Change Iframe title from "Kaltura Embed Player iFrame" to the player's title
- SUP-4621 - Player Analytics regression around statistics properties
- SUP-3383 - "Install Flash" message not shown on IE8
- SUP-3590 - Translating error message from English to Dutch 
- SUP-4572 - issue with video on application for iOS devices
- SUP-4129 - Page zoomed in after exiting fullscreen
- SUP-4678 - Full screen issue in Android Galaxy Note and Galaxy S3

* Mon May 4 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.30-1
- FEC-3100 - Support DFP player identification
- SUP-3177 - [v2.20] Player stuck when seeking on Firefox/OSX, webm flavor
- SUP-3404 - Youtube videos will not load if Audio Description Plugin Enabled
- SUP-3569 - Flicking TTML captions
- SUP-3648 - Pausing on iPhone jumps to 00:00:15
- SUP-3684 - Thumbnail at the end of a live stream
- SUP-3864 - Download gets cut for large flavors
- SUP-4003 - language of default captions will be chosen by browser language
- SUP-4077 - Video Player Voice Over Accessibility Issue
- SUP-4168 - [2.28] No progress or countdown indication for a DoubleClick ad
- SUP-4213 - Video quality drop with player version 2.28 - preferedFlavorBR not respected
- SUP-4250 - VAST preroll not respected in 2.28 on mobile.
- SUP-4277 - Mediahuis - Windows Phone 8.1 black screen on playback
- SUP-4473 - 2.29: "Stack overflow at line: 0" at end of playback on IE8
- SUP-4546 - Embed code for video with chaptering is not loading
- SUP-3314 - Player dimensions in Universal Studio 
- SUP-4232 - Black screen in IE when viewing videos in full screen
- SUP-4051 - Downloading from player yields 0 bytes files

* Sun Apr 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.29-1
- SUP-3340 - Live stream freezes for a few seconds when streaming with KRecord
- SUP-4096 - [2.27.1] document.onclick is kept even after player is gone
- SUP-3793 - No video playing
- SUP-4018 - Thumbnail isn't Displayed in Audio Playlist
- SUP-3984 - [2.28-rc8] Previous captions <track> elements not removed from <video> upon changeMedia
- SUP-3944 - [2.27.1] EmbedPlayerYouTube fails with an exception
- SUP-4137 - v2.28 broken hotkey functionality (End Key)
- SUP-4119 - Handle hidden iframe player loading and display
- SUP-4198 - [BankOfAmericaSaaS] Captions request is being blocked
- SUP-3684 - Thumbnail at the end of a live stream
- SUP-4189 - Kaltura Player versions greater than 2.22 don't handle onTextData event data properly - Kaplan
- SUP-4118 - issues with SpotXchange integration
- SUP-3367 - V2 player fires 2~3 'doPlay' events when using the related videos
- SUP-3369 - Captions on live stream don't show (manual live streaming)
- SUP-3960 - Ad tag issue - KDP

* Sun Mar 8 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.28-1
- FEC-417 - Player 2.0 - Share & Embed functionality
- FEC-2866 - Enable multi-stream for iPad viewers
- FEC-2918 - Add uiconf id to Google Analytics
- FEC-2620 - Support vast loadAdsOnPlay property
- SUP-3996 - Playlist player issus, BOA
- SUP-3967 - Player requests undefined ciu_szs param
- SUP-3649 - Adding Class to Spinner using Custom CSS | HTML5 Player
- SUP-3888 - [2.27.1] Captions cookie does not take any effect
- SUP-3830 - Player stuck on spinning in iOS after changeMedia is called
- SUP-3783 - Player and KMC not showing all the captions available
- SUP-3641 - playlist section vs. video section
- SUP-3849 - Downloading from player causes no extension on Firefox+Mac
- SUP-3858 - [2.26-2.27] Captions text color doesn't apply
- SUP-3850 - HDS source selector broken in 2.24-2.27
- SUP-3781 - Captions supported in KDP does not in HTML5
- SUP-3629 - Postmedia No playerPlayed event after prerolls and before contnet with DFP ads
- SUP-3340 - Live stream freezes for a few seconds when streaming with KRecord

* Sun Feb 8 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.27-1
- SUP-3485 - Chapter playlist gaps and unresponsive in external URL (standalon page) | V2 player | Chapters plugin
- SUP-3559 - Player gives a "No source video was found"
- SUP-3616 - JS player API. changeMedia doesnt work
- SUP-3687 - HDS\HLS mediaPlayFrom\To does not work.
- SUP-3772 - preferred bitrate
- FEC-2055 - Playhead switch events are missing on all browsers (was: "Playhead switch events - Duration line has not been added under video on IE8") 
- FEC-2753 - Lecture capture Multiple stream: black screen instead of video when change stream on iPad
- FEC-2773 - Lecture capture : Chapters and switching streams - Timer & slide is wrong on iPad
- FEC-2809 - Related video does not work in FireFox on production

* Sun Jan 25 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.26-1
- SUP-3609 - Misplaced playback on iPad with 2.24 & 2.25
- FEC-2611 - Chapters/Slides Menu (revised) - Playback

* Sun Jan 11 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.25-1
- FEC-2611 - Chapters/Slides Menu (revised) - Playback
- FEC-1997 - lecture Capture - search , search results, no results.
- FEC-1971 - Support VPAID events mapping to VAST events
- SUP-3067 - Default captions malfunction 
- SUP-3396 - captions do not appear on v2 players
- SUP-3252 - doStop() function malfunction.
- SUP-3429 - Clipped duration not displayed on page load, but only after play 
- SUP-2937 - Thumbnail message in the beginning of entries
- SUP-3502 - HLS playback fails due to access control
- SUP-3496 - Change image file name when download with Universal studio
- SUP-3480 - Playlist player layout display issues in iOS/Android
- FEC-2594 - Playhead segment doesn't works - the video started to play from beginning
 
* Sun Jan 4 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.24-2
- Neglected to include v2.21 v2.22 v2.23
- Use a for loop to iterate on vers.

* Sun Dec 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.24-1
- FEC-1764 - Playback rate should support video tag interface switch.
- PS-1987 - PostMedia: Failed to block playback of domain restricted entries
- PS-1967 - (INTLKVP-133) Ads not played on Android stock browser
- PS-1912 - (INTLKVP-114) Ad completed event is not reported for post-roll on iPad Air (iOS 8)
- PS-1988 - PostMedia-iPad-iPhone-S4-nexus: Failed to load Geo Restricted playlist
- SUP-3377 - Universal player download button doesn't work right with image
- SUP-2991 - 508 v2 player - Audio description does not rewind
- SUP-2604 - Player don't load when "Rate Selector" is enabled | V2 player | customer site only
- SUP-3341 - [v2.22.1] changeMedia does not make player exit sharing
- SUP-3344 - Android 5.0 playback doesn't work | HTML 5 player
- SUP-3256 - [2.21] Fullscreen button does not lose focus; space exits fullscreen
- SUP-3290 - DFP Vast not working in IE9
- SUP-3393 - "changeMedia" notice failure to update segments or stream url

* Sun Dec 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.23-1
- FEC-2316 - Support Akamai Media Analytics Logging for forceKPlayer flash mode
- FEC-2315 - Create Strings plugin demo page expand override to all keys
- FEC-2350 - DFP plugin should support pauseAdOnClick with default true
- FEC-2281 - VAST plugin should support pauseAdOnClick with default true
- SUP-28 - Design live UI buttons and user flow
- FEC-869 - Playhead should dynamically adjust per available DVR 
- FEC-1998 - Lecture Capture - select video stream
- SUP-3319 - Ad beacon don't fire the 100% track | V2 player
- SUP-3243 - Configure player logo to a non-clickable logo doesn't work on Firefox
- SUP-2985 - changeMedia notification from audio entry to video entry causes first-frame-freeze
- SUP-2604 - Player don't load when "Rate Selector" is enabled | V2 player | customer site only
- SUP-3322 - Playlist entries list is not responsive even tough video section is responsive.| Player V2

* Mon Dec 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.22-1
- SUP-3001 - Pre-roll ads don't show and player freezes on iPad+iOS8+Safari (2.19.5)
- SUP-3078 - Source Selector display in bitrate instead of pixels when using HDS/Akamai/RTMP delivery
- SUP-2943 - Long titles wrap and distort elements on the top bar container
- SUP-3128 - Video thumbnail stretch in the iOS 8 web view and lose it aspect ratio.
- SUP-3132 - Control Bar Icons are not transparent
- SUP-3175 - Playlist disappears and full screen icon is incorrect when returning from fullscreen mode
- FEC-2150 - Buffer underrun should not cause "media not found" message

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
