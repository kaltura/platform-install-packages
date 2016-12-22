%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define apache_user	apache
%define apache_group	apache
%define prefix /opt/kaltura
%define confdir %{prefix}/app/configurations
%define logdir %{prefix}/log
%define webdir %{prefix}/web
%define codename Lynx 

Summary: Kaltura Open Source Video Platform 
Name: kaltura-base
Version: 12.8.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/server/archive/%{codename}-%{version}.zip 
Source4: emails_en.template.ini
Source10: entry_and_uiconf_templates.tar.gz
# fixes https://github.com/kaltura/platform-install-packages/issues/37
Source11: clear_cache.sh
# monit templates
Source13: sphinx.template.rc 
Source14: httpd.template.rc 
Source15: batch.template.rc 
Source16: memcached.template.rc 
Source17: navigation.xml 
Source18: monit.phtml 
Source19: IndexController.php
Source20: sphinx.populate.template.rc
Source25: kaltura_populate.template
Source26: kaltura_batch.template
#Source28: embedIframeJsAction.class.php
Source32: KDLOperatorFfmpeg1_1_1.php
#Source33: kuserPeer.php
Source34: clients-generator-%{codename}-%{version}.zip
URL: https://github.com/kaltura/server/tree/%{codename}-%{version}
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: rsync,mysql,kaltura-monit,kaltura-postinst,cronie, php-cli, php-xml, php-curl, php-mysql, php-gd, php-gmp, php-ldap, php-mbstring, php-process, ntp, mailx

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

This is the base package, needed for any Kaltura server role.

%prep
%setup -qn server-%{codename}-%{version}
unzip -q -o %{SOURCE34}


%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/app
mkdir -p $RPM_BUILD_ROOT%{prefix}/log
mkdir -p $RPM_BUILD_ROOT%{prefix}/var/run
mkdir -p $RPM_BUILD_ROOT%{prefix}/tmp
mkdir -p $RPM_BUILD_ROOT%{prefix}/web
mv clients-generator-%{codename}-%{version} $RPM_BUILD_ROOT%{prefix}/clients-generator 
for i in alpha api_v3 batch generator infra scripts sphinx testme thumb deploy testmeDoc html5;do
	mkdir -p $RPM_BUILD_ROOT%{prefix}/app/cache/$i
done

mkdir -p $RPM_BUILD_ROOT%{prefix}/bin
mkdir -p $RPM_BUILD_ROOT%{prefix}/lib
mkdir -p $RPM_BUILD_ROOT%{prefix}/include
mkdir -p $RPM_BUILD_ROOT%{prefix}/share

mkdir -p $RPM_BUILD_ROOT%{prefix}/tmp/convert
mkdir -p $RPM_BUILD_ROOT%{prefix}/tmp/thumb/

mkdir -p $RPM_BUILD_ROOT%{prefix}/web/tmp
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/tmp/imports
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/tmp/convert
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/tmp/thumb
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/tmp/xml
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/dropfolders/monitor
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/control
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content/cacheswf
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content/uploads
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content/entry
mkdir -p $RPM_BUILD_ROOT%{prefix}web/content//metadata
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content/batchfiles
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content/templates



mkdir -p $RPM_BUILD_ROOT/etc/kaltura.d
# align faulty permissions.
for i in "*.xml" "*.template" "*.ttf" "*.xsl" "*.xsd" "*.yml" "*.smil" "*.srt" "*.sql" "*.orig" "*.patch" "*.po" "*.pdf" "*.otf" "*.txt" "*.php" "*.phtml" "*.
project" "*.png" "*.properties" "*.sample" "*.swf" "*.sf" "*.swz" "*.uad" "*.prefs" "*.psd" "*.rvmrc" "*.sln" "*.ini" "*.log" ;do
	find . -iname "$i" -exec chmod 644 {} \;
done

for i in admin_console alpha api_v3 batch configurations deployment generator infra plugins start tests ui_infra var_console vendor VERSION.txt  license.txt release-notes.md;do 
	mv  %{_builddir}/server-%{codename}-%{version}/$i $RPM_BUILD_ROOT%{prefix}/app
done
find  $RPM_BUILD_ROOT%{prefix}/app -name "*.sh" -type f -exec chmod +x {} \;


sed -i 's@^IsmIndex@;IsmIndex@g' $RPM_BUILD_ROOT%{prefix}/app/configurations/plugins.template.ini
sed -i "s#^;kmc_version = @KMC_VERSION@#kmc_version = %{_kmc_version}#g" $RPM_BUILD_ROOT%{prefix}/app/configurations/local.template.ini
sed -i 's@^otp_required_partners\[\]@;otp_required_partners\[\]@g' $RPM_BUILD_ROOT%{prefix}/app/configurations/local.template.ini
sed -i "s@^partner_otp_internal_ips@;partner_otp_internal_ips@g" $RPM_BUILD_ROOT%{prefix}/app/configurations/local.template.ini
sed -i "s#^;html5_version = @HTML5LIB_VERSION@#html5_version = %{html5_version}#g" $RPM_BUILD_ROOT%{prefix}/app/configurations/local.template.ini
sed -i "s#^;kmc_login_version = @KMC_LOGIN_VERSION@#kmc_login_version = %{kmc_login_version}#g" $RPM_BUILD_ROOT%{prefix}/app/configurations/local.template.ini
sed -i "s@clipapp_version = @CLIPPAPP_VERSION@#clipapp_version = %{clipapp_version}#g" $RPM_BUILD_ROOT%{prefix}/app/configurations/local.template.ini
sed -i "s#^clipapp_version =.*#clipapp_version = %{clipapp_version}#g" $RPM_BUILD_ROOT%{prefix}/app/configurations/base.ini
sed -i "s#^;kdp3_wrapper_version = @KDP3_WRAPPER_VERSION@#kdp3_wrapper_version = %{kdp3_wrapper_version}#g" $RPM_BUILD_ROOT%{prefix}/app/configurations/local.template.ini
sed -i 's@^writers.\(.*\).filters.priority.priority\s*=\s*7@writers.\1.filters.priority.priority=4@g' $RPM_BUILD_ROOT%{prefix}/app/configurations/logger.template.ini 
# our Pentaho is correctly installed under its own dir and not %prefix/bin which is the known default so, adding -k path to kitchen.sh
sed -i 's#\(@DWH_DIR@\)$#\1 -k %{prefix}/pentaho/pdi/kitchen.sh#g' $RPM_BUILD_ROOT%{prefix}/app/configurations/cron/dwh.template
#rm $RPM_BUILD_ROOT%{prefix}/app/generator/sources/android/DemoApplication/libs/libWVphoneAPI.so
rm $RPM_BUILD_ROOT%{prefix}/clients-generator/sources/android/DemoApplication/libs/libWVphoneAPI.so
rm $RPM_BUILD_ROOT%{prefix}/app/configurations/.project
# we have our own that is provided with the kaltura-monit package
rm $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.template.conf
rm $RPM_BUILD_ROOT%{prefix}/app/deployment/base/scripts/init_content/04.dropFolder.-4.template.xml

# we bring our own for kaltura-front and kaltura-batch.
cp %{SOURCE4} $RPM_BUILD_ROOT%{prefix}/app/batch/batches/Mailer/emails_en.template.ini
cp %{SOURCE11} $RPM_BUILD_ROOT%{prefix}/app/alpha/crond/kaltura/clear_cache.sh
mkdir -p $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail
cp %{SOURCE13} $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/
cp %{SOURCE20} $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/
cp %{SOURCE14} $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/
cp %{SOURCE15} $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/
cp %{SOURCE16} $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/
#cp $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.d/*.template.rc $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/
#cp $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.d/memcached.template.rc $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/memcached.rc
#cp $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.d/mysqld.template.rc $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/mysqld.rc
#cp $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.d/mariadb.template.rc $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/mariadb.rc
#cp $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.d/percona.template.rc $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/percona.rc
rm $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.d/*template*
cp %{SOURCE25} $RPM_BUILD_ROOT%{prefix}/app/configurations/logrotate/
cp %{SOURCE26} $RPM_BUILD_ROOT%{prefix}/app/configurations/logrotate/


# David Bezemer's Admin console and monit patches:
cp %{SOURCE17} $RPM_BUILD_ROOT%{prefix}/app/admin_console/configs/navigation.xml
cp %{SOURCE18} $RPM_BUILD_ROOT%{prefix}/app/admin_console/views/scripts/index/monit.phtml
cp %{SOURCE19} $RPM_BUILD_ROOT%{prefix}/app/admin_console/controllers/IndexController.php
# patch for auto embed to work, should be dropped when core merge.
#cp %{SOURCE28} $RPM_BUILD_ROOT%{prefix}/app/alpha/apps/kaltura/modules/extwidget/actions/embedIframeJsAction.class.php
# we bring a1nother in kaltura-batch
rm $RPM_BUILD_ROOT%{prefix}/app/configurations/batch/batch.ini.template
cp %{SOURCE32} $RPM_BUILD_ROOT%{prefix}/app/infra/cdl/kdl/KDLOperatorFfmpeg1_1_1.php
#cp %{SOURCE33} $RPM_BUILD_ROOT%{prefix}/app/alpha/lib/model/kuserPeer.php

mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content
tar zxf %{SOURCE10} -C $RPM_BUILD_ROOT%{prefix}/web/content

%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/kaltura_base.sh << EOF
PATH=\$PATH:%{prefix}/bin
export PATH
alias allkaltlog='grep --color "ERR:\|PHP \|Stack trace:\|CRIT\|\[error\]" %{prefix}/log/*.log %{prefix}/log/batch/*.log'
alias kaltlog='tail -f %{prefix}/log/*.log %{prefix}/log/batch/*.log | grep -A 1 -B 1 --color "ERR:\|PHP \|Stack trace:\|CRIT\|\[error\]"'
if [ -r /etc/kaltura.d/system.ini ];then
	. /etc/kaltura.d/system.ini
fi
EOF

%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/kaltura_base.conf << EOF
%{prefix}/lib

EOF

%clean
rm -rf %{buildroot}

%pre
if [ "$1" = 2 ];then
	if rpm -q httpd >> /dev/null;then
		service kaltura-monit stop
		if service httpd status;then
			service httpd stop
		fi
	fi
	rm -rf %{prefix}/app/cache/*
fi
# maybe one day we will support SELinux in which case this can be ommitted.
if which getenforce >> /dev/null 2>&1; then
	
	if [ `getenforce` = 'Enforcing' ];then
		echo "You have SELinux enabled, please change to permissive mode with:
# setenforce permissive
and then edit /etc/selinux/config to make the change permanent."
		exit 1;
	fi
fi
# create user/group, and update permissions
getent group %{kaltura_group} >/dev/null || groupadd -r %{kaltura_group} -g7373 2>/dev/null
getent passwd %{kaltura_user} >/dev/null || useradd -m -r -u7373 -d %{prefix} -s /bin/bash -c "Kaltura server" -g %{kaltura_group} %{kaltura_user} 2>/dev/null

getent group %{apache_user} >/dev/null || groupadd -g 48 -r %{apache_group}
getent passwd %{apache_user} >/dev/null || \
  useradd -r -u 48 -g %{apache_group} -s /sbin/nologin \
    -d /var/www -c "Apache" %{apache_user}
usermod -a -G %{kaltura_group} %{apache_user}

usermod -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true


%post

ln -sf %{prefix}/app/configurations/system.ini /etc/kaltura.d/system.ini
ln -sf %{prefix}/app/api_v3/web %{prefix}/app/alpha/web/api_v3
chown apache.kaltura %{prefix}/web/content/entry %{prefix}/web/content/uploads/  %{prefix}/web/tmp/
chmod 775 %{prefix}/web/content/entry %{prefix}/web/content/uploads  %{prefix}/web/tmp
service ntpd start
if [ "$1" = 2 ];then
	if [ -r "%{prefix}/app/configurations/local.ini" -a -r "%{prefix}/app/configurations/base.ini" ];then
		sed -i "s@^\(kaltura_version\).*@\1 = %{version}@g" %{prefix}/app/configurations/local.ini
		echo "Regenarating client libs.. this will take up to 2 minutes to complete."
		if service httpd status;then
			service httpd stop
		fi
		# this is read by kaltura-sphinx-schema-update.sh to determine rather or not to run
		touch %{prefix}/app/configurations/sphinx_schema_update
		find %{prefix}/app/cache/ -type f -exec rm {} \;
		rm -f %{prefix}/app/base-config-generator.lock
		php %{prefix}/app/generator/generate.php
		php %{prefix}/app/deployment/base/scripts/installPlugins.php
		php %{prefix}/app/deployment/base/scripts/populateSphinxMetadata.php
		find %{prefix}/app/cache/ %{prefix}/log %{prefix}/var/run -type d -exec chmod 775 {} \;
		find %{prefix}/log -type f -exec chmod 664 {} \;
		chown -R %{kaltura_user}.%{apache_user} %{prefix}/app/cache/ %{prefix}/log %{prefix}/var/run
		chmod 775 %{prefix}/web/content

		service kaltura-monit start
		if rpm -q httpd >> /dev/null;then
			if ! service httpd status;then
				service httpd start
			fi
		fi

		# we now need CREATE and DROP priv for 'kaltura' on kaltura.*
		if [ -r /etc/kaltura.d/system.ini ];then
			. /etc/kaltura.d/system.ini
			# disbale Default_Akamai_HLS_direct since we want the nginx vod-module profile to be used [ID 1001, system_name: Kaltura HLS segmentation]
			echo "update delivery_profile set is_default=0 where id=1 and system_name='Default_Akamai_HLS_direct';"|mysql -h$DB1_HOST -u $DB1_USER -p$DB1_PASS -P$DB1_PORT $DB1_NAME
			echo "GRANT INSERT,UPDATE,DELETE,SELECT,ALTER,DROP,CREATE ON kaltura.* TO '$DB_USER'@'%';FLUSH PRIVILEGES;"|mysql -h$DB1_HOST -u $SUPER_USER -p$SUPER_USER_PASSWD -P$DB1_PORT
		fi
		php %{prefix}/app/deployment/updates/update.php -i -d >> /opt/kaltura/log/kalt_up.log 2>&1
		php %{prefix}/app/deployment/updates/update.php -i -s >> /opt/kaltura/log/kalt_up.log 2>&1
		php %{prefix}/app/deployment/base/scripts/installPlugins.php >> /opt/kaltura/log/kalt_up.log 2>&1

	fi

fi


%preun
if [ "$1" = 0 ] ; then
	rm -f %{_sysconfdir}/kaltura.d/system.ini
	rm -f %{prefix}/app/alpha/web/api_v3
	rm -f %{_sysconfdir}/logrotate.d/kaltura_base
	# get rid of stray symlinks.
	find %{_sysconfdir}/httpd/conf.d/ -type l -name "*kaltura*" -exec rm {} \;
	find %{prefix}/app -maxdepth 1 -name "*.lock" -exec rm {} \;
fi

%postun

%files
%{prefix}/app/admin_console
%{prefix}/app/var_console
%{prefix}/app/alpha
%{prefix}/app/api_v3
%{prefix}/app/batch
%{prefix}/app/deployment
%{prefix}/app/generator
%{prefix}/app/infra
%{prefix}/app/ui_infra
%{prefix}/app/plugins
%{prefix}/app/start
%{prefix}/app/vendor
%{prefix}/app/tests
%{prefix}/app/cache
%{prefix}/clients-generator

%config %{prefix}/app/configurations/*
%config %{prefix}/clients-generator/config/*
%config %{_sysconfdir}/profile.d/kaltura_base.sh
%config %{_sysconfdir}/ld.so.conf.d/kaltura_base.conf


%dir /etc/kaltura.d
%defattr(-, %{kaltura_user}, %{apache_group} , 0775)
%dir %{prefix}/log
%dir %{prefix}/var/run
%dir %{prefix}/tmp
%dir %{prefix}/app/cache
%{prefix}/web/*
%defattr(-, %{kaltura_user}, %{kaltura_group} , 0755)
%dir %{prefix}
%dir %{prefix}/web/control
%dir %{prefix}/web/dropfolders
%defattr(-, root,root, 0755)
%dir %{prefix}/app/configurations/monit/monit.d
%dir %{prefix}/bin
%dir %{prefix}/lib
%dir %{prefix}/include
%dir %{prefix}/share
%doc %{prefix}/app/release-notes.md
%doc %{prefix}/app/license.txt
%doc %{prefix}/app/VERSION.txt

%changelog
* Thu Dec 22 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.8.0-1
- Ver Bounce to 12.8.0

* Thu Dec 22 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.8.0-1
- Ver Bounce to 12.8.0

* Mon Dec 19 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.7.0-6
- SUP-9163 - first status of a user
- SUP-9535 - iTunes Syndication feed not updating explicit tag in channel
- SUP-9785 - Youtube Distribution fails for several entries
- SUP-9799 - Duplicated Users Per Same PID
- PLAT-6516 - Delivery Profile selection order not working properly
- PLAT-6150 - Typo in HTTP notification name related to Attachments
- PLAT-5707 - optimize the thumbnail grabbing
- PLAT-5801 - Design batch optimiztion
- PLAT-6478 - Deployment of new FFMPEG 3.2
- PLAT-6429 - Suggestion: "re-register authentication" button in Youtube API distribution profile settings
- PLAT-6448 - hbbtv - support set-top boxes
- PLAT-6461 - new player initialization - create play manifest URL

* Tue Dec 6 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.7.0-1
- Ver Bounce to 12.7.0

* Tue Dec 6 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.6.0-6
- SUP-9130 - Cannot download media via KMS
- SUP-9437 - WN - 414 Request-URI Too Large errors on player version 2.48.1
- PLAT-6415 - Timeout when generating 'Business-Process Cases' table in admin console
- PLAT-5783 - Template Entry Overrides Irrelevant Field if New Entry Type is External Media
- PLAT-6419 - Recscheduling - Publish - VOD Entry is not published
- PLAT-6428 - Recscheduling - Recurrence - Weekly series missing two last events (specific case)

* Thu Nov 24 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.6.0-1
- Ver Bounce to 12.6.0

* Tue Nov 22 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.5.0-4
- PLAT-6348 - Add ReplacedEntryId Xsl variable
- SUP-8727 - Deleting CaptureSpace Quiz entry with presentation removes presentation from original entry
- SUP-9501 - Query - in the KMC - Entitlements Settings are empty
- SUP-9451 - Long Conversion Duration for Clipped/trimmed Content - 12H-18H
- PLAT-5983 - Sphinx improvement - add partnerId to privacy_by_contexts
- PLAT-6338 - Multi-Audio: audioLanguage - add label tag to manifest - HLS 
- PLAT-6412 - add KalturaBaseEntryBaseFilter userIdNotIn field

* Wed Nov 9 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.5.0-1
- Ver Bounce to 12.5.0

* Tue Nov 8 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.4.0-13
- Fix Sphinx config https://github.com/kaltura/server/pull/4869/files

* Mon Nov 7 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.4.0-12
- PLAT-6135 - Get end date of last event of a series
- PLAT-6164 - events orderby name is missing
- PLAT-6215 - 2 factor authentication feature
- SUP-9163 - first status of a user
- SUP-9229 - API Error metadata.list
- SUP-9337 - Captions on iPhone not displaying since KS is missing the 'disableentitlementforentry' priviliedge
- PLAT-6197 - List response filter does not return new resources added after creation
- PLAT-6198 - Recscheduling- Recurrence event - time of day is taken from current system time
- PLAT-6218 - Change single event to recurring returns wrong event time.
- PLAT-6255 - edit the resource of an occurrence
- PLAT-6279 - Bulk Upload XML replacement deleted entry's original thumbnails
- PLAT-6268 - Weekly recurrence calculation
- PLAT-6287 - Recurrence date is 31
- PLAT-6305 - exporting schdule events in ICAL format results in incorrect dates

* Mon Oct 10 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.4.0-1
- Ver Bounce to 12.4.0

* Mon Oct 10 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.3.0-7
- PLAT-6132 - Display cross day events
- PLAT-6135 - Get end date of last event of a series
- PLAT-6127 - Add "EXT-X-SESSION-KEY" tag to master manifest for offline FairPlay
- PLAT-5983 - Sphinx improvement - add partnerId to privacy_by_contexts 
- PLAT-5485 - The max duration of an event should be 24 hours
- SUP-7180 - API call - emailRecipients field not working
- SUP-9173 - Server side notifications not working since Sep 2nd - notification ID 7721
- PLAT-5774 - iCal with recurring events ingestion issues
- PLAT-6083 - Response profile returns wrong results
- PLAT-6124 - can't update recurrence of past recurring event
- PLAT-6123 - Can't update series recurrence from until to count or the either way around
- PLAT-5613 - Possible to create duplicate scheduleEventResource
- PLAT-5513 - Possible to set non-existing resource as parent
- PLAT-6186 - Push notifications code is not compatible with Push server V2

* Wed Oct 6 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.3.0-5
- disbale Default_Akamai_HLS_direct since we want the nginx vod-module profile to be used [ID 1001, system_name: Kaltura HLS segmentation]

* Tue Sep 27 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.3.0-1
- Ver Bounce to 12.3.0

* Fri Sep 23 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.2.0-5
- PLAT-5105 - playManifest refactoring for live - delivery profile
- PLAT-5916 - Enhance Access Control Creation script for uDRM
- PLAT-5962 - Support Dash packaging for Firefox standard
- SUP-9003 - The property "accessControlId" is updatable with admin session only
- PLAT-5983 - Sphinx improvement - add partnerId to privacy_by_contexts
- PLAT-5963 - Add makeHidden property to Kaltura_Client_Type_LiveEntryRecordingOptions
- PLAT-5964 - createRecordedEntry method should set display_in_search to -1 if makeHidden is true
- PLAT-5965 - expose entry's display_in_search property in api v3 
- PLAT-5966 - In baseEntry.list (or any derived service) - when listing with IdIn, entries with display_in_search = -1 should be returned
- PLAT-6007 - When picture is not available mediaprep failed the entry
- PLAT-6027 - Enable filtering based on resource ID or parent resource ID
- PLAT-6061 - When picture is not available mediaprep failed to populate metadata
- PLAT-5732 - copy annotation cue points from live to VOD
- PLAT-6047 - yahoo syndication error

* Tue Sep 13 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.2.0-1
- Ver Bounce to 12.2.0

* Mon Sep 12 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.1.0-8
- PLAT-5105 - playManifest refactoring for live - delivery profile
- PLAT-5778 - On playManifest, When Captions are available add them automatically in the packager request
- PLAT-6024 - Live Delivery profile - enable overiding live delivery profiles per partner similar to how we work with VOD
- PLAT-5907 - Add live delivery profile configuration in admin console partner configure page
- SUP-8321 - Trimming VOD of a live entry results in two sources
- SUP-8905 - Cross Kaltura distribution failing intermittently 
- SUP-8016 - replacing media to a VOD entry results with adding instead of replacing

* Mon Aug 29 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.1.0-1
- Ver Bounce to 12.1.0

* Sun Aug 28 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.0.0-9
- PLAT-5747 - Recurrences aren't created from recurring event 
- SUP-8866 - YouTube Distributor 

* Mon Aug 15 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.0.0-1
- Ver Bounce to 12.0.0

* Fri Aug 12 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.21.0-6
- SUP-8019 - caption URL with 404 error gets set as the caption URL for the entry using bulk
- SUP-8470 - Thumbnail Preview Displayed Direction 
- SUP-4381 - Akamai live stream - deletion process inquiry
- PLAT-5797 - Distribution is happening before entry is ready
- PLAT-5742 - Player warm load gets all cue points with no filter so big polls will "kill" the player 
- PLAT-5878 - scheduleEventResource set on recurring event isn't copied to child recurrences

* Thu Aug 4 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.21.0-1
- Ver Bounce to 11.21.0

* Tue Aug 2 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.20.0-8
- SUP-7827 - Access control is not being set by default
- SUP-8669 - Possible Sphynx issue- When using guest KS, restricted entry is not returned when doing baseEntry->get (expected) but DOES return when baseEntry->List (not expected)

* Tue Jul 19 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.20.0-1
- Ver Bounce to 11.20.0

* Tue Jul 19 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.19.0-4
- SUP-8470 - Thumbnail Preview Displayed Direction
- SUP-7683 - API calls failing (Limited to metadata->update)
- PLAT-5725 - Add user-role CAPTURE_DEVICE_ROLE to partner 0
- PLAT-5326 - As a Kaltura platform developer, I'd like to set an entry template on an event

* Tue Jul 12 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.19.0-1
- Ver Bounce to 11.19.0

* Tue Jul 5 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.18.0-7
- PLAT-5390 - syndication xml format
- TOG-369 - Source COPY flavor fails for MPEG-TS files 
- PLAT-5519 - Bulk upload and drop folder ingestion doesn't work
- PLAT-5529 - Can not do bulk actions on resource object

* Sat Jun 25 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.18.0-1
- Ver Bounce to 11.18.0

* Tue Jun 21 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.17.0-8
- PLAT-5484 - As a Kaltura platform developer, I'd like to filter events by linked resource system name
- PLAT-5488 - As a scheduling admin, I'd like to filter events based on the entry template categories tied to the event
- PLAT-5544 - recorded is not exported to remote storage when remote storage has rules
- PLAT-5295 - Live/DVR & Play manifest use register to caluclate playmanifest response
- PLAT-5441 - Add ability to set language on flavor asset object 
- PLAT-5521 - Multi audio support - create infra language manager
- PLAT-5545 - retrieve event-resource objects using responseProfile when listing events
- PLAT-5604 - active Html purifier
- SUP-6788 - Api Error/Access denied in Blackboard
- SUP-8220 - Live stream report
- SUP-8208 - Email notifications sends temporary entry ID when replacing media
- PLAT-5443 - MultiAudioTracks: Video with multiple audio tracks is not working with subtitles
- PLAT-5580 - Live Refactoring -Merging PlayManifest with partner that configure "force Proxy" enable
- PLAT-5519 - Bulk upload and drop folder ingestion doesn't work
- PLAT-4661 - When changing a user's ID - category_kuser records (and maybe others) go out of sync
- PLAT-5120 - When stream is inactive chunklist is still returned instead of 404

* Tue Jun 7 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.17.0-1
- Ver Bounce to 11.17.0

* Fri Jun 3 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.16.0-8
- PLAT-4620 - Support delete on MediaPrep
- PLAT-5408 - VNPT tokenizer
- PLAT-5369 - Change default pre fetch time to be a configurable value
- PLAT-4961 - Support passthrough as part of Slating Epic
- PLAT-4962 - Support return to defined entry as part of Slating development
- PLAT-5295 - Live/DVR & Play manifest use register to caluclate playmanifest response
- PLAT-5357 - Change RTMP url to contain all information on DNS
- SUP-8280 - YouTube API - Distribution error due to duplicate distribute 
- SUP-7828 - Can't distribute when description use HTML tags 
- PLAT-5543 - Searching codeCue points with metadatSearch condition is not working
- PLAT-5264 - ADVs are not played(SyntaxError: Unexpected token @).


* Tue May 24 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.16.0-1
- Ver Bounce to 11.16.0

* Mon May 9 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.15.0-1
- Ver Bounce to 11.15.0

* Sun May 8 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.13.0-8
- PLAT-5348 - Add support for prepositioning when running access control even when using admin KS
- PLAT-5350 - Failed to play smooth stream on the fly flavor due to transcoding issue
- PLAT-5354 - bug when changing user roles via admin console (and api)
- PLAT-5387 - Append to recorded entry does not work properly
- PLAT-5400 - Add support for playlist paging over 200 entries limit
- PLAT-5404 - FSM change status from suspend to play, although entry is not live
- PLAT-3023 - captions does not update Youtube API distribution

* Mon Apr 25 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.14.0-1
- Ver Bounce to 11.14.0

* Mon Apr 25 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.13.0-6
- PLAT-4961 - Support passthrough as part of Slating Epic
- PLAT-4962 - Support return to defined entry as part of Slating development
- PLAT-5040 - LiveProxy call new API
- WEBC-682 - As a producer I'd like to configure my player with a default view

* Tue Apr 12 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.13.0-1
- Ver Bounce to 11.13.0

* Sun Apr 10 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.12.0-6
- SUP-7496 - Syndicated Feed Player Problem 
- PLAT-3872 - Internal Database Error returns when trying to create a userEntry given a non-existing entry ID
- PLAT-5186 - Multi Audio tracks: Playmanifest is empty instead of showing the audio sources

* Mon Mar 28 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.12.0-1
- Ver Bounce to 11.12.0

* Sun Mar 27 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.11.0-8
- SUP-5851 - Categories/Media gallery locked 
- SUP-7437 - API Errors When Pulling Custom Reports
- PLAT-3842 - Two userEntry objects can be created for the same user and entry
- PLAT-5222 - Can't list by AUTOMATIC type 
- PLAT-5197 - The Duration of the DVR windows Don't match the parameters of Entry

* Tue Mar 15 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.11.0-1
- Ver Bounce to 11.11.0

* Fri Mar 11 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.10.0-8
- PLAT-5056 - Enable content Pre-positioning on KES - only download
- PLAT-5091 - Expose Exception throwing in KalturaClient so it can be overridden by implementors
- SUP-6103 - Chapters module embed code not working properly
- PLAT-4082 - Distribution profile fail (YouTube)


* Tue Mar 1 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.10.0-1
- Ver Bounce to 11.10.0

* Mon Feb 29 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.9.0-12
- SUP-6997 - Server returning all stream information when loading the player
- SUP-7185 - Live stream Passthrough ingest is missing
- SUP-7236 - Slow transcoding
- SUP-7267 - Disney - Bulk ingestion intermittently fails to create certain flavors
- PLAT-4714 - Sometimes there is more than one scheduler running on a batch machine
- PLAT-5007 - MAC - Safari:File is not download when pressing on "Export to CSV"
- PLAT-5097 - "Flavor Asset Status Changed" - http event notification template
- PLAT-5103 - can not create drm profile from api
- PLAT-5122 - bad sync between DCs on specific conditions
- PLAT-5126 - KalturaCaptionAssetItemFilter returns KalturaCaptionAsset
- FEC-4958 - Multi Audio tracks: Playmanifest is empty instead of showing the audio sources

* Mon Feb 15 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.9.0-1
- Ver Bounce to 11.9.0

* Sun Feb 14 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.8.0-11
- SUP-7174 - iOS | Widevine Classic | OVP | uDRM | Licence duration error - app playback fails after approximately 10 min. 
- SUP-6997 - Server returning all stream information when loading the player
- SUP-7144 - Image downloaded in jpg format when was uploaded by bulk upload
- PLAT-5042 - Remove user_videos permission from Facebook connector
- PLAT-5045 - Recording fails when user stops few seconds after 15 minutes alignment (15:04,30:02 for example )
- PLAT-4839 - Kaltura's webex account "kalturawebexhost" records meetings in *.MP4 instead of *.arf
- PLAT-4924 - Facebook distribution - missing functionality - Tags
- PLAT-4925 - Facebook distribution - missing functionality - Place
- PLAT-4945 - Facebook distribution - update action missing on Custom Metadata Action
- PLAT-4992 - Facebook distribution - real user cannot connect to Facebook
- PLAT-5004 - In-Video Quizzes: Download PDF is limited to 13 questions
- PLAT-5024 - QuizUserEntry - score should not be int
- PLAT-5025 - Facebook distribution - TargetingCities\Regions failed
- PLAT-4778 - UDRM - OTT BackEnd Entitlement response parsing error
- PLAT-4020 - Media Server package is broken
- PLAT-4714 - Sometimes there is more than one scheduler running on a batch machine

* Mon Feb 1 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.8.0-1
- Ver Bounce to 11.8.0

* Sun Jan 31 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.7.0-9
- PLAT-3593 - DVR refactoring
- PLAT-3270 - Facebook distribution connector
- SUP-7095 - Lakana - Sudden appearance of 'Save Original Source' flavors
- SUP-6618 - Duplicate users created in the backend
- PLAT-4878 - eCDN|KES|Failover|Need ability to handle situation when parent KES is down
- PLAT-4937 - eCDN|There is no verification of EdgeServerType (KES or KSS) on registering
- PLAT-4943 - facebook distribution - update title failed
- PLAT-4189 - In Video Quizzes: copy cue points of chapter-based quiz
- PLAT-4870 - Playlists (Rule Based) - Support Relative Dates

* Mon Jan 18 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.7.0-1
- Ver Bounce to 11.7.0

* Sun Jan 17 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.6.0-13
- PLAT-2443 - eCDN: cache Webcast's thumbAssets with KES
- PLAT-4828 - eCDN: AccessControlProfile rules are limited (50)
- PLAT-4433 - Facebook authentication for Distribution Connector
- PLAT-4434 - Facebook Distribution Configuration
- PLAT-4435 - Distribute content metadata to Facebook
- PLAT-4436 - Video distribution to Facebook
- PLAT-4438 - Distribution of thumbnails to Facebook
- PLAT-4613 - Sometimes, ADV is not played, due to delay between live flavors(also occurs on WN entry).
- PLAT-4940 - ADV is not played after restart FMLE/Wowza over time.
- PLAT-4960 - Multiple stream watchers are started for the same rendition

* Fri Jan 8 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.6.0-5
- Ridiculously enough, the php RPM is compiled with posix as shared and you need to install php-process[!] to get it.
  We want it so we can do posix_getuid() and get the proc's UID. Too much to ask?

* Mon Jan 4 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.6.0-1
- Ver Bounce to 11.6.0

* Sun Jan 3 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.5.0-9
- PLAT-4780 - Support generating packeger url format for external remote storage as well 
- PLAT-4776 - eCDN: SaaS KES Failover support
- PLAT-4433 - Facebook authentication for Distribution Connector
- PLAT-4434 - Facebook Distribution Configuration
- PLAT-4435 - Distribute content metadata to Facebook
- PLAT-4436 - Video distribution to Facebook
- PLAT-4438 - Distribution of thumbnails to Facebook
- PLAT-4862 - Optionally preserve original source when custom intermediate-source is used
- PLAT-2502 - Ad Stitching: log all ad calls & ad beacons; create sample live event ad event audit
- SUP-5785 - playManifest request, allows access from 'unallowed' domain
- SUP-6009 - Getting the sent notifications data - users, mails etc.
- SUP-6187 - Unable to get the category ids from API
- PLAT-4097 - quiz.update fails when using format=9 (jsonp)
- PLAT-4782 - EmailReport:cue-point.VAST/Creatives gets wrong value

* Mon Dec 21 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.5.0-1
- Ver Bounce to 11.5.0

* Mon Dec 21 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.4.0-12
- Added support for custom parameters on akamai hds urls. 
  Needed in order to add hdcore=x.x.x when playing without the player Akamai HD plugin.

* Sat Dec 19 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.4.0-11
- SUP-6332 - Live entry has not been fully uploaded / transcoded
- SUP-6763 - Cross Kaltura connector does not export thumbnails
- PLAT-4712 - reduce duplicates in entryRequired
- PLAT-4445 - Failed to change privacy to category by user from group with permission manager
- PLAT-4663 - Support for HTTP Authentication in MRSS Feed ingestion
- PLAT-4788 - TMZ SFTP YouTube connector issues

* Mon Dec 7 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.4.0-1
- Ver Bounce to 11.4.0

* Sun Dec 6 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.3.0-12
- SUP-4598 - Infinite entry creation when using "Create new entry for every broadcast session"
- SUP-5438 - Converting Live Stream to VOD Not Working at all
- SUP-6536 - Entries Not in "Ready" Status - Fail to Clone
- SUP-6614 - ARF transcoding failure
- PLAT-3386 - Stream is rewinded on HLS when stopping and starting the stream with FMLE
- PLAT-4068 - When streaming with FMLE, first chunk has invalid duration (mostly after stop-start)
 
* Mon Nov 23 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.3.0-1
- Ver Bounce to 11.3.0

* Sun Nov 22 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.2.0-12
- 11.2.0 final

* Wed Nov 18 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.2.0-8
- SUP-6218 - Live entry, VOD entry stuck on "Pending" status
- PLAT-4028 - Enable adding categories with privacy context to syndication feeds

* Mon Nov 9 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.2.0-1
- Ver Bounce to 11.2.0

* Mon Nov 9 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.1.0-11
- Final 11.1.0 release

* Fri Nov 6 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.1.0-10
- SUP-5976 - Channel - kuser_id is '0' Causing Redundant Errors Sent to Users
- SUP-4924 - API changes 'KalturaFlavorAssetFilter'
- SUP-6003 - Setting the frameRate parameter to float
- PLAT-3078 - TestMe should output JSON rather than XML
- PLAT-4067 - Like->List - adding "creation-date" field 
- PLAT-3593 - DVR refactoring

* Tue Nov 3 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.1.0-8
- Fix manual HLS live streaming:
  https://github.com/kaltura/server/pull/3430
  http://forum.kaltura.org/t/manual-live-stream-not-happening/3782/11

* Mon Nov 2 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.1.0-7
- https://github.com/kaltura/server/pull/3420
- https://github.com/kaltura/server/pull/3421

* Mon Oct 26 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.1.0-1
- Ver Bounce to 11.1.0

* Sun Oct 25 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.0.0-12
- SUP-6102 - Default Metadata not working via Krecord (BB/ KMS)
- PLAT-3920 - add Like->list

* Wed Oct 21 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.0.0-7
- Pre create dirs under app/cache in order to set them to proper permissions

* Thu Oct 15 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.0.0-4
- Trying to use current default 04.*Params.ini

* Mon Oct 12 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.0.0-1
- Ver Bounce to 11.0.0

* Sun Oct 11 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.21.0-9
- SUP-5280 - "userId" flashvar to player?
- SUP-5457 - TMZ - Reduce cache age for certain partner
- SUP-5523 - Authentication error for youtube API distribution PID 1895531, connector ID 1420071
- SUP-5673 - HLS URL
- New ffmpeg version [2.7.2]

* Mon Oct 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.21.0-6
- https://github.com/kaltura/platform-install-packages/issues/455

* Mon Sep 21 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.21.0-1
- Ver Bounce to 10.21.0

* Mon Sep 21 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.20.0-11
- SUP-3920 - Downloading Error when trying to download the original CSV file

* Wed Sep 16 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.20.0-9
- https://github.com/kaltura/server/pull/3194
- https://github.com/kaltura/server/pull/3187

* Mon Sep 7 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.20.0-1
- Ver Bounce to 10.20.0

* Mon Sep 7 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.19.0-9
- PLAT-3752 - Live Analytics | Driver hangs when handling events with empty partnerId/entryId
- PLAT-3733 - Notifier job- remove write of the notification result to the DB
- PLAT-3477 - Allow hash function to use for appToken.startSession to be defined on appToken.add

* Mon Aug 24 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.19.0-1
- Ver Bounce to 10.19.0

* Thu Aug 20 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.18.0-11
- https://github.com/kaltura/server/pull/3066

* Thu Aug 20 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.18.0-10
- PLAT-3659 - baseEntry->addfromUploadedFile fails for data entry 
- SUP-2038 - Multiple Playlists - API inquiry
- SUP-5243 - KMC strips KalturaEndUserReportInputFilter when generating CSV
- SUP-4380 - Comments in e-mail notification
- PLAT-3522 - TR Reverse Proxy - pass "od" parameter when redirecting to mwEmbedLoader.php
- PLAT-3558 - Add Support for AIFF File Format in base.ini
- PLAT-3575 - Main file should be ism not a4m

* Mon Aug 10 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.18.0-1
- Ver Bounce to 10.18.0

* Thu Aug 6 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.17.0-10
- SUP-5223 - KMS uploads do not inherit entry's 'Default Metadata Settings'
- PS-2298 - Custom Metadata HTTP notification - JSON with special chars
- SUP-4363 - API - captionAsset - serveByEntryId issue
- PLAT-3182 - eCDN: silverlight multicast plugin doesn't produce 30fps
- PLAT-3293 - provider name is too long
- PLAT-3523 - Extract Input validation to its own thread
- PLAT-3576 - Remove TTL From Register_File
- PLAT-3546 - TR Reverse Proxy support - validate domain from "x-forwarded-host" header against white-list

* Wed Aug 5 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.17.0-8
- Do not compile against FDK and faac as distributing the binary with such support violates license.
  See:
  https://github.com/kaltura/platform-install-packages/issues/392
  https://trac.ffmpeg.org/ticket/4735

* Thu Jul 30 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.17.0-4
- https://github.com/kaltura/server/pull/2943

* Mon Jul 27 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.17.0-2
- Changed kaltlog alias to grep pattern 'PHP ' and not 'PHP' since that catches things like 'IZLe9ciBPHPcaiToJfOgv0w96eKrocGEm4oiL8piQreTaUmKbZaUk6wop7RM' which arent errors at all.

* Mon Jul 27 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.17.0-1
- Ver Bounce to 10.17.0

* Fri Jul 24 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.16.0-6
- SUPPS-299 - Notifications issue - replacement video event
- SUP-5363 - WebEx Connector Errors - during and after Cisco BACKUP
- PLAT-3504 - Zombie cleaner check
- PLAT-3458 - WV flavor does not created

* Mon Jul 13 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.16.0-2
- https://github.com/kaltura/server/pull/2838 merged so SOURCE31 is no longer needed.

* Mon Jul 13 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.16.0-1
- Ver Bounce to 10.16.0

* Sun Jul 12 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.15.0-8
- https://github.com/kaltura/server/pull/2844#event-353800482

* Fri Jul 10 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.15.0-7
- Local patch for https://github.com/kaltura/server/pull/2838

* Thu Jul 9 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.15.0-6
- Disable MySQL strict mode when deploying DB
- Added HTTP notification templates to deployment
- PLAT-3178 - eCDN: KES multicast
- PLAT-3180 - eCDN: KES non-flat multicast support from backend
- PLAT-3214 - eCDN: KES multicast - player changes
- PLAT-2924 - OTT DIstribution Module enhancements for MediaPrep Phase 1
- PLAT-3326 - Developer Account
- SUP-4344 - Presentation not uploaded to CaptureSpace
- SUP-3031 - Uploading issue
- SUP-3117 - getting an error on bulk category upload
- SUP-3867 - TechSmith relay issue
- SUP-4641 - Wrong content type returned for JS documententry in Chrome 42
- SUP-4776 - Dynamically retrieve the updated default thumbnail asset
- SUP-5236 - WeatherNation - Media server becoming unavailable 
- SUP-4191 - Live stream stopped
- SUP-5228 - Cannot live stream with specific entry
- SUP-5257 - Live Stream presents still image of a previously streamed content
- PS-2287 - New HTTP notification fired when change is made to entry custom data
- PLAT-3387 - Spark stopped processing events when failed to parse a log line
- PLAT-3304 - Devices stopped to play Live(Ad stitching) after 90 min
- PLAT-3066 - Anonymous analytics 
- PLAT-3014 - Converison profile default entry should not copy type and media type
- PLAT-3016 - entitlement prevent from load Conversion Profile Default entry
- PLAT-3287 - removeGroupSmils concurrent modification
- PLAT-3292 - Playlist API - Cannot save CategoryEntryAdvancedFilter as an advanced search filter
- PLAT-3294 - OR between KalturaCategoryEntryAdvancedFilter and KalturaMetadataSearchItem produces AND
- PLAT-3295 - Playlist API - Advanced filter items are duplicated

* Mon Jun 29 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.15.0-1
- Ver Bounce to 10.15.0

* Sun Jun 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.14.0-7
- https://github.com/kaltura/server/pull/2751

* Sun Jun 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.14.0-6
- SUP-4393 - Downloading screen recording from KMS saved as tmp file
- SUP-4339 - Email notifications send all addresses in the "To" field
- PLAT-3215 - ES3 - UnMuxed Solution Project
- PLAT-2908 - syndication feeds using playManifest not working with Access Control 
- PLAT-3072 - many kuser_kgroup queries
- PLAT-3059 - KalturaNullableBoolean in format=json

* Sun Jun 21 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.14.0-3
- https://github.com/kaltura/server/pull/2707

* Tue Jun 16 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.14.0-1
- Ver Bounce to 10.14.0

* Sun Jun 14 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.13.0-5
- SUP-4515 - Widevine Media Transcoding Errors
- SUP-4362 - Adding Tags with less than 2 letters when uploading 
- SUP-4491 - Entry ID containing # sign causing entries not to load
- SUP-4264 - Thumbnail rotation not working with ARF files
- SUP-4001 - Category listing options is not filtering on KMC
- PLAT-2983 - externalSourceType isn't being cloned
- PLAT-2872 - Refactor media server to suit SyncPoints requirements

* Mon Jun 1 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.13.0-1
- Ver Bounce to 10.13.0

* Sun May 31 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.12.0-5
- SUP-4016 - Cannot find category in analytics "Select Categories" drop down menu
- SUP-4408 - Specific WMV file not transcoding 
- SUP-4695 - Entry does not display as expected
- SUP-4739 - Player's download button does not work in KMS
- PLAT-2204 - Can't add thumb cuepoint of sub type chapter without a slide
- PLAT-2987 - Auto-Intermediate-source flow for sources that processable only by Mencoder
- https://github.com/kaltura/server/blob/Jupiter-10.12.0-typeReflectorError/api_v3/lib/KalturaTypeReflector.php

* Tue May 19 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.12.0-1
- Ver Bounce to 10.12.0

* Sun May 17 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.11.0-7
- PLAT-2871 - Caption search using KalutraBaseEntryFilter::advancedSearch and cross metadata search
- PLAT-1998 - Avoid the need to update many metadata objects 
- PLAT-2850 - API Changes for Q&A 
- PLAT-2946 - Hide default template uiconfs from partner preview&&embed 
- SUP-3451 - KMC error - The language 'sv_SE' has to be added before it can be used. 
- SUP-3965 - Telepictures - high storage usage, flavors are not deleted after export? 
- PLAT-2914 - Too many logs are written to file 
- PLAT-2906 - Json serializer causing Studio crash 
- PLAT-2387 - manual dispatch error 
- PLAT-2934 - clip_test script fails 
- PLAT-2940 - groupUser->list return fatal error
- https://github.com/kaltura/server/pull/2561 

* Tue May 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.11.0-1
- Ver Bounce to 10.11.0

* Tue May 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.10.0-3
- Tmp patch for https://github.com/kaltura/server/pull/2522 and https://github.com/kaltura/server/pull/2521

* Mon May 4 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.10.0-2
- PLAT-2042 - Kaltura MRSS Ingest for PostMedia (TR next)
- PLAT-2829 - New feature: Add a pager to playlist->execute
- SUP-3584 - Ellentv.com V2 playlist is out of sync
- SUP-4358 - [Pearson] Java API SDK throws a NumberFormatException
- PLAT-2865 - Live - isLive remains on true after stop streaming (regression)
- PLAT-1600 - Duplicate VOD entry is created when stopping streaming before live entry starts to play. 
- PLAT-2497 - randomly the HLS flavors in the cloud transcode are not in sync
- PLAT-2885 - Kaltura Live with DVR: Player stuck for a few minutes after loading page
- WEBC-467 - Application error received when attempting to edit a webcast 

* Sun Apr 26 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.10.0-1
- Ver Bounce to 10.10.0

* Sun Apr 26 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.9.0-7
- SUP-4081 - distributing from remote storage
- PLAT-2055 - Trim is not performed on Kaltura Live recorded VOD entry.
- PLAT-2593 - Live - Passthrough recorded entries sometimes missing Source and Ingest3 flavors
- PLAT-2762 - Sometimes live entries are not synced between DC
- PLAT-2489 - image extension - set according to original file

* Mon Apr 13 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.9.0-5
- merged https://github.com/phansys/server/commit/9e24777565cf21bf65f327c1406fa2cb8ff70dc3

* Mon Apr 6 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.9.0-1
- Ver Bounce to 10.9.0

* Sun Apr 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.8.0-12
- Run installPlugins.php post upgrade.

* Sun Apr 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.8.0-11
- SUP-3451 - KMC error - The language 'sv_SE' has to be added before it can be used.
- SUP-4124 - Adding support for video file extension .m2ts
- SUP-3916 - [2.27.1] AutoEmbed+HTTPS+streamerType=auto does not play on HTTP sites
- SUP-3864 - Download gets cut for large flavors
- PLAT-2653 - DVR audience missing on calculation audience on entry cube
- PLAT-2616 - Entries on "All Viewed Live Entries" dashboard do not sorted
- PLAT-2630 - location map enhancements
- PLAT-1680 - Server KalturaMediaEntryFilterForPlaylist call does not respect filter limit or pagging
- PLAT-2005 - Can't use Amazon remote storage
- PLAT-2654 - DVR audience missing on total audience calculation on CSV report
- PLAT-2646 - Predictive Tags: Suggested tags displayed twice

* Thu Apr 2 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.8.0-10
- Tmp patch due to https://github.com/kaltura/platform-install-packages/issues/367

* Mon Mar 23 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.8.0-3
- Stop monit before starting upgrade, restart when done.

* Mon Mar 23 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.8.0-2
- If upgrade, lets try to stop apache at %pre phase, seems that writing new files while its runnign cause it to hang.

* Mon Mar 23 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.8.0-1
- Ver Bounce to 10.8.0

* Sun Mar 22 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.7.0-2
- PLAT-2550 - owner of an entry should be able to update entitledUsersEdit & entitledUsersPublish
- PLAT-2542 - kFileSyncUtils::moveFromFile crashes on "object already exists"
- PLAT-2536 - Request of max available flavorIds or flavorParamIds gets 404
- PLAT-2601 - Enable retry for Webex imports

* Sun Mar 15 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.7.0-1
- Ver Bounce to 10.7.0

* Mon Mar 8 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.6.0-2
- SUP-3864 - Download gets cut for large flavors
- PLAT-2524 - sphinxFilter code relocation - (KMS-5141)
- PLAT-2540 - Live - A/V out of sync in second part of recorded entry after restart streaming (regression)

* Fri Mar 6 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.6.0-1
- Ver Bounce to 10.6.0

* Tue Feb 24 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.5.0-6
- Fix clipapp ver

* Sun Feb 22 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.5.0-5
- SUP-2942 - Audio-Video Sync Issue on Kaltura Live stream
- SUP-3443 - VOD entry missing after livestream (from Kaplan) - "race condition"
- SUP-3251 - Update Syndication XSD to Comply With the media->getMrss API Call
- SUP-3572 - Email notifications send all addresses in the "To" field
- SUP-3927 - TMZ - Analytics report request
- SUP-3608 - Kaltura java client fail on test
- SUP-3644 - Changing feed's XML without changing the feed's url

* Tue Feb 15 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.5.0-3
- For this one: https://github.com/kaltura/server/pull/2258

* Wed Feb 11 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.5.0-1
- Ver Bounce to 10.5.0

* Wed Feb 4 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.4.0-1
- Ver Bounce to 10.4.0
- SUP-3505 - Player not working in Chrome with entries that are shorter then 5 mins (KS PREVIEW)
- SUP-2485 - can't change USER_LOGIN_ATTEMPTS maximum value in admin console
- SUP-2974 - Image file extension lost when uploading via bulk upload
- PLAT-2452 - EBU - Fixing in-accurate aspect ratio (partner 1844091)
- PLAT-2451 - slides triplicate on copy to vod entry (EBU)

* Thu Jan 25 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.3.0-3
- SUP-3065 - Cannot create category using CSV - "already exists" 
- SUP-3161 - Source assets missing source tag
- PLAT-1751 - Reduce cache when listing live cuepoints
- PLAT-2082 - redirectEntryIdEqual filter causes an exception
- KMS-5141 - Cannot perform search by Custom Data "Text Select List" field (Drop Down List)

* Thu Jan 15 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.3.0-2
- Added the VOD delivery profile.

* Tue Jan 13 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.3.0-1
- Ver Bounce to 10.3.0

* Sun Jan 10 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.2.0-5
- Ver Bounce to 10.2.0
- SUP-2516 - Crop thumbnail after grab from video error
- SUP-3282 - Multi-Account Management Console copy content from template account Error
- PLAT-2347 - Failure in recognition of the long/lat in the location reports due to update to IP2Location
- PLAT-2313 - Entitlements are not inherited from live entry to recorded entry (was "API error on kwebcast page")
- PLAT-1631 - Support Media Repurposing use-case (time capsule) 

* Wed Jan 7 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.2.0-1
- Ver Bounce to 10.2.0

* Sun Dec 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 10.1.0-2
- Bounce KMC ver.

* Sun Dec 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 10.1.0-1
- Ver Bounce to 10.1.0
- Changes to support RHEL7 and PHP 5_4.
- Added app/release-notes.md and app/license.txt

* Mon Dec 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 10.0.0-8
- https://github.com/kaltura/server/pull/2009
- https://github.com/kaltura/server/pull/2010
 
* Thu Dec 11 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 10.0.0-3
- call service instead of /etc/init.d

* Thu Dec 11 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 10.0.0-1
- Ver Bounce to 10.0.0
- Webcasting BE enhancements
- Kaltura Media Server supporting Webcasting BE enhancements
- Kaltura-Live DVR Window change to 24 hours
- Allow searching cuepoints in categories
- SUP-2899 - User sessions cannot view their own user data
- SUP-2810 - ARF ingestion issue - audio garbled
- PLAT-2151 - report->getTable data amount restriction


* Mon Dec 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.8-3
- We do not need php-imap which is particularily important for RHEL/Cent 7 where this package does not exist.

* Mon Dec 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.8-1
- Ver Bounce to 9.19.8
- PLAT-1112 - LC - Add support for multiple video/audio substreams
- SUP-2614 - Playlist description is missing from Tiny URL
- SUP-2792 - Unable to update playlist 'orderBy' field
- SUP-3152 - Entry is set as "Ready" for corrupted source file
- PLAT-2080 - playList->execute - apply array manipulation only on manual playlists

* Tue Nov 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.7-2
- Added app/configurations/sphinx_schema_update which is read by kaltura-sphinx-schema-update.sh to determine rather or not to run

* Mon Nov 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.7-1
- Ver Bounce to 9.19.7
- SUP-2768 - Recorded copy of Live Entry stream doesn't retain custom metadata
- SUP-3144 - Manifest delivery returns HTTP 500 code - Es3
- PLAT-1952 - Using CloudTranscode transcoding profile - recording entry of live entry shorter than original live entry (in ~11 seconds)
- PLAT-2021 - Read permissions for Delivery profiles
- PLAT-2078 - First Entry of the Playlist does not appear as First entry on related video card 
- PLAT-889 - Support RTP and RTSP Wowza GoCoder ingest
- SUP-2935 - Remove Kaltura from being automatically added to the whitelisted domains
- PLAT-2069 - Add sub type for thumb cue point

* Sun Nov 2 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.6-1
- Ver Bounce to 9.19.6
- PLAT-1735 - Security checks missing in flavorAsset.getDownloadUrl
- PLAT-1965 - preventing useless AsyncDelete jobs creation
- SUP-2767 - The peak usage Summary usage totals are wrong in Multiacct Admin
- SUP-2935 - Remove Kaltura from being automatically added to the whitelisted domains
- PLAT-934 - Bulk-download job stuck if no source or source not 'ready' & no conversion
- PLAT-1973 - search media by user first name, last name, screen name 

* Sat Oct 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.5-1
- Ver Bounce to 9.19.5
- PLAT-1897 - Enable users to play-out the remaining DVR even with recording disabled
- PLAT-1459 - DVR take over during live broadcast
- PLAT-1886 - Support Live to VOD flow with no "down time" where DVR + Recording is enabled.
- PLAT-1476 - Stability issues around live recording / appending
- PLAT-1114 - Test Wirecast Encoder with Kaltura Live Platform
- SUP-2553 - Bulk upload URL problem 
- SUP-2202 - Live stream recording issue
- PLAT-1830 - Add access to the "Attachment" service to the "PLAYBACK_BASE_ROLE"
- PLAT-1957 - ERROR on log - Failed to list entries cue-points.

* Sun Oct 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.4-1
- Ver Bounce to 9.19.4
- PLAT-1556 - BACKMS5SecAudit - Add ability to invalidate KS by a session ID
- PLAT-1834 - Add support for the clipTo / seekFrom playManifest parameters in Akamai HDN2 deliveries
- PLAT-1928 - adding an entry several times to category reports batch error
- SUP-2489 - SF 48088 - Unable to download a Video
- SUP-2764 - sf 50841| Telepictures-Ellen| analytics does not match
- No email notification when removing member from channel

* Tue Sep 30 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.3-4
- http://forum.kaltura.org/t/upgrade-from-9-18-x-to-9-19-x-latest-release-as-on-date-caused-ssl-to-break/662

* Mon Sep 29 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.3-3
- Patch for auto embed to work, should be dropped when core merge.

* Sun Sep 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.3-2
- PLAT-1649 - Allow the option to disable KMC "forgot password" functionality per partner
- PLAT-1559 - KMC-login to ignore "remember me" checkbox per partner configuration
- PLAT-1558 - Add partner configuration to "disable" the "remember me" functionality in KMC login
- PLAT-1555 - add XSS protection in API to not allow HTML
- PLAT-1554 - Add ability to change the KS expiration for KMC login per partner
- PLAT-1548 - analytics reports downloaded from KMC do not enforce any access-control policies or any other means of authentication
- PLAT-1547 - stored XSS vulnerability in "my user settings" in the KMC
- PLAT-1886 - Support Live to VOD flow with no "down time" where DVR + Recording is enabled.
- PLAT-1663 - Create an API service that returns the version of the server
- SUP-2447 - Clipping entries throws an error
- API isCountryRestricted parameter returns-0

* Mon Sep 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.2-3
- Dropping patches that were already merged to Core.

* Fri Aug 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.2-1
- SUP-2591 - Application Error in Canvas iFRAME EMBED
- SUP-2581 - User Unable to Set Thumbnails /KMC
- PLAT-1543 - Replacing entry distribute the temporary entry

* Thu Jul 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.0-1
- Ver Bounce to 9.19.0
- SUP-2290 - API endDate and startDate issues
- SUP-2369 - executeplaylist service does not escape characters in the 'tag' field
- SUP-2422 - UserID cannot be removed from a category
- PLAT-1525 - key and iv in widevine configuration are switched 
- PLAT-1442 - Create template for "Entry Changed" email notification
- PLAT-1256 - Entry does not update replacement status properly if replacement fails to convert all flavors
- PLAT-1510 - Multi-stream sources and Watermarking

* Tue Jul 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.18.0-3
- https://github.com/kaltura/server/pull/1397/files#diff-0

* Sun Jun 29 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.18.0-1
- Ver Bounce to 9.18.0
- PLAT-1345 - API for per entry ingesting onTextData  (default 608 live captions)
- PLAT-1136 - expose session start time on live entries
- PLAT-1375 - Add configurable option to YouTube API connector - include entry name in YT 'raw file' filed instead of file name
- PLAT-1403 - ISM flow - change file sync sub type of the manifest flavor to ASSET sub type instead ISM
- PLAT-1299 - Add deletion mechanism to Webex drop Floder
- SUP-2266 - Change the dataUrl to use thumbnail API
- PLAT-1104 - KMC Login: The 'login' button is cut for Espan~ol
- PLAT-1105 - KMC Login: Default captions are not shown in the selected language
- PLAT-1106 - KMC Login: Default captions on the login page are editable

* Sun Jun 29 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.17.0-10
- From now on - will run update.php at each upgrade instead of specific scripts.

* Tue Jun 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.17.0-4
- Core now need the passwd for partner 99. Manually merged from 9.18.0.

* Tue Jun 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.17.0-3
- No need to override 01.Partner.template.ini any longer

* Sat Jun 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.17.0-1
- Ver Bounce to 9.17.0
- PLAT-1382 - Audio distortions on AAC
- PLAT-1308 - Delivery Managers 
- PLAT-1352 - Tvinci integration - extend POC connector for Kaltura Connect Demo
- PLAT-1111 - Lecture Capture - Ingestion and Management
- SUP-2000 - Error when entering the edit entry window with content moderator role
- SUP-1669 - Captions search returning incorrect number of results
- SUP-1992 - Updating YT content (SF 43231)
- SUP-2218 - Order of entries in KMS are not working for alphabetical order
- SUP-2008 - Bulk download option randomly generates broken links
- SUP-2119 - Issue with adding a new user

* Tue Jun 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.16.0-2
- Fix for https://github.com/kaltura/platform-install-packages/issues/147
* Wed May 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.16.0-1
- Ver Bounce to 9.16.0
- PLAT-974 - add partner Reference ID to KMC and Multi-Account console
- PLAT-1131 - Triggering distribution only when entry is assigned to a specific metadata
- PLAT-1267 - Merge both DCs manifests into a single combined manifest
- SUP-814 - Media counts in Channels do not match Channel preview or KMC counts
- SUP-1504 - Re-publishing a rejected media item doesn't update for channel owner
- SUP-1826 - Widevine encoding fails
- SUP-1867 - Flavors Quality
- SUP-1910 - Green line with flavor 480P
- SUP-1987 - Instant blocking of user on KMC
- SUP-2059 - Script error in Multiaccount console
- PLAT-1039 - Kaltura live entry gets duration 1 hours.
- PLAT-1311 - Wrong kaltura live duration when setting two DCs.
- PLAT-1323 - Sphinx optimization - dynamic attributes within the match optimization

* Mon May 19 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.15.0-7
- tmp patch until https://github.com/jessp01/server/commit/13bd0c220111c1809d1a7f6e5544cc02b4e26cd9 is merged back to Core.

* Thu Apr 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.15.0-1
- Ver Bounce to 9.15.0
- SUP-1866 - Disabling email notifications
- PLAT-1155 - Live streaming provision should exclude cloud transcode where not available
- PLAT-1241 - Kaltura live - add support for setting base URL per customer
- PLAT-1163 - Job suspend
- i18n system flip (switched off by default)
- PLAT-975 - add an option to define partner specific default thumbnail for audio entries 
- PLAT-982 - m4a container support
- PLAT-1037 - Using updateContent API request on an entry does not retain custom thumbnails 
- Add a GeoDistance condition to the access control profile which verifies whether the request IP is within a given latitude:longitude:radius ranges (requires new ip2location)
- SUP-1772 - Video replacement - cannot "Preview" flavor asset before approving replacement
- SUP-1866 - Disabling email notifications
- SUP-1742 - INTERNAL_SERVER_ERROR when trying to reset to a password with an invalid structure
- PLAT-692 - Freezes occurs when playing kaltura live entry. (happens in production as well)
- PLAT-1229 - When setting liveTranscording without source->FMLE export config is wrong
- PLAT-1233 - Audio-Video Sync Issue on Live stream
- PLAT-952 - Production:Kaltura live entry that is stream for many hours can't play->media not found


* Tue Apr 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.14.0-6
- We need to run the alter scripts in the event the version is lower than n, not equal to n. Why? cause jumping from say 11 to 13 is completely legit.

* Mon Apr 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.14.0-4
- Another instance of the ipadnew tag[darn!].

* Sun Apr 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.14.0-1
- Ver Bounce to 9.14.0
- PLAT-927 - In YouTube API connector map an entry to a YT playlist
- SUP-1641 - Open Editor for the config file is not working
- SUP-1775 - MP4 corrupted source shows as ready in KMC 
- SUP-1579 - Entry 1_q5jzwqd0 not found in HTTP progressive
- SUP-1612 - remote storage is not updated
- SUP-1676 - CSV Bulk Upload - Fail
- PLAT-1080 - Security Fix - Prevent Admin-Console from being loaded in iFrame
- PLAT-1081 - Security Fix - disable auto complete for password field in admin-console login
- PLAT-1082 - Security Fix - admin-console session cookie security hardening
- PLAT-1151 - Webex - detect black/silent conversions
- PLAT-1145 - Updating UIConf with JSOn Config looses the config XML 

* Sun Apr 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.13.0-6
- Here is our problem: the ip{hone,ad}new tags are only good for Akamai HLS, on any other serve method, it makes ip{hone,ad} serves not to work.
  If a user DOES wish to use Akamai HLS, we have the kaltura-remote-storage-config.sh for them to run.

* Thu Mar 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.13.0-4
- Log update scripts output to file instead of STDOUT

* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.13.0-3
- if system.ini is available, source it in kaltura_base.sh, good when you run stuff like:
  mysql -h$DB1_HOST -p$DB1_PASS

* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.13.0-2
- Typo in file path.

* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.13.0-1
- Ver Bounce to 9.13.0
- PLAT-307 - FFMpeg 2.1.3 integration 
- PLAT-914 - FileSyncImport - re-use curl 
- PLAT-558 - Live streaming should support multiple stream ingest 
- PLAT-932 - Production admin_console: "View History" doesn't work 
- PLAT-1003 - E-mail for notification ,configurable fields override default values 
- SUP-1567 - Problem to duplicate KSR from admin console. 
- SUP-1625 - Avoid creating notification jobs when no notification email is configured


* Tue Mar 20 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.12.0-7
- Remove password tag from app/deployment/base/scripts/init_content/01.UserRole.99.template.xml.
  It causes issues and isn;t needed.

* Tue Mar 20 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.12.0-6
- https://github.com/kaltura/server/commit/4d47c158774ebd41b0a60e6af20f0beab02d459d did not make it in so, reapplying the patch.

* Tue Mar 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.12.0-5
- Don't run upgrade scripts if not INIs.

* Thu Mar 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.12.0-2
- Generate random monit passwd.

* Thu Mar 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.12.0-2
- Fix for https://github.com/kaltura/platform-install-packages/issues/71

* Sun Mar 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.12.0-1
- Ver Bounce to 9.12.0
- PLAT-852 - Wowza working with multicast in a hybrid model Closed
- PLAT-823 - enable use of draft entries in playlists - when video media is not expected Closed
- Added the ability to create transcoding profiles with no flavors based on the permission "Enable KMC transcoding profile selection for draft entries".
- Entries based on such transcoding profile are created with status "Ready".
- PLAT-599 - On Course copy (copy category entries) enable to clone all entries Closed
- Removal of 32 categories limitation on entry
- PLAT-343 - Improved Fixed-Aspect-Ratio calculation Closed
- PLAT-933 - Migrate to new Widevine url structure in encryption Closed
- MG-134 - thumbnail - option to get an entry thumbnail with width/height closest to required work partial Closed
- Backend permanent bypass to cache was verified by QA.Core
- Fix must be verified by QA.App as well
- PLAT-865 - add partner CRM id to the api Closed
- PLAT-987 - Change default DVR window to be 2h rather than 24h Closed 
- SUP-1505 - Is there a limitation for bulk download from KMC? Closed
- SUP-1530 - Retry mechanism for import jobs when 'couldn't connect to host' Deployed
- SUP-1574 - 'Add to playlist' shows playlists that does not belong to the logged user_id Deployed


* Wed Mar 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-16
- Place holder for Chain. See: https://github.com/kaltura/platform-install-packages/issues/57
  
* Fri Feb 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-15
- Fixes https://github.com/kaltura/platform-install-packages/issues/50

* Fri Feb 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-14
- https://github.com/kaltura/platform-install-packages/issues/51

* Tue Feb 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-11
- Update version number.

* Mon Feb 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-9
- Consent strings added.

* Mon Feb 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-6
- Post install mail templt: added the debug aliases to Tip #4 discussing troubleshooting procs.

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-4
- Added tracking concent messages file.

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-2
- Added mechanism to handle SQL alters.

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-1
- Fixes:
  SUP-1389 - Flipped thumbnail for video Ready for Deployment
  SUP-1416 - Removing the CC from the Email notifications Target Tamplates Ready for Deployment
  SUP-1382 - KMC Return 2 Source flavors
  PLAT-925 - Bug for PLAT-722 (Moderation with Live): Basic functionality not working consistently Closed

* Sat Feb 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-48
- fixed typo sphinx.populate.template.rc

* Sat Feb 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-47
- placeholder @ADMIN_CONSOLE_ADMIN_MAIL@ for mail in monit.conf.

* Sat Feb 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-46
- monit config moved to %%prefix/app/configurations/monit

* Sat Feb 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-45
- Integrated David Bezemer's Admin Console changes for monit.

* Sat Feb 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-44
- Added patched monit temlpates.

* Sat Feb 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-43
- Added alias for allkaltlog and changed kaltlog. Suggestion by David Bezemer.

* Thu Feb 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-42
- Fix for https://github.com/kaltura/platform-install-packages/issues/37

* Wed Feb 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-39
- Fix https://github.com/kaltura/platform-install-packages/issues/34

* Tue Feb 11 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-38
- Removed IsMindex plugin from template.

* Mon Feb 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-34
- Fix editing of p99 template.

* Sun Feb 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-32
- Only gen client libs if conf files are in place.

* Sun Feb 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-31
- Fix for https://github.com/kaltura/platform-install-packages/issues/28

* Sun Feb 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-30
- Fix for https://github.com/kaltura/platform-install-packages/issues/25:
disable Audit plugin.
- Fix def. flavor creation.

* Sun Feb 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-29
- Fix for https://github.com/kaltura/platform-install-packages/issues/23.

* Fri Feb 7 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-28
- Fix for https://github.com/kaltura/installer/issues/5

* Wed Feb 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-27
- Fixed the conversion template for p99. Include flav. ID 19.

* Sun Feb 2 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-21
- Only PHP CLI is needed.

* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-19
- New KDP3 ver v3.9.7 and hence, new 01.uiConf.99.template.xml. 

* Fri Jan 31 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-18
- Fixed template for UI conf generation.

* Wed Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-10
- debugme.

* Wed Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-9
- %%{prefix} to be owned by %%{kaltura_user}, %%{kaltura-user}

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-4
- Depend on mailx.

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-3
- Added emails_en.template.ini.

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-1
- Moving to IX-9.9.0

* Mon Jan 20 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-33
- Create additionally needed directories under web.

* Sat Jan 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-28
- Make sure SELinux is not enabled.

* Fri Jan 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-27
- Do not create system.ini, post installs create it from template.

* Wed Jan 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-24
- Added web/tmp web/control and web/dropfolders.

* Sun Jan 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-23
- We have CLI scripts in PHP that need to run post install of the base package.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-22
- Change name from .*.template.rc to .*.rc.template so that monit.d/*.rc will work correctly.

* Thu Jan 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-16
- No need for base.ini, there are no tokens there.

* Thu Jan 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-15
- Replace tokens in local.ini and base.ini as well.

* Thu Jan 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-13
- Create all base dirs and make sure they will be removed during un.

* Thu Jan 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-12
- Added creation of /opt/kaltura/tmp dir.
- Postinstall message.

* Wed Jan 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-9
- rm system.ini synlink only at complete uninstalls, not upgrades.

* Wed Jan 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-8
- Do not override system.ini, add to it.

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-7
- Added version file.
- Added dep in kaltura-postinst.

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-6
- Depend on kaltura-monit and also fix PATH and LD_LIBRARY_PATH to include /opt/kaltura/{bin,lib}.

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-5
- Fuck me.

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-4
- Correctly replace tokens!

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-3
- Replace tokens.
 
* Fri Jan 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-2
- Permissions corrected.

* Mon Dec  23 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-1
- First package.

