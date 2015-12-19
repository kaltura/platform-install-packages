%define prefix /opt/kaltura

Summary: Kaltura Open Source Video Platform 
Name: kaltura-html5lib
Version: v2.38
Release: 1
Epoch:0 
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/mwEmbed/tarball/%{name}-%{version}.tar.gz 
#Source1: LocalSettings.php
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
Source22: kaltura-html5lib-v2.32.1.tar.gz
Source23: kaltura-html5lib-v2.33.tar.gz
Source24: kaltura-html5lib-v2.34.tar.gz
Source25: kaltura-html5lib-v2.35.5.tar.gz
Source26: kaltura-html5lib-v2.36.tar.gz
Source27: kaltura-html5lib-v2.37.1.tar.gz
Source29: kaltura-html5lib-v2.38.tar.gz
Source28: simplePhpXMLProxy.php

URL: https://github.com/kaltura/mwEmbed 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: php, kaltura-base

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
tar zxf %{SOURCE23} -C %{_builddir}/
tar zxf %{SOURCE24} -C %{_builddir}/
tar zxf %{SOURCE25} -C %{_builddir}/
tar zxf %{SOURCE26} -C %{_builddir}/
tar zxf %{SOURCE27} -C %{_builddir}/
tar zxf %{SOURCE29} -C %{_builddir}/

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib
for i in v2.1.1 v2.3 v2.4 v2.6 v2.9 v2.14 v2.15 v2.18.5 v2.20 v2.21 v2.22 v2.23 v2.24 v2.25 v2.26 v2.27 v2.28 v2.29 v2.30 v2.31 v2.32.1 v2.33 v2.34 v2.35.5 v2.36 v2.37.1 v2.37.3 %{version};do
	rm -rf %{_builddir}/%{name}-$i/modules/Widevine
	cp -r %{_builddir}/%{name}-$i $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/$i
	cp %{SOURCE28} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/$i/
	ln -sf %{prefix}/app/configurations/html5.php $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/$i/LocalSettings.php 
	mkdir $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/$i/cache
done
%clean
rm -rf %{buildroot}

%post
find /opt/kaltura/web/html5/html5lib -type d -name cache -exec chown -R 48 {} \; 

%postun

%files
%defattr(-, root, root, 0755)
%doc COPYING README.markdown 
%{prefix}/web/html5/html5lib
%config %{prefix}/web/html5/html5lib/%{version}/LocalSettings.KalturaPlatform.php

%changelog
* Sat Dec 19 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.38-1
- id3 tags support for Live HLS (native and flash)
- id3 tags support improved: time update interval has been reduced to 1 second
- New OSMF-HLS plugin 2.37 + id3 tags code
- FEC-4344 - webcast live event -cant move to old slide que point
- FEC-4433 - Add getLicenseData service in mwEmbed
- FEC-4035 - Support DASH stream with dash everywhere castlabs player
- PS-2381 - Doubleclick skipping two cue point midrolls ad, playing the Ad shows no video only audio
- FEC-4434 - Force playback engine flags don't enforce playable sources selection
- FEC-4427 - comScore Plugin Bugs
- FEC-3720 - Regression:External stream:plugin crushes and the stream is no longer playable
- FEC-3610 - VOD HLS: Player stuck on replay during throttling
- New OSMF-HLS plugin - massive buffers refactor
- FEC-4418 - Support flavorParamsId configuration option against download plugin
- FEC-4446 - silverlight player does not resolve playmanifest 302 redirect header http
- FEC-3832 - heartbeat: add config of heartbeat plugin to studio
- FEC-4431 - clipTo param is trimmed from manifest request when using Flash HDS
- SUP-6647 - alert-container text overflows
- SUP-6602 - no audio playback on Android
- SUP-6584 - Hovering controls subtitles issue
- SUP-6603 - Akamai Analytics: player uses default beacon URL instead of the one defined
- FEC-4389 - Enable player message to be overridden
- SUP-6535 - Change in Google Analytics plugin
- FEC-4462 - HLS OSMF - Seek in Kaltura DVR take more time than in previous player version
- FEC-4459 - HLS OSMF - take around 10-12 seconds to switch from DVR to Kaltura Live
- FEC-4458 - HLS OSMF - Kaltura Live with DVR loaded with 40-50 seconds of delay
- Fix IE8 variable-function name collision
- Fix PHP version syntax issues
- Add PiP plugin to support pip in iOS9
- FEC-4468 - Player layout is wrong in narrow bandwidth
- WB-2151 - Wrong spacing between buttons - OTT skin
- SUP-6143 - Player v2.35 - Icons Display
- FEC-4429 - (ClosedCaptions + playlist + hover-controls + IE8) != love
- FEC-4364 - Hard coded http fonts on some CSS files
- FEC-4125 - server side playback rate- rate selection doesn't work after changing media
- FEC-4472 - Regression : SDK - 2.0.5 Doesn't play any video with player version v2.38.rc9
- FEC-4481 - Regression: the players with autoEmbed type failed to be loaded
- FEC-4314 - if the number of items in the playlist is lower than MinClips, calculate mediaItemWidth according to it, else according to MinClips settings
- FEC-4068 - Display error on unsupported DRM use-cases
- FEC-3832 - trackEventMonitor function added to the studio config
- Fix PS modules not loading
- Fix DASH silverlight cross domain loading
- FEC-2648 - Rate Selector - Rate selector doesn't work in Chrome
- FEC-4503 - Player: While hovering over seek bar, the arrow pointer above it doesn't point to where user points
- FEC-4431 - clipTo param is trimmed from manifest request when using Flash HDS
- FEC-4500 - Channel Playlist - Playlist is not disabled during pre-roll Ad
- FEC-4484 - Improve Native Callout
- FEC-4521 - webcast with no DVR - after stop start of the video the player is freeze.
- FEC-4519 - Kaltura Live isn't starting to play after stop and re-run the stream
- FEC-4068 - DRM playback error handling
- FEC-4524 - Webcast NO DVR- player freeze for 10 sec when open
- Enable using MultiDRM with nativeCallout
- FEC-4533 - Hovering controls: After return from full screen mode, the "pause" button displayed forever on mobile devices
- FEC-4528 - drm playback : replay doesn't work , player stuck on spinning wheel
- Disable inlineScript in mobile devices
- FEC-4068 - Disable DASH on mobile Chrome, use on SDK
- FEC-4548 - start monitor on native onplay event instead of when clicking our play button
- FEC-4557 - Regression: Seek doesn't works for audio entry
- FEC-4554 #comment Reset chapters state on media change
- Fix DFP crash on empty player init
- updated comScoreStreamingTag plugin
- FEC-4554 - Channel Playlist - entry with chapters and slides not playable in channel playlist
- FEC-4561 - Channel playlist: impossible to change slides for audio LC if it part of playlist with Live stream
- KalturaHLS2 plugin removed

* Fri Dec 4 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.37.3-1
- FEC-4446 - Fix issue with playback engine fail resolving URL redirect(HTTP 302)

* Sun Nov 22 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.37.1-2
- Remove unneeded and yet very big modules/Widevine dir while packaging.

* Fri Nov 20 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.37.1-1
- FEC-2823 - Google Analytics configuration in Studio is wrong
- FEC-3724 - uDRM: Modular DRM p2 is not working on IE11 & Edge
- FEC-3937 - Player Share is hardcoded to cdnapi.kaltura.com
- FEC-3982 - Related videos are stretched on fullscreen
- FEC-4063 - Share&Embed: white lines appear after click on some social network icon on FireFox
- FEC-4158 - Strings plugin should support per localization key overrides
- FEC-4236 - Add logic to the flavor selection in Android
- FEC-4253 - Captioning flyout does not disappear as expected
- FEC-4296 - Playlists should support setting playlist width in percentage
- FEC-4328 - Support hide cursor durring fullscreen playback
- FEC-4336 - evars and props do not get updated in playlist
- FEC-4349 - Fix native callout on Android
- FEC-4367 - moderation plugin: Thank you message not localized
- FEC-4394 - Seek race condition prevent seek events propagation in native player
- IVQ integration
- OPF-1572 - Issues with Sub-titles
- PLAT-3590 - Replace existing og:tags in KMC Preview & Embed links to support HTML5 playback on Facebook and Embedly
- Remove unneeded and yet very big modules/Widevine dir while packaging.
- SUP-5575 - Google analytics page display
- SUP-5910 - "EmbedPlayer.HidePosterOnStart" Attribute Overrides "EmbedPlayer.ShowPosterOnStop"
- SUP-5984 - URL Top syndicators
- SUP-5991 - "video content" tooltip is showing while the player loads
- SUP-6057 - Logo stretched on IE 9
- SUP-6097 - Changing playbackRate modifies number of captions
- SUP-6143 - Player v2.35 - Icons Display
- SUP-6313 - Live steam - the stream doesn't starts after the first click on the play button with embed type - thumbnail and embed
- SUP-6372 - Size of cookie request header field exceeds server limit.
- WEBC-581 - keyboard shortcuts are not disabled in in-player Q&A
- fix chromecast HLS support*
- SUP-5072 - YouTube player autoplay fails
- FEC-4417 - IMA issue - When preroll ended the media content ended the player can't replay
- FEC-4414 - Scrubber head is sometimes cut during playback in Chrome latest version
- FEC-4413 - multiple "doStop" notifications causes the video to load in iOS mobile devices
- SUP-6540 - Fallback from Flash to HTML5 v2.36 causes an endless wheel GUI issue
- FEC-3844 - Rate selector: the video started to play at beginning, if seek it and after increase speed
- SUP-6312 - mwe-embedplayer-no-source not respected

* Thu Oct 22 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.36-1
- SUP-5808 - Watermark test page uses outdated attribute names
- SUP-5902 - Video Invisible For Contrast Function of Windows OS
- FEC-3786 - Captions- 'Set as default' button does not work
- FEC-4162 - Channel playlist - playlist button look disabled in live event that had not start
- SUP-5515 - VPAID Overlay positioning issue
- KMS-8968 - In Video Quizzes: Questions are not pop-upped in youtube entry
- KMS-8929 - Channel Playlist - when Live/Webcast Live event should start to play, all playlists entries displayed grey out
- FEC-4155 - regression : HLSMultiAudioFlashTest test page not working
- FEC-3938 - Start Over + Catchup + VOD test support
- FEC-4055 - Android not being able to play stream on Onprem solution, and works fine on SaaS
- SUP-5971 - [2.34 Regression] EmbedPlayer.EnableIpadHTMLControls=false no longer shows native controls
- FEC-4162 - Channel playlist - playlist button look disabled in live event that had not start
- FEC-4151 - v2.35 Error: Using non-prodcution version of kaltura player library.
- FEC-4179 - airPlay plugin doesn't work
- FEC-4080 - Kaltura Live with DVR through HLS failed to be load
- FEC-4200 - Channel playlist: No Vast pre-roll playing before LC entries on iPad
- FEC-4219 - Channel playlist: YouTube entry failed to be start on iPhone if previous entry also has been YouTube
- FEC-3127 - Playlist should support playlist scroll to current entry
- FEC-4255 - Audio starting no from beginning for specific customer's stream
- FEC-4219 - Channel playlist: YouTube entry failed to be start on iPhone if previous entry also has been YouTube
- FEC-4211 - Seek is not not released if performing seek to current position
- FEC-4185 - omniture: name of ad is not reported in the omniture events (vast)
- WEBC-627 - Support multiple presenters/moderators
- FEC-4258 - Google Analytics playr plug-in - setAlllowLinker attribute support
- FEC-3127 - Playlist should support playlist scroll to current entry
- FEC-3967 - scubber doesn't make any progress when playing the AES stream
- FEC-4297 - Playlist with DFP: after seek video, possible to select other entry during Ad that causes to unexpected behavior
- Enable suppressing non production URLs error message
- New Chromecast custom receiver app
- Youbora fixes
- Smart Client fixes
- New HLS plugin
- Correcting Impression and Tracking URL calling for multiple Vast Wrapper feeds.
- Channel playlist dual screen support
- Changed checking for Vast Element in ad XML to explicitely look for an element node.

* Thu Oct 8 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.35.5-1
- IVQ release

* Thu Sep 17 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.35-1
- FEC-4021 - Video is not playing on IOS9 while it has overly
- FEC-4012 - Seek on ios 9 : presents only sound on DFP midroll
- FEC-4010 - Main video on playlist slides down
- FEC-4030 - Switching between slides stack the video on spinner, on IOS-9
- FEC-4032 - Video is not replayed on : Vast pre-roll with interval (IOS-9)
- FEC-4031 - Seek is not working on IOS-9 - spinner is shown
- FEC-4026 - video can't be replayed on IOS-9 in API player
- FEC-4025 - PlaylistReady event is sent untimely (looped) on playlist on IOS-9
- FEC-4028 - Vast postroll playing twice - video does not play and keeps loading forever on IOS-9
- FEC-4029 - Video is not playing while has vast tracking on non-linear ad
- FEC-4016 - Playhead is not updated to progress time on IOS-9 after DFP midroll (audio entry)
- FEC-4011 - Fullscreen is not enlarged to the ios 9 screen entirely
- FEC-3814 - Share & Embed basic - User not able log in to any social media on Microsoft Edge
- FEC-4013 - While seek on IOS-9 in player with DFP pre-mid-postroll - Replay will not work
- FEC-4019 - VMAP_post_linear is not skipped
- FEC-4064 - YouTube playlist - can't change entry
- PLAT-3588 - Add playMainfest paramater for timealign removal of source flavor for wowza live streaming
- SUP-5515 - VPAID Overlay positioning issue
- FEC-4039 - Green marks on the video and video freezes on Firefox
- FEC-3720 - External stream: plugin crushes and the stream is no longer playable
- FEC-4040 - Video is not smooth and jumps
- FEC-4067 - Omniture is not sending additional evars and props to view events
- FEC-4069 - Support load with KS with slashes parameterization ( does not work ?ks param )
- SUP-5512 - Download link not working in versions 2.33
- FEC-4066 - The player don`t display the sync point and the Admin player plays HLS instead of HDS.
- FEC-2522 - Support DFP VAST VPAID engine: Kaltura cuePoints, API invocation and partial mediaProxy cuePoint override
- FEC-4087 - Re-evaluate mediaName before sending the 1st event
- FEC-2693 - Lecture Capture: the LC menu appears also for VOD entries, if LC and VOD included in playlist
- FEC-4088 - The mixed playlist with youtube entries doesn't work properly
- SUP-4784 - Entry duration presented with an additional second
- SUP-5206 - Player CC button - UI issue
- SUP-5184 - Player CC - UI issues
- SUP-5353 - emebed - Full Screen playback on IE9 fails due to domain restrictions
- SUP-5635 - Large button size in a custom style causes misalignment in "Share" screen
- FEC-3173 - Google Analytics: Support custom event category and custom labels
- FEC-4038 - Update Buffer documentation and add buffer duration to events and mediaProxy
- FEC-3905 - Support NPAW youbora analytics plugin
- FEC-4079 - Some entries play with interrupts
- FEC-4094 - In-Video Quizzes: YouTube entry: Playback time & scrubber synchronization issue
- SUP-5573 - Question - player events and logs
- FEC-4091 - Auto play and auto continue don't work for YouTube playlist
- FEC-4090 - spinner stuck on youtube entry after seek
- FEC-4074 - Tokenization for v2.34
- FEC-4096 - YouTube playlist: the playlist doesn't load if delivery type is Kaltura auto or HDS
- FEC-4095 - Source not found player error
- FEC-3820 - ad pod events are not sent to reporting server
- FEC-3559 - allow overriding the ServiceUrl and CdnUrl completely by passing respective flashvars
- FEC-3820 - ad pod events are not sent to reporting server
- SUP-5849 - Scrubber arrow location with aspect ratio
- KMS-8879 - Channel Playlist - Cannot handle upcoming Live/Webcast event
- FEC-4100 - YouTube playlist: need to tap twice on screen in order to pause YouTube entry on Android and iOS
- FEC-4099 - Youtube and KMC playlist: impossible to change playing entry from YouTube to KMC or vice versa on Android and iOS
- FEC-4098 - YouTube playlist disabled after player loads on Android or iOS devices
- FEC-4097 - YouTube playlist with auto play - the video doesn't start, black screen appears on Android and iOS devices
- FEC-4092 - YouTube playlist: black screen in player area appears after refreshing the test page
- FEC-4093 - Lecture Capture: the LC menu/controls appear also for Kaltura live entries in combined playlist
- FEC-3974 - "wrong reference id" message does not appear when using wrong reference id as source
- FEC-4131 - can't play live with ad stitching specific stream
- FEC-4122 - Lecture capture - Video plays in the main screen when stream is selected
- FEC-4120 - Multiple Playlists Monetization - Clicking an overlay ad pauses the video instead of open the target page
- New HLS-OSMF plugin
- Improved IE8 detection *

* Tue Sep 15 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.34-3
- Create cache dir under web/html5/html5lib/$i/cache and set write perms for Apache
- Symlink LocalSettings.php to /opt/kaltura/app/configurations/html5.php
- kaltura-html5lib depends on kConf.php provided by kaltura-base so a Requires: kaltura-base is needed

* Thu Aug 20 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.34-1
- SUP-5551 - Source selector doesn't work after changing media
- SUP-5535 - Large Play button - Bug in "Custom styles"
- SUP-5468 - Font color change in chapters
- SUP-5428 - Image player causes insecure content to load
- SUP-5398 - If flash disabled, player fallback to http progressive and displays auto only in source selector
- SUP-5397 - Scrubber is not released from the cursor after seeking
- SUP-5377 - Cannot change the time label font color
- SUP-5357 - Pause button stop working
- SUP-5356 - Disney - No playback when DoubleClick ad tag is null
- SUP-5262 - VAST Ads - Cause Endless Loop on iPhones 
- SUP-5260 - KMS - editing Clip not working properly
- SUP-5120 - Playback rate selector starts video from beginning when changing rate for first time
- SUP-4913 - Embed code does not play and the player's wheel keep spinning
- SUP-4911 - Postmedia - autoMute parameter is cached
- SUP-4721 - Play button disappears in 2.30 player in IE + iframe embed when in full screen

* Fri Jul 24 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.33-1
- FEC-677 - volumeControl plugin should support verical layout
- FEC-3331 - Support server side playback Rate where not available client side or no progressive stream
- FEC-3678 - Make the entryList param dynamic for the related data 
- FEC-1755 - Adobe Analytics Omniture Heartbeat AppMeasurement player implmenation
- FEC-3509 - Design OTT Player Skin
- FEC-3733 - Anonymous user
- FEC-2900 - Implement embedly player.js interface for player API against kaltura player
- SUP-4886 - Disabling the Livstream redirect
- SUP-5119 - Playback rate selector issue
- SUP-4976 - changeMedia issue on Android 5.0
- SUP-5142 - VPAID Issues, clickthrough, portrait and playback
- SUP-4014 - Adtag link not working on HTML5 players
- SUP-4904 - Chapters names on menu not so visible on IE9
- SUP-5120 - Playback rate selector starts video from beginning when changing rate for first time
- SUP-5312 - Vast ads are not filling the player area
- SUP-4277 - Mediahuis - Windows Phone 8.1 black screen on playbac
- SUP-5278 - VPAID Overlay dimensions/position issue in full screen
- SUP-5357 - Pause button stop working
- SUP-5349 - Unable to change preferred bitrate in source selector

* Sun Jul 12 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.32.1-1
- Support MSE/EME only on Chrome

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
