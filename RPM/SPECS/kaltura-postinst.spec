%define prefix /opt/kaltura 

Summary: Kaltura Open Source Video Platform 
Name: kaltura-postinst 
Version: 1.0.8
Release: 17 
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.gz
Source1: post_inst_mail.template
Source2: consent_msgs
Source3: sql_updates
URL: http://kaltura.org
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

This package includes post install scripts to be run post RPM install as they require user input.

%prep
%setup -qn postinst

%install
mkdir -p $RPM_BUILD_ROOT/%{prefix}/bin
mkdir -p $RPM_BUILD_ROOT/%{prefix}/app/configurations $RPM_BUILD_ROOT/%{prefix}/app/deployment/updates/scripts
chmod +x *.sh 
mv  *.sh *.rc $RPM_BUILD_ROOT/%{prefix}/bin
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
				mysql kaltura -h $DB1_HOST -u $SUPER_USER -P $DB1_PORT -p$SUPER_USER_PASSWD < $SQL
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

%files
%{prefix}/bin/*
%{prefix}/app/deployment/*
%config %{prefix}/bin/db_actions.rc
%config %{prefix}/app/configurations/*

%changelog
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
