%define prefix /opt/kaltura 
Summary: Kaltura Open Source Video Platform 
Name: kaltura-postinst 
Version: 1.0.28
Release: 18
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.gz
Source1: post_inst_mail.template
Source2: consent_msgs
Source3: sql_updates
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: bc,unzip,redhat-lsb-core

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

This package includes post install scripts to be run post RPM install as they require user input.

%prep
%setup -qn postinst

%install
mkdir -p $RPM_BUILD_ROOT/%{prefix}/bin
mkdir -p $RPM_BUILD_ROOT/%{prefix}/app/configurations $RPM_BUILD_ROOT/%{prefix}/app/deployment/updates/scripts
chmod +x *.sh 
mv  *.sh *.rc *.php *.ini *.xml *.jpg *.srt $RPM_BUILD_ROOT/%{prefix}/bin
cp %{SOURCE1} $RPM_BUILD_ROOT/%{prefix}/app/configurations
cp %{SOURCE2} $RPM_BUILD_ROOT%{prefix}/app/configurations/consent_msgs
cp %{SOURCE3} $RPM_BUILD_ROOT%{prefix}/app/deployment/sql_updates
cp -r patches $RPM_BUILD_ROOT/%{prefix}/app/deployment/updates/scripts
sed -i 's#@APP_DIR@#%{prefix}/app#g' $RPM_BUILD_ROOT/%{prefix}/bin/*rc

%clean
rm -rf %{buildroot}

%post
if [ "$1" = 2 ];then
	if [ -r "%{prefix}/app/configurations/system.ini" -a -r %{prefix}/app/deployment/sql_updates ];then
		. %{prefix}/app/configurations/system.ini
		RC=0
		for SQL in `cat %{prefix}/app/deployment/sql_updates`;do
		# if we have the .done file, then some updates already happened
		# need to check if our current one is in the done list, if so, skip it.
			if [ -r  %{prefix}/app/deployment/sql_updates.done ];then
				if grep -q $SQL %{prefix}/app/deployment/sql_updates.done;then
					continue
				fi
			fi
			if [ -r $SQL ];then
				mysql kaltura -h $DB1_HOST -u $DB1_USER -P $DB1_PORT -p$DB1_PASS < $SQL 2>/dev/null
				RC=$?
			else
				echo "In order to upgrade your DB, please run %{prefix}/bin/kaltura-db-update.sh once the RPMs installation completes."
				RC=1
			fi
		done
		if [ $RC -eq 0 ];then
			cat %{prefix}/app/deployment/sql_updates >> %{prefix}/app/deployment/sql_updates.done
			rm %{prefix}/app/deployment/sql_updates
		fi
	fi
fi
%preun
find %{_sysconfdir}/logrotate.d -type l -name "kaltura_*" -exec rm {} \;

%files
%{prefix}/bin/*
%{prefix}/app/deployment/*
%config %{prefix}/bin/db_actions.rc
%config %{prefix}/app/configurations/*

%changelog
* Thu Oct 1 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.28-18
- http://forum.kaltura.org/t/kaltura-fails-to-install-on-ubuntu-14-04-3-lts/3491/6

* Fri Sep 25 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.28-16
- https://github.com/kaltura/platform-install-packages/issues/60

* Fri Sep 18 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.28-15
- https://github.com/kaltura/platform-install-packages/issues/443

* Tue Sep 15 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.28-12
- replace @APP_REMOTE_ADDR_HEADER_SALT@ token.

* Mon Sep 14 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.28-11
- When the port is 80 or 443, do not concat the port to the service URL.
  This is important when you want to do SSL offloading..
* Mon Aug 10 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.28-7
- https://github.com/kaltura/platform-install-packages/pull/425

* Sun Aug 9 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.28-6
- use lsb_release -c -d to report linux_flavor to analytics.

* Mon Aug 3 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.28-5
- https://github.com/kaltura/platform-install-packages/pull/430

* Fri Jul 31 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.28-3
- Increase waiting period for daemons to be started by monit to 120s.

* Thu Jul 16 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.28-2
- notifications tests: delete() in the end of test.

* Thu Jul 16 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.28-1
- dropfolder test: delete() afterwards.

* Tue Jul 14 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.27-16
- In RHEL/CentOS 7 - memcached is not started and set to init by its RPM postinst script, do it in ours.

* Tue Jul 14 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.27-15
- for RHEL7, package is called nfs-utils not nfs-utils-libs

* Fri Jul 10 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.27-14
- Changed script name to match script naming convention.

* Fri Jul 10 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.27-11
- Added script that clears old dwh logs, runs the logrotate and then all the jobs from /etc/cron.d/kaltura-dwh.. Useful for when debugging analytics.

* Thu Jul 9 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.27-10
- Thumb signature test was only relevant when we only supported RHEL/CentOS 6. Now that we support RHEL7, Debian and Ubuntu of multiple versions, it will fail cause the hash will be different per platform and so - disabling it.

* Wed Jul 8 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.27-3
- Added upload captions test 
- Added search entry test
- Added notification tests

* Fri Jun 19 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.26-5
- use $SUPER_USER when dropping db, do not assume root

* Thu Jun 18 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.26-4
- https://github.com/kaltura/platform-install-packages/issues/413

* Sun Jun 1 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.26-2
- Corrected typo in nginx-config
- Added script for kaltura-play-server

* Thu May 21 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.26-1
- Fix studio sanity on deb
- Redirect errors Can't DROP| already exists| Duplicate column name to /dev/null for db-update.sh since they stem from the fact these update SQLs were already prev. processed and are therefore not actual errors.

* Tue May 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.25-11
- Reinstated clipping checks.

* Mon May 4 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.25-10
- Disable trimming and clipping tests as they stopped working since 10.9.0.

* Mon Apr 13 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.25-3
- Modifications to allow sanity to run on both RPM and deb based systsms.

* Mon Apr 6 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.25-2
- Use example.com for test partner. example.com is ignored by MTAs.

* Fri Apr 3 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.24-12
- Remove logrotate syms during preun.

* Thu Apr 2 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.24-11
- Added script to clean all data from the DWH DBs. Useful for when you want to keep the operational 'kaltura' DB but clear analytics.

* Tue Mar 17 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.24-9
- corrected clipapp sanity check.

* Sun Mar 15 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.24-8
- Symlink Kaltura vhost config to apache conf.d when installing batch.

* Sat Mar 14 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.24-7
- added limit 1 to select conf_file_path from ui_conf where tags like '%kmc_uploadWebCam%' LIMIT 1; 
  reported by Kinglok, Fong - thank you.

* Sat Feb 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.24-6
- instead of chmoding in cache dir just get rid of it.

* Sat Feb 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.24-5
- push WWW_HOST var to ans file.

* Sat Feb 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.24-4
- Added test for clipapp url.

* Wed Feb 18 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.24-1
- Added BPM deploy script.

* Wed Jan 14 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.23-2
- Modifications to support VOD packager.

* Sun Jan 11 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.22-10
- Direct STDERR to /dev/null when rpm -q.

* Fri Jan 9 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.22-9
- Added create and remove flavor tests.

* Sun Jan 4 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.22-4
- Support mariadb in kaltura-mysql-settings.sh
- Remove resriction to MySQL 5.1 since it seems to work fine with it now

* Fri Nov 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.22-1
- Fix for https://github.com/kaltura/platform-install-packages/issues/234

* Tue Nov 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.21-9
- Init BEGINNERS_TUTORIAL_URL, QUICK_START_GUIDE_URL, FORUMS_URLS outside the interactive block as it applies to silent installs too.
 
* Mon Nov 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.21-8
- escape root's MySQL passwd with ".

* Wed Nov 19 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.21-6
- Until they merge: https://github.com/kaltura/server/pull/1880..

* Tue Nov 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.21-5
- Added call to sphinx-schema-upgrade.sh from kaltura-sphinx-config.sh.

* Wed Nov 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.21-3
- Added validation for timezone value.

* Mon Nov 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.21-2
- Added script to handle the event of Sphinx being added a column

* Tue Nov 4 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.21-1
- Installytics moved to MySQL so curl call for reporting changed some
- Added subscribed_for_ce_updates to the report

* Mon Nov 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.20-10
- Try to use dmidecode to generate uniq machine ID, if it exists..

* Thu Oct 30 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.20-9
- Fixes for Analytics.

* Mon Oct 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.20-8
- Added reconversion of entry to sanity.

* Sun Oct 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.20-6
- Call for Marketo takes a few sec to complete - added a message.

* Sun Oct 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.20-5
- Prompt about Community newsletter

* Fri Oct 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.20-4
- Only run studio test if kaltura-html5lib is installed

* Thu Oct 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.20-3
- Redirect ls' STDERR to /dev/null when looking for java
- Added test for studio's index.html to kaltura-sanity.sh

* Sun Oct 19 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.20-2
- Correct /dev/null redirection.

* Thu Oct 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.19-4
- Better distro detection for analytics.

* Mon Oct 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.19-2
- redirect ls STDERR to dev/null
- fix analytics.

* Sun Sep 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.19-1
- We do not want to reload Apache during base because if this is a reconfig, there would already be a symlink under /etc/httpd/conf.d/ pointing to the kaltura apache config, base will replace the actual values with the template and so, Apache will not load.

* Sun Aug 31 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.18-1
- Fix for https://github.com/kaltura/platform-install-packages/issues/215.

* Sun Aug 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.17-16
- Replace new tokens in init_data.

* Wed Aug 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.17-14
- With storage creation script.

* Mon Aug 11 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.17-10
- With thumb testing..

* Mon Aug 11 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.17-5
- Added dropfolder creation test.

* Sun Aug 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.17-4
- Added tests to sanity:
  - clipping
  - trimming
  - mail sending post partner creation

* Tue Aug 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.17-1
- Starting support of alt port for Apache and CDN.

* Tue Jul 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.16-5
- Fixes for making the install work when MySQL is on alt port.

* Thu  Jul 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.16-4
- ls on the KMC dir may fail because this is running on Sphinx which needs no web mount so redirect STDERR to /dev/null

* Mon Jul 2 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.16-3
- KMC SWF tests added.

* Mon Jun 30  2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.16-1
- Added playManifest and download test to san.

* Wed Jun 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.15-4
- Added new token replacement for TEMPLATE_PARTNER_ADMIN_PASSWORD

* Tue Jun 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.15-2
-  -6 partner token replacement.

* Tue Jun 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.15-1
- need to replace WWW_HOST in the DB create scripts too

* Tue Jun 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.14-5
- Fixed streams dir and symlink check.

* Tue Jun 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.14-4
- Reload apache post base config so cache is cleared.

* Tue Jun 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.14-3
- https://github.com/kaltura/platform-install-packages/pull/153

* Mon Jun 2 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.14-2
- Our analytics server moved to a new castle.

* Sun Jun 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.14-1
- Offering 'root' as default does little good if we don't accept it and looping with prompt.

* Thu May 22 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.13-8
- F typo. 
- Added call for contributors banner.

* Wed May 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.13-4
- Added license info to scripts header. thank you David Kohen for pointing this out.

* Thu May 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.13-2
- Following https://github.com/kaltura/platform-install-packages/pull/128.

* Wed May 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.13-1
- Fix for https://github.com/kaltura/platform-install-packages/issues/122

* Mon May 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.12-32
- Fixes https://github.com/kaltura/platform-install-packages/pull/119

* Sun May 11 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.12-31
- Check if NFS volume is already mounted, if not, mount and exit if that fails.

* Sun May 4 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.12-28
- Better output.

* Tue Apr 29 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.12-23
- need unzip for the sanity test.

* Tue Apr 29 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.12-22
- ans file has passwds in it and must be 600.

* Sat Apr 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.12-8
- https://github.com/kaltura/platform-install-packages/issues/99

* Sat Apr 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.12-6
- [master 1112364] no need for these functions to accept machine as param. They check the services locally.

* Sat Apr 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.12-5
- No reason to require root previleges for running the alters. 'kaltura' user is capable of it.

* Sun Apr 20 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.11-18
- Added dwh and delete partner to sanity testing.

* Sat Apr 19 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.11-2
- In kaltura-front-config.sh - first call kaltura-base-config.sh

* Thu Apr 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.11-1
- Bugs->fixes.

* Wed Apr 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.10-8
- Need to respect USER_CONSENT coming from the ans file.

* Tue Apr 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.10-7
- Added bc to deps. Used in kaltura-sanity.sh

* Tue Apr 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.10-2
- Check if kaltura-base is installed before starting config proc.

* Wed Mar 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.9-8
- replace html5_version in base.ini to latest.

* Wed Mar 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.9-7
- The creation of ans file should be called later on.

* Wed Mar 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.9-6
- Script to setup MySQL replication added.

* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.9-2
- To match Core release 9.13.0.

* Sun Mar 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.9-1
- kaltura-sanity.sh's output revised according to Zohar's requests.

* Sat Mar 22 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.8-19
- kaltura-sanity.sh is operational.

* Thu Mar 20 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.8-18
- kaltura-front-config.sh - we can't use rpm -q kaltura-kmc because this node may not be the one where we installed the KMC RPM on, as it resides in the web dir and does not need to be installed on all front nodes.

* Thu Mar 20 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.8-16
- disable ERR trap when checking if kalturadw tables exist.

* Mon Mar 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.8-11
- Colors && shit..

* Mon Mar 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.8-10
- Color corrections
- Do not sed on php INIs where they are not present [DWH, Sphinx].
- Suggest to drop the DB if it exists and db-config is run.

* Mon Mar 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.8-7
- Colorful output to make err detection easy.

* Thu Mar 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.8-3
- Random monit passwd.

* Thu Mar 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.8-2
- Modified message in drop-db.sh

* Thu Mar 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.8-1
- Modified mail template a little.
- Added script to configure NFS client side.

* Tue Mar 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-23
- '"' around CONSENT.

* Wed Mar 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-22
- Base - exit if something failed.

* Wed Mar 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-21
- Fix for https://github.com/kaltura/platform-install-packages/issues/57

* Mon Mar 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-20
- kaltura-db-update.sh by David Bezemer.
- Respect the USER_CONSENT var from ans file for quiet installs.
 
* Sat Mar 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-19
- Write {KEY,CRT}_FILE to system.ini
- Fix consent code flow to work with ans file.

* Fri Feb 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-15
- Fix for https://github.com/kaltura/platform-install-packages/issues/47

* Fri Feb 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-14
- Added explanation on how to increase log level to DEBUG, see:
  https://github.com/kaltura/platform-install-packages/issues/51  

* Wed Feb 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-10
- https://github.com/mobcdi/platform-install-packages/commit/00d06299204b5b3a7314b8e705a75e73ae2de017

* Wed Feb 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-9
- Do not beacon an install in case it is an upgrade.
  For upgrade, we will send the event via the RPM post install as we already have all the info we need and know if the
  user gave consent or not so, the fact the hook cannot get output does not bother us at all.

* Tue Feb 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-8
- Added version and revision info to beacons.

* Wed Feb 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-7
- /app/deployment/sql_updates should be in this package and not in base, since it is being used here.

* Tue Feb 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-2
- typo

* Tue Feb 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.7-1
- Becons modifications.
- User consent msg added.

* Mon Feb 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.6-8
- If this is an upgrade and DB connectivity works - generate UI confs.

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.6-2
- monit's init show failure when attempting to stop a monit that isn't running.
  Direct to /dev/null in that case.

* Sat Feb 22 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.6-1
- Post becon tests.

* Sat Feb 22 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-34
- Becon corrections.

* Fri Feb 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-30
- With becons.

* Thu Feb 20 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-29
- Only add studio.template.ini to CONF_FILES if html5-studio is installed.

* Tue Feb 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-26
- Only do the update if the record is missing.

* Tue Feb 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-22
- https://github.com/kaltura/platform-install-packages/issues/28
 
* Mon Feb 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-20
- Have hostname as default for Red5.

* Sun Feb 16 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-19
- Attempt to correct corrupted UI confs.

* Sun Feb 16 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-18
- Need to restart monit daemon after each daemon config, can't do it in all because not every inst. is all in 1.

* Sun Feb 16 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-14
- chown and chmod monit.conf to be root.root 600.

* Sat Feb 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-13
- Monit fixes.

* Fri Feb 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-11
- chown apache for the streams dir.

* Fri Feb 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-8
- Replace localhost with actual server name in oflaDemo/index.html
* Fri Feb 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-6
- Some fixes for Red5.

* Fri Feb 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-5
- Added Red5 config script.

* Thu Feb 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-4
- Symlink to red5 streaming dir.

* Thu Feb 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-3
- Prompt for RED5 host.

* Thu Feb 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.5-2
- Replace toks in studio.ini.

* Fri Feb 7 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.4-11
- Fixes https://github.com/kaltura/platform-install-packages/issues/21
- Add logging to file during DWH setup.
- Batch: only configure Kaltura vhost in the event the service URL is local.

* Wed Feb 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.4-10
- Correctly replace timezone directive
- Easier copy paste output for MySQL directives

* Wed Feb 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.4-8
- typo fix.

* Wed Feb 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.4-7
- Passwd confirmation prompt
- Changed string 'host' to 'hostname'

* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.4-3
- Exit configs if the relevant RPM package isn't installed.

* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.3-11
Replace tokens in %%{prefix}/app/tests/monitoring/config.template.ini

* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.3-10
- Don't attempt to replace tokens for DWH if DWH isn't installed on node.

* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.3-9
- Fixes for cluster install.

* Sun Feb 2 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.3-7
- Auto detect TZ.

* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.3-5
- Phrasing correction.

* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.3-4
- Minor corrections to db-config.

* Wed Jan 29 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-8
- Modified post install mail template.

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-7
- With post install mail template.
* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-8
- Now actually USE the templ to send it out.

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-7
- With post install mail template.

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-6
- Proper Analytics population msg.
- Change all server prompt defaults to 127.0.0.1.
- Changed inst complete msg.

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-5
- bash -x on drop-db.sh

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-3
- Removed debug from front.
- Added DWH config to config-all.sh

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-1
- New minor release.

* Sat Jan 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-38
- Unsubscribe mail token now replaced
- Setting Apache on HTTP works
- Added port selection in front config
- Added export DB script
- Added %%prefix/bin/kaltura-drop-db.sh
- Added %%prefix/kaltura-mysql-settings.sh

* Sun Jan 19 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-15
- Version bounce. 

* Thu Jan 16 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-13
- Only run base-config if there's no lock indicating it already ran.

* Tue Jan 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-12
- Additions to both base and db config scripts.

* Tue Jan 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-11
- Added DB config script and RC file.

* Thu Jan 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-4
- Bounce.

* Thu Jan 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-2
- Updated base config script.

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-1
- initial package. 
