%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define apache_user	apache
%define apache_group	apache
%define prefix /opt/kaltura
%define confdir %{prefix}/app/configurations
%define logdir %{prefix}/log
%define webdir %{prefix}/web
%define codename Mercury

Summary: Kaltura Open Source Video Platform 
Name: kaltura-base
Version: 13.5.0
Release: 4
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
Source32: KDLOperatorFfmpeg1_1_1.php
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
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/tmp/dropFolderFiles
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
sed -i 's#<html5Url>/html5/html5lib/v.*/mwEmbedLoader.php</html5Url>#<html5Url>/html5/html5lib/%{html5_version}/mwEmbedLoader.php</html5Url>#g' $RPM_BUILD_ROOT%{prefix}/app/deployment/base/scripts/init_content/01.uiConf.99.template.xml
sed -i "s#^;kmc_login_version = @KMC_LOGIN_VERSION@#kmc_login_version = %{kmc_login_version}#g" $RPM_BUILD_ROOT%{prefix}/app/configurations/local.template.ini
sed -i "s@clipapp_version = @CLIPPAPP_VERSION@#clipapp_version = %{clipapp_version}#g" $RPM_BUILD_ROOT%{prefix}/app/configurations/local.template.ini
sed -i "s#^clipapp_version =.*#clipapp_version = %{clipapp_version}#g" $RPM_BUILD_ROOT%{prefix}/app/configurations/base.ini
sed -i "s#^;kdp3_wrapper_version = @KDP3_WRAPPER_VERSION@#kdp3_wrapper_version = %{kdp3_wrapper_version}#g" $RPM_BUILD_ROOT%{prefix}/app/configurations/local.template.ini
sed -i 's@^writers.\(.*\).filters.priority.priority\s*=\s*7@writers.\1.filters.priority.priority=4@g' $RPM_BUILD_ROOT%{prefix}/app/configurations/logger.template.ini 
# our Pentaho is correctly installed under its own dir and not %prefix/bin which is the known default so, adding -k path to kitchen.sh
sed -i 's#\(@DWH_DIR@\)$#\1 -k %{prefix}/pentaho/pdi/kitchen.sh#g' $RPM_BUILD_ROOT%{prefix}/app/configurations/cron/dwh.template
rm $RPM_BUILD_ROOT%{prefix}/clients-generator/sources/android/DemoApplication/libs/libWVphoneAPI.so
#rm $RPM_BUILD_ROOT%{prefix}/clients-generator/sources/android2/DemoApplication/libs/libWVphoneAPI.so
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
rm $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.d/*template*
cp %{SOURCE25} $RPM_BUILD_ROOT%{prefix}/app/configurations/logrotate/
cp %{SOURCE26} $RPM_BUILD_ROOT%{prefix}/app/configurations/logrotate/


# David Bezemer's Admin console and monit patches:
cp %{SOURCE17} $RPM_BUILD_ROOT%{prefix}/app/admin_console/configs/navigation.xml
cp %{SOURCE18} $RPM_BUILD_ROOT%{prefix}/app/admin_console/views/scripts/index/monit.phtml
cp %{SOURCE19} $RPM_BUILD_ROOT%{prefix}/app/admin_console/controllers/IndexController.php
# we bring a1nother in kaltura-batch
rm $RPM_BUILD_ROOT%{prefix}/app/configurations/batch/batch.ini.template
cp %{SOURCE32} $RPM_BUILD_ROOT%{prefix}/app/infra/cdl/kdl/KDLOperatorFfmpeg1_1_1.php

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
		# || true because it may fail if root_squash is used
		chown -R %{kaltura_user}.%{apache_user} %{prefix}/app/cache/ %{prefix}/log %{prefix}/var/run || true
		chmod 775 %{prefix}/web/content || true

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
			echo "GRANT INSERT,UPDATE,DELETE,SELECT,ALTER,DROP,CREATE ON kaltura.* TO '$DB1_USER'@'%';FLUSH PRIVILEGES;"|mysql -h$DB1_HOST -u $SUPER_USER -p$SUPER_USER_PASSWD -P$DB1_PORT
			echo "GRANT INSERT,UPDATE,DELETE,SELECT,ALTER,DROP,CREATE ON kaltura_sphinx_log.* TO '$DB1_USER'@'%';FLUSH PRIVILEGES;"|mysql -h$DB1_HOST -u $SUPER_USER -p$SUPER_USER_PASSWD -P$DB1_PORT
			echo "ALTER TABLE kaltura_sphinx_log.sphinx_log ADD type INT AFTER created_at;"|mysql -h$DB1_HOST -u $SUPER_USER -p$SUPER_USER_PASSWD -P$DB1_PORT 2>/dev/null|| true
		fi
			MINUS_2_PARTNER_ADMIN_SECRET=`echo "select admin_secret from partner where id=-2"|mysql -N -h$DB1_HOST -u$DB1_USER -p$DB1_PASS $DB1_NAME -P$DB1_PORT`
			CONF_FILES=`find $APP_DIR/deployment/updates/ -type f -name "*template.xml"`
			for TMPL_CONF_FILE in $CONF_FILES;do
				CONF_FILE=`echo $TMPL_CONF_FILE | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
				if [ -r $CONF_FILE ];then
					cp $CONF_FILE $CONF_FILE.backup
				fi
				if `echo $TMPL_CONF_FILE|grep -q template`;then
					cp  $TMPL_CONF_FILE $CONF_FILE
				fi
				sed -e "s#@ADMIN_CONSOLE_PARTNER_ADMIN_SECRET@#$MINUS_2_PARTNER_ADMIN_SECRET#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -i $CONF_FILE		
			done
#	@ADMIN_CONSOLE_PARTNER_ADMIN_SECRET@ @SERVICE_URL@	
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
* Sat Oct 14 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.5.0-4
- Nightly build.

* Fri Oct 13 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.5.0-3
- Nightly build.

* Thu Oct 12 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.5.0-2
- Nightly build.

* Wed Oct 11 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.5.0-1
- Ver Bounce to 13.5.0

* Mon Oct 9 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.4.0-7
- Don't call fullMkdir since it requires full file name (https://github.com/kaltura/server/pull/6139)
- apigrep - support case insensitive (https://github.com/kaltura/server/pull/6137)
- Update the add permission script date (https://github.com/kaltura/server/pull/6135)
- PLAT-8083: allow inclusion/exclusion cloning metaData and flavors objects (https://github.com/kaltura/server/pull/6134)
- Fix for 6sec default chunk duration (https://github.com/kaltura/server/pull/6131)
- PLAT-7986: Add getVolumeMap action to media service (https://github.com/kaltura/server/pull/6130)
- PLAT-8085: Fix elastic populate Exceptions (https://github.com/kaltura/server/pull/6129)
- SUP-12195: Default value for update method (https://github.com/kaltura/server/pull/6127)
- PLAT 6597: apply 6 sec default chunk duration (https://github.com/kaltura/server/pull/6125)
- FileGetContant patch for maxlen (https://github.com/kaltura/server/pull/6124)
- PLAT-8049: Upgrade FB SDK to 2.5 (https://github.com/kaltura/server/pull/6123)
- Adding defaultExpiry as 30 day for filesystemPlayKitJsSourceMap (https://github.com/kaltura/server/pull/6122)
- PLAT-7961: sftp engine use kFile function (https://github.com/kaltura/server/pull/6121)
- PLAT-7951: Add _matchand_entitled_kusers_view entry filter (https://github.com/kaltura/server/pull/6120)
- PLAT-7961: Adopt the myFlvStreamer to FileSyncKey (https://github.com/kaltura/server/pull/6118)
- SUP-12069: Add url domain to uploadToken->add (https://github.com/kaltura/server/pull/6117)
- PLAT-7988: Return only the time and not an array when parsing caption times (https://github.com/kaltura/server/pull/6116)
- Increase chunk retries count and max exec time (https://github.com/kaltura/server/pull/6114)
- PLAT-7961: Tunnel Set content through kFile in kActivitiBusinessProcessProvider.php (https://github.com/kaltura/server/pull/6113)
- PLAT-7961: Remove redundant code in BusinessProcessCaseService.php (https://github.com/kaltura/server/pull/6112)
- PLAT-8060: Add fullscreen attributes to iframe (https://github.com/kaltura/server/pull/6111)
- Fix playkit embed (https://github.com/kaltura/server/pull/6109)
- PLAT-7961: Get content in KalturaFileSync through kFileSyncUtils (https://github.com/kaltura/server/pull/6108)
- PLAT-8037: Obtain kuser from ks when users:exclude clone option is given (https://github.com/kaltura/server/pull/6107)
- PLAT-7961: Use kFile::createTempFile() instead of getTempFileWithContent() (https://github.com/kaltura/server/pull/6106)
- PLAT-5577: Always return primary server stream first when serving playManifest (https://github.com/kaltura/server/pull/6105)
- PLAT-8064: Add permission to restore entry action to Admin console partner (https://github.com/kaltura/server/pull/6104)
- PLAT-8064: Add restore entry button to entry investigation (https://github.com/kaltura/server/pull/6103)
- PLAT-7961: Use kFile::appendToFile() instead of addToLogFile() (https://github.com/kaltura/server/pull/6100)
- PLAT-7961: Refactor sFTP distribution engine (https://github.com/kaltura/server/pull/6094)
- PLAT-8038: Support flavor asset update without updating source content (https://github.com/kaltura/server/pull/6087)
- PLAT-8030: Recording 24 By 7 feature flip (https://github.com/kaltura/server/pull/6085)
- PLAT-7988: Add caption support for webvtt format on clip/trim (https://github.com/kaltura/server/pull/6037)
- PLAT-7906: Add php7 support for accessing sftp urls (https://github.com/kaltura/server/pull/5937)

* Mon Sep 25 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.4.0-1
- Ver Bounce to 13.4.0

* Sun Sep 24 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.3.0-16
- PLAT-8067: Use impersonated partnerId if one exists (https://github.com/kaltura/server/pull/6091)
- googleoauth action fix save timezone (https://github.com/kaltura/server/pull/6080)
- PLAT-7978: Set the original entry as the root of the cloned entry (https://github.com/kaltura/server/pull/6075)
- Don't send empty strings + cache.ini fix (https://github.com/kaltura/server/pull/6074)
- Avoid fatal error when returning header that contains multiple ':' chars (https://github.com/kaltura/server/pull/6073)
- PLAT-7987: Support beacon add via api layer (https://github.com/kaltura/server/pull/6070)
- playManifest beacon - improve clientTag parsing (https://github.com/kaltura/server/pull/6068)
- Change type of KalturaOptionalAnswersArray (https://github.com/kaltura/server/pull/6066)
- PLAT-8023: Fix mismatch on enc-at-rest replacement (https://github.com/kaltura/server/pull/6064)
- SUP-11906: Invalidate query cache before fetching entryServerNode list (https://github.com/kaltura/server/pull/6061)
- Recorded entry should always get the live conversion profile id from the live entry (https://github.com/kaltura/server/pull/6058)
- Enhance search support sorting (https://github.com/kaltura/server/pull/6055)
- PLAT-7985: Avoid adding user entry for empty userId (https://github.com/kaltura/server/pull/6049)
- PLAT-7999: Fix the media type validation in the mediaService get action (https://github.com/kaltura/server/pull/6048)
- playManifest - allow overriding of playbackType (https://github.com/kaltura/server/pull/6047)
- PLAT-7978: Add copyRootEntryId option to baseEntry clone action (https://github.com/kaltura/server/pull/6045)
- PHP Strict Standards (https://github.com/kaltura/server/pull/6044)
- PLAT-7975: Add valid check for partner when getting drop folder to watch (https://github.com/kaltura/server/pull/6041)
- KMS-15029: Support trimming of quiz entries (https://github.com/kaltura/server/pull/6040)
- PLAT-7917- new CHUNKED_ENCODE_JOB_SCHEDULER job (https://github.com/kaltura/server/pull/6039)
- SUP-12047: Cross Kaltura connector retries endlessly due to deleted cuepoint (https://github.com/kaltura/server/pull/6036)
- Remove code for aborting file sync import jobs (https://github.com/kaltura/server/pull/6035)
- PLAT-7943: Support setting flavor language and label via xml bulk upload (https://github.com/kaltura/server/pull/6026)
- PLAT-7952: Add user login by ks action allow change account operation (https://github.com/kaltura/server/pull/6020)
- should match Infra_AuthAdapter::getUserIdentity()'s signature (https://github.com/kaltura/server/pull/6017)

* Mon Sep 11 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.3.0-1
- Ver Bounce to 13.3.0

* Mon Sep 11 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.2.0-31
- Preview and Embed: do not encode entry names (https://github.com/kaltura/server/pull/6031)
- PLAT-7969: fix ical bulk ingestion to handle [duration] field input (https://github.com/kaltura/server/pull/6019)
- PLAT-7971: Clip of entry not in ready state fails (https://github.com/kaltura/server/pull/6018)
- Admin Console UI: fix input type for password (https://github.com/kaltura/server/pull/6016)
- SUP-11944: add retry when download part of the file (https://github.com/kaltura/server/pull/6009)
- PLAT-7953: Audio upload fix to add the stream language correctly (https://github.com/kaltura/server/pull/6006)
- add ascii folding to kaltura_keyword (https://github.com/kaltura/server/pull/6002)
- PLAT-7945: Allow deleting live + recorded entries for which the recording flow is stuck for more the 7 days (https://github.com/kaltura/server/pull/5997)
- PLAT-7827: add entry server node recording status (https://github.com/kaltura/server/pull/5994)
- PLAT-7818: handling language and label copy when replacing entry (https://github.com/kaltura/server/pull/5991)
- PLAT-7894: Add new delivery profile type for serving vod HLS manifest directly from packager (https://github.com/kaltura/server/pull/5988)
- PLAT-7889: When clipping and trimming, add caption files from the original entry onto the new one (https://github.com/kaltura/server/pull/5983)
- plat-7942: Add a playManifest param to disable the returning of captions (https://github.com/kaltura/server/pull/5979)
- PLAT-7928: Added retrieveVolumeLevels() (https://github.com/kaltura/server/pull/5976)
- PLAT-7939: Prevent adding user entry without user id + prevent changing entryId on existing user entry object (https://github.com/kaltura/server/pull/5975)
- PLAT-7933: Extend language support in ISO 639 (https://github.com/kaltura/server/pull/5973)
- PLAT-7854: Align bigint db fields to API objects and services (https://github.com/kaltura/server/pull/5971)


* Tue Aug 15 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.2.0-1
- Ver Bounce to 13.2.0

* Tue Aug 15 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.1.0-17
- In older versions, the 'kaltura' user did not have ALTER priviliges on the kaltura_sphinx_log DB. Added %post action to correct this.

* Fri Aug 11 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.1.0-13
- serveFlavor replace path only when pathOnly is set (https://github.com/kaltura/server/pull/5917)
- PLAT-7863: If new file download attempt failed unlink local file created (https://github.com/kaltura/server/pull/5914)
- ElasticSearch modifcations (https://github.com/kaltura/server/pull/5912)
- add default value to type in retrieveByLastId (https://github.com/kaltura/server/pull/5911)
- support path prefix replacement in serveFlavor (https://github.com/kaltura/server/pull/5909)
- Update kMetadataManager.php (https://github.com/kaltura/server/pull/5907)
- Avoid PHP Fatal error in case getSingleLayerCache did return cache object (https://github.com/kaltura/server/pull/5906)
- add delete from elastic index (https://github.com/kaltura/server/pull/5905)
- PLAT-7863: Move validation of invalid import URL after the file download attempt to avoid failing request to domains that block head request (https://github.com/kaltura/server/pull/5902)
- Fix category full name indexing (https://github.com/kaltura/server/pull/5901)
- Specify on alias actions what plugins they come from (https://github.com/kaltura/server/pull/5899)
- add the unlockJobsByScheduler script (https://github.com/kaltura/server/pull/5897)
- apiGrep - add support for --match-any (https://github.com/kaltura/server/pull/5895)
- add flag for disabling events (https://github.com/kaltura/server/pull/5894)
- optimize grepping of gzip files (https://github.com/kaltura/server/pull/5892)
- PLAT-7836: Add copy from template entry for live stream entries (https://github.com/kaltura/server/pull/5891)
- add script for grepping api logs (https://github.com/kaltura/server/pull/5889)
- SUP-11537: Allow uploading of MO files in restriction mode. (https://github.com/kaltura/server/pull/5888)
- PLAT-7837: prevent user-entry duplicate only on history context (https://github.com/kaltura/server/pull/5887)
- ElasticSearch (https://github.com/kaltura/server/pull/5885)
- SUP-11599 - Fix non-integer width case (https://github.com/kaltura/server/pull/5883)
- Use standart error when filter is not provided correctly + minor code changes (https://github.com/kaltura/server/pull/5871)
- PLAT-7822: indexIdGreaterThan should refer to the entry int_id in case of entry (https://github.com/kaltura/server/pull/5869)
- PLAT-7821: When fetching multiple entrries need to reset deliveryAttributes between entry iterations (https://github.com/kaltura/server/pull/5867)
- PLAT7813: use playlist version when creating thumbnail (https://github.com/kaltura/server/pull/5864)

* Mon Jul 31 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.1.0-1
- Ver Bounce to 13.1.0

* Sun Jul 30 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.0.0-15
- Nightly build.

* Sat Jul 29 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.0.0-14
- Nightly build.

* Fri Jul 28 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.0.0-13
- Nightly build.

* Fri Jul 28 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.0.0-12
- PLAT-7823 - add params validation and partner filters to userEntry filter (https://github.com/kaltura/server/pull/5870)
- SUP-11599 - new AR mode (https://github.com/kaltura/server/pull/5868)
- SUPPS-1191 - Serve Flavor DC Redirect Fix (https://github.com/kaltura/server/pull/5865)
- SUPPS-1191 - Serve Flavor DC Redirect Fix (https://github.com/kaltura/server/pull/5863)
- caption fixes (https://github.com/kaltura/server/pull/5861)
- PLAT-7810 - Entry appears multiple times in history page (https://github.com/kaltura/server/pull/5859)
- KMS-14633 - modify metaData delete action. (https://github.com/kaltura/server/pull/5858)
- SUP-9349 - unescape parameters that were escaped in Flex KMC and passed via ExternalInterface (https://github.com/kaltura/server/pull/5857)
- PLAT-7804 - verify that the resource file type is text (https://github.com/kaltura/server/pull/5856)
- PS-3201 - When making a playmanifest request with a minBitrate that is higher than the available bitrates, all flavours should be returned (https://github.com/kaltura/server/pull/5852)
- PLAT-7801 - New 'virtual' Chunked-FFmpeg transcoder type (https://github.com/kaltura/server/pull/5851)
- SUP-11614 - embedIframeJsAction should pass referrer when dumping request to avoid ACL not passing validation (https://github.com/kaltura/server/pull/5850)
- Set MRSS timeout (https://github.com/kaltura/server/pull/5849)
- PLAT-7796 - Resolve PHP Fatal error: Call to undefined method LiveStreamEntry::getPushPublishConfigurations when pushPublish flag enabled on entry (https://github.com/kaltura/server/pull/5845)
- PLAT-7571 -  Add support for Thumbnail Stripes (https://github.com/kaltura/server/pull/5841)
- Add play_manifest_cache_age kconf param (https://github.com/kaltura/server/pull/5838)
- PLAT-7663: shouldn't use recorderLengthInMsecs if entry is no longer served from live (https://github.com/kaltura/server/pull/5837)
- Add sender header to MR mail (https://github.com/kaltura/server/pull/5836)
- Add serve thumbnail with thumbnail api with flavor_params_id parameter (https://github.com/kaltura/server/pull/5833)
- SUP-11336: Correctly sync entitlement info between parent and child entries (https://github.com/kaltura/server/pull/5832)
- PLAT-7754: Add support for distributing all entry thumbnails + Resolve bugs in K2K distribution flow (https://github.com/kaltura/server/pull/5830)
- Check response code from curl request (https://github.com/kaltura/server/pull/5829)
- Sequence in dash and hls only (https://github.com/kaltura/server/pull/5827)
- PS-3180 - playmanifest - adding minimum bit-rate limit parameter (https://github.com/kaltura/server/pull/5826)
- Check for type in media->get() (https://github.com/kaltura/server/pull/5824)
- PLAT-7669: add addContent action to the Data service (https://github.com/kaltura/server/pull/5814)

* Tue Jul 18 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.0.0-1
- Ver Bounce to 13.0.0

* Mon Jul 17 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.20.0-22
- PLAT-7741: additional filters shouldn't be used with filter (https://github.com/kaltura/server/pull/5816)
- PLAT-7725: Deploy live packager delivery profiles to support new live playback (https://github.com/kaltura/server/pull/5809)
- PLAT-7737: when generating target client send partnerId to login to solve error when same user id exists multiple partner ids (https://github.com/kaltura/server/pull/5807)
- Fix monitoring (https://github.com/kaltura/server/pull/5804)
- Coherent exception message if the kalturadw DB cannot be reached (https://github.com/kaltura/server/pull/5803)
- SUP-10803-arf-to-wmv inter-source files (https://github.com/kaltura/server/pull/5802)
- PLAT-7483: make sure flavour exists  (https://github.com/kaltura/server/pull/5799)
- add privilege to spesific entryIds (https://github.com/kaltura/server/pull/5798)
- PLAT-7682: need to add insert permission for kalturathumbcuepoint (https://github.com/kaltura/server/pull/5797)
- PLAT-7483: should use origEntry instead of reference for serverUrl (https://github.com/kaltura/server/pull/5796)
- PLAT-7635: Update not triggered when replacing timed thumb asset associated with cue point (https://github.com/kaltura/server/pull/5795)
- add referenceId to the entry updateable fields list (https://github.com/kaltura/server/pull/5792)
- SUP-11032: fail process for unsupported file types (https://github.com/kaltura/server/pull/5791)
- PLAT-7682: allow capture space to add cue points and thumb assets (https://github.com/kaltura/server/pull/5788)
- add DigitalElement geocoder (https://github.com/kaltura/server/pull/5787)
- add bypass to user filter in the cue point service (https://github.com/kaltura/server/pull/5784)
- Increment recorded entry index only in case new recorded entry id is defined and is different from current one (https://github.com/kaltura/server/pull/5783)
- Add lastFileTimestamp to DF configuration (https://github.com/kaltura/server/pull/5781)
- PLAT-7714: when setting recorded content fetch assets in deleted status as well in case someone changed conversion profile id (https://github.com/kaltura/server/pull/5780)
- PLAT-7708: Refactor drop folder watcher to avoid multi scanning of same file (https://github.com/kaltura/server/pull/5778)
- Change file name to template and add check of exist (https://github.com/kaltura/server/pull/5777)
- PLAT-7316: kObjectDeleteHandler::objectDeleted is called twice any time an object is deleted (https://github.com/kaltura/server/pull/5775)
- PLAT-7676 (https://github.com/kaltura/server/pull/5773)
- PLAT-7675 (https://github.com/kaltura/server/pull/5771)

* Tue Jul 4 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.20.0-1
- Ver Bounce to 12.20.0

* Mon Jul 3 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.19.0-15
- Update kViewHistoryUserEntryAdvancedFilter.php (https://github.com/kaltura/server/pull/5762)
- PLAT-7483: put language and label in correct place (https://github.com/kaltura/server/pull/5760)
- Override filter limit from advanced filter (https://github.com/kaltura/server/pull/5756)
- syndication feed - cue-points ordering by created_at (https://github.com/kaltura/server/pull/5745)
- DropFolder: add order by to list (https://github.com/kaltura/server/pull/5735)
- Source flavour can only be ingested, not generated (https://github.com/kaltura/server/pull/5734)
- PLAT-7639: Avoid sync issue now that first sync point could be a few seconds into the video (https://github.com/kaltura/server/pull/5733)
- PLAT-7639: Recorded video is always missing last few seconds so when copying cue points make sure to include cue points added during that time (https://github.com/kaltura/server/pull/5732)
- PS-3159 - fix improper frame-rate assignment (https://github.com/kaltura/server/pull/5730)
- KALTURA_RECORDED_LIVE deleting validation should only be done when root entry id is of type live (https://github.com/kaltura/server/pull/5729)
- Fix PS2 XSSes (https://github.com/kaltura/server/pull/5728)
- PLAT-7565: allow the update of flavorAsset::label (https://github.com/kaltura/server/pull/5724)
- PLAT-7575 (https://github.com/kaltura/server/pull/5718)
- SUP-11306: handle ampersand chars in XML document" (https://github.com/kaltura/server/pull/5716)
- add stats->reportDeviceCapabilties action (https://github.com/kaltura/server/pull/5714)
- add reset of MR entry status when retention time changes (https://github.com/kaltura/server/pull/5713)
- PLAT-7504: refactore drop folder watcher for file transfer engine (https://github.com/kaltura/server/pull/5679)
- PLAT-7483: On-the-fly stitching of the bumper video (https://github.com/kaltura/server/pull/5669)
- PLAT-6734: getPlaybackContext fixes (https://github.com/kaltura/server/pull/5653)

* Tue Jun 20 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.19.0-1
- Ver Bounce to 12.19.0

* Mon Jun 19 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.18.0-18
- Minor fix - if found 0 user entries, should return empty result (https://github.com/kaltura/server/pull/5696)
- Default parameter assignment is not supported in IE (https://github.com/kaltura/server/pull/5690)
- Revert "Return Global parter only when specifically requested" (https://github.com/kaltura/server/pull/5688)
- Return Global parter only when specifically requested (https://github.com/kaltura/server/pull/5687)
- Allow partner zero impersonate (https://github.com/kaltura/server/pull/5686)
- Adding script for change drop folders tag (https://github.com/kaltura/server/pull/5685)
- Don't allow deletion while entry live (https://github.com/kaltura/server/pull/5680)
- 1. Remove privacy context from userEntry calculations (https://github.com/kaltura/server/pull/5678)
- PLAT-7471: add Access-Control-Expose-Headers (https://github.com/kaltura/server/pull/5675)
- fix drop folder file copy and add log to webex engine (https://github.com/kaltura/server/pull/5674)
- Lynx 12.18.0 plat 7531 (https://github.com/kaltura/server/pull/5673)
- PLAT-7518: Prevent deleting recorded entry while recorded content is not set (https://github.com/kaltura/server/pull/5672)
- missing enum from quiz plugin (https://github.com/kaltura/server/pull/5671)
- PLAT-7535: CE|On Prem - support new live packages + LC flow + webcast (https://github.com/kaltura/server/pull/5670)
- PLAT-7472: fix handling stripping html tags in youtube distribution (https://github.com/kaltura/server/pull/5668)
- PLAT-7386: modify entry (https://github.com/kaltura/server/pull/5667)
- save bundles in subdirectories and allow explicitly bundle regeneration (https://github.com/kaltura/server/pull/5666)
- If no user ID was passed, use current KS user ID (https://github.com/kaltura/server/pull/5665)
- PLAT-7485: Handle security issues in in-video-quiz (https://github.com/kaltura/server/pull/5664)
- preg_replace(): The /e modifier is no longer supported (https://github.com/kaltura/server/pull/5663)
- The /kmc alias is not only unnecessary but also triggers errors (https://github.com/kaltura/server/pull/5661)
- PLAT-7371: Support defining multiple parents pre server node (https://github.com/kaltura/server/pull/5659)
- hls compatibility features (https://github.com/kaltura/server/pull/5657)
- return the dry run batch job Id from the server (https://github.com/kaltura/server/pull/5656)
- SUP-10933:: when generating flavor asset URL disable parentEntry entity (https://github.com/kaltura/server/pull/5650)
- remove setting kuser when updating cue point (https://github.com/kaltura/server/pull/5649)
- PS-3112: don't delete existing cue points during update (https://github.com/kaltura/server/pull/5648)
- PLAT-7502: get vote implementation (https://github.com/kaltura/server/pull/5647)
- Update QuizUserEntry.php (https://github.com/kaltura/server/pull/5646)
- PLAT-7343 handle opera xslt with special characters in media:category(https://github.com/kaltura/server/pull/5645)
- PLAT-7482: Automaticity fail request that we failed to replaceMultiRequestResults (https://github.com/kaltura/server/pull/5644)
- PLAT-7499: When calculating push notifications hash use original ks object (https://github.com/kaltura/server/pull/5643)
- PLAT-7385: (https://github.com/kaltura/server/pull/5640)
- add move to category option in modify category engine (https://github.com/kaltura/server/pull/5639)
- change script delete process (https://github.com/kaltura/server/pull/5638)
- Updated version (https://github.com/kaltura/server/pull/5637)
- PlayKit player embed (https://github.com/kaltura/server/pull/5587)

* Mon Jun 5 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.18.0-1
- Ver Bounce to 12.18.0

* Mon Jun 5 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.18.0-1
- Ver Bounce to 12.18.0

* Mon Jun 5 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.18.00-1
- Ver Bounce to 12.18.00

* Mon Jun 5 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.17.0-20
- PLAT-7487: keepOriginalFile flag should be passed when ingesting per flavor asset as well (https://github.com/kaltura/server/pull/5631)
- handle use case where header value contains the ":" character (https://github.com/kaltura/server/pull/5630)
- remove notification from  template name (delete) (https://github.com/kaltura/server/pull/5625)
- PLAT-7333 disable cache for service (https://github.com/kaltura/server/pull/5622)
- qnd: When creating poll ids need to disable cache (https://github.com/kaltura/server/pull/5621)
- PLAT-7288 support keep https (https://github.com/kaltura/server/pull/5620)
- PS-3058: syndication feed - add capabilities (https://github.com/kaltura/server/pull/5619)
- do not update metadata when deleting entry (https://github.com/kaltura/server/pull/5618)
- PLAT-7436: check directory existance (https://github.com/kaltura/server/pull/5617)
- PS-3067+8 (https://github.com/kaltura/server/pull/5616)
- Lynx 12.15.0 plat 7333 (https://github.com/kaltura/server/pull/5614)
- SUP-11188: Validate permission only if property is being changed (https://github.com/kaltura/server/pull/5613)
- add check for not null, change button placement (https://github.com/kaltura/server/pull/5612)
- PLAT-7343 - update opera xslt (https://github.com/kaltura/server/pull/5611)
- In case of conflict validation , add SchedulerEventId to ignore (https://github.com/kaltura/server/pull/5608)
- Avoid php notice if the remove address does not exist (https://github.com/kaltura/server/pull/5607)
- conversion prof xslt - use congigured shared folder path (https://github.com/kaltura/server/pull/5606)
- get intval of partner_id and from/to dates params to prevent sql injection (https://github.com/kaltura/server/pull/5604)
- view history - check profile existance (https://github.com/kaltura/server/pull/5603)
- update release notes (https://github.com/kaltura/server/pull/5599)
- PLAT-7460 - reindex schedule event when deleting schedule_event_resource (https://github.com/kaltura/server/pull/5598)
- Improved evaluateConcurrency func (https://github.com/kaltura/server/pull/5595)
- Update PollService.php (https://github.com/kaltura/server/pull/5594)
- Update PollService.php (https://github.com/kaltura/server/pull/5592)
- Update PollService.php (https://github.com/kaltura/server/pull/5591)
- Added helper PendingChunksCount function (https://github.com/kaltura/server/pull/5590)
- Update PollService.php (https://github.com/kaltura/server/pull/5589)
- PLAT-7343 - fixed syndication feed roku and opera xslt to hold CDATA (https://github.com/kaltura/server/pull/5588)
- allow player do userEntry->update (https://github.com/kaltura/server/pull/5586)
- PLAT-3761: Support deploying system profile used by Kaltura webcast application (https://github.com/kaltura/server/pull/5584)
- Lynx 12.16.0 ps 3045 (https://github.com/kaltura/server/pull/5583)
- PLAT-7384: Enforce ACL limitFlavors action on live streams as well (https://github.com/kaltura/server/pull/5582)
- As of PHP 5.4.0, removed call-time pass-by-refer (https://github.com/kaltura/server/pull/5581)
- move the copy template MD to MD object (https://github.com/kaltura/server/pull/5579)
- Lynx 12.16.0 plat 7429 mr validate filter (https://github.com/kaltura/server/pull/5578)
- Updated version (https://github.com/kaltura/server/pull/5577)
- PLAT-7445: minor fix (https://github.com/kaltura/server/pull/5575)
- Lynx 12.15.0 plat 7333 (https://github.com/kaltura/server/pull/5574)
- Sort by user entry order (https://github.com/kaltura/server/pull/5573)
- PLAT-7407: cross kaltura connector doesn't distribute ThumbCuePoints correctly (https://github.com/kaltura/server/pull/5566)

* Mon May 22 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.17.0-1
- Ver Bounce to 12.17.0

* Sun May 21 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.16.0-16
- Nightly build.

* Sun May 21 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.16.0-15
- Final 12.16.0 build

* Thu May 18 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.16.0-10
- Update ScheduledTaskPlugin.php (https://github.com/kaltura/server/pull/5565)
- insert creating date into the loop (https://github.com/kaltura/server/pull/5564)
- Add permission script (https://github.com/kaltura/server/pull/5562)
- Lynx 12.16.0 plat 6960 increase time out (https://github.com/kaltura/server/pull/5561)
- Add missing function to delivery profile (https://github.com/kaltura/server/pull/5560)
- PLAT-6960: add validation on numbers (https://github.com/kaltura/server/pull/5557)
- PLAT-7022 PLAT-7344 - Roku and Opera syndication feed xslt modification (https://github.com/kaltura/server/pull/5556)
- PLAT 6960: modify GUI - 1 (https://github.com/kaltura/server/pull/5555)
- SUP-10928: add a check for null puser_id (https://github.com/kaltura/server/pull/5554)
- Add scheduleEvent->list optimization (https://github.com/kaltura/server/pull/5552)
- Apply URANDOM to PlayReady form as it slow down the add/configure (https://github.com/kaltura/server/pull/5551)
- increase Drop folder ttl in cache for 15 minutes (https://github.com/kaltura/server/pull/5550)
- PLAT-7381 : sanitize html tags from title and tags as well in youtube (https://github.com/kaltura/server/pull/5549)
- Add sending mail to admin when profile suspended (https://github.com/kaltura/server/pull/5548)
- PLAT-7378: fix get conflicts to retrive events with recurrence type of a single  (https://github.com/kaltura/server/pull/5546)
- PLAT-7373: If flavor params id not found on live entry throw exception (https://github.com/kaltura/server/pull/5545)
- SUP-10970: getId => getFlavorParamsId (https://github.com/kaltura/server/pull/5543)
- Add support for insert absolute dates (https://github.com/kaltura/server/pull/5542)
- Fix issue when getting conflicts to get only the active events (https://github.com/kaltura/server/pull/5536)
- SUP-10970: filter temprorary entries from event notifications (https://github.com/kaltura/server/pull/5535)
- PLAT-7365: set maxConcurrency (https://github.com/kaltura/server/pull/5533)
- PLAT-7365: fix required bootstrap cmd (https://github.com/kaltura/server/pull/5532)
- PLAT-7365: fix min concurrency default (https://github.com/kaltura/server/pull/5531)
- Check if folder exists before calling freeExclusiveDropFolder() (https://github.com/kaltura/server/pull/5530)
- Syndication feed - add external media duration value (https://github.com/kaltura/server/pull/5529)
- PLAT-7244: Support live stream recording of each individual flavor (https://github.com/kaltura/server/pull/5527)
- PLAT-7365: chunked encoding (https://github.com/kaltura/server/pull/5526)
- PLAT-7256: fix youtube distribution on update (https://github.com/kaltura/server/pull/5525)
- Fix cloning filter array before insert extra data (https://github.com/kaltura/server/pull/5524)
- SUPPS-1126 (https://github.com/kaltura/server/pull/5523)
- TR-1205: add whitelisted parameters (https://github.com/kaltura/server/pull/5522)
- PLAT-7281: ViewHistory feature (https://github.com/kaltura/server/pull/5521)
- Moderation status - make 'deleted' external (https://github.com/kaltura/server/pull/5518)
- PLAT-7357: Return kMultiCast location based on the request format (https://github.com/kaltura/server/pull/5517)
- Anonymous IP ACL (https://github.com/kaltura/server/pull/5515)
- Ignore entitlement fields in ranker (https://github.com/kaltura/server/pull/5514)
- Add bin_path_ffprobe to local.template.ini (https://github.com/kaltura/server/pull/5508)
- PLAT-7301 support response profile in schedule events getConflicts (https://github.com/kaltura/server/pull/5480)
- PLAT-7294 playback context handling recorded-live entries (https://github.com/kaltura/server/pull/5473)

* Tue May 9 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.16.0-1
- Ver Bounce to 12.16.0

* Sun May 7 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.15.0-17
- Nightly build.

* Sun May 7 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.15.0-16
- PLAT-7251: handle script exception (https://github.com/kaltura/server/pull/5507)
- Update KAsyncDropFolderWatcher.class.php (https://github.com/kaltura/server/pull/5506)
- PLAT-7251: fix script and typo (https://github.com/kaltura/server/pull/5504)
- service names are always kaltura-$DAEMON_NAME, not kaltura_$DAEMON_NAME (https://github.com/kaltura/server/pull/5503)
- PLAT-7251: add comment (https://github.com/kaltura/server/pull/5502)
- PLAT-7332: allow specific partnerPackages to be inserted without KS (https://github.com/kaltura/server/pull/5501)
- PLAT-7277: verify "/v" in path before splitting to get version (https://github.com/kaltura/server/pull/5499)
- Add missing sharedTempPath to batch template file (https://github.com/kaltura/server/pull/5498)
- add error to metadata when can not process task on entry (https://github.com/kaltura/server/pull/5497)
- add try catch when try to updata metadata for delete entry (https://github.com/kaltura/server/pull/5496)
- prevent creation of duplicate kuser when the puser is long (https://github.com/kaltura/server/pull/5495)
- Lynx 12.15.0 plat 7300 (https://github.com/kaltura/server/pull/5494)
- PLAT-7318: if no profile configured for partner we should take default (https://github.com/kaltura/server/pull/5493)
- PLAT-7317-FIX channels_layout in ffmpeg cmdLine (https://github.com/kaltura/server/pull/5491)
- PLAT-7317-FIX channels_layout in ffmpeg cmdLine (https://github.com/kaltura/server/pull/5490)
- PLAT-7003-FIX-WM-for-true-portrait-sources (https://github.com/kaltura/server/pull/5489)
- PS-3018: syndicationFeed - get entry type as dynamic enum (https://github.com/kaltura/server/pull/5488)
- PS-3015+6: syndicationFeed - if no more entries don't add link (https://github.com/kaltura/server/pull/5487)
- PLAT-7313: syndicationFeed - check entryFilter existance (https://github.com/kaltura/server/pull/5486)
- PS-3017: syndicationFeed - no ampersand escaping (https://github.com/kaltura/server/pull/5485)
- add check for MR metadata profile request (https://github.com/kaltura/server/pull/5483)
- PLAT-7238: small fix (https://github.com/kaltura/server/pull/5482)
- add metadataProfileId for MR (https://github.com/kaltura/server/pull/5481)
- PLAT-7251: remove broadcast urls from custom data (https://github.com/kaltura/server/pull/5478)
- in case a filename filter was passed enforce a statusIn filter in order to limit slow db queries (https://github.com/kaltura/server/pull/5475)
- PS-2993: syndication-feed - enable relative-time filter (https://github.com/kaltura/server/pull/5474)
- fix permission and impersonate for admin partner (https://github.com/kaltura/server/pull/5472)
- First version of Media Repurposing (https://github.com/kaltura/server/pull/5471)
- PLAT-7254 fix missing flavor params id for live entries (https://github.com/kaltura/server/pull/5470)
- Don't deploy KDP players to partner 99 (https://github.com/kaltura/server/pull/5469)
- Remove flix and mencoder trans engines in flavour creation. (https://github.com/kaltura/server/pull/5468)
- PLAT-7299: change core object of KalturaGenericSyndication feed to be genericSyndicationFeed (https://github.com/kaltura/server/pull/5467)

* Mon Apr 24 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.15.0-1
- Ver Bounce to 12.15.0

* Mon Apr 24 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.14.0-31
- add missing conn took variable (https://github.com/kaltura/server/pull/5459)
- use 'apphome_url_no_protocol' instead of 'cdn_api_host_https' (https://github.com/kaltura/server/pull/5458)
- PLAT-7022: fix NOTICE of undefined XSTL (https://github.com/kaltura/server/pull/5456)
- PLAT-7238: add ability for hash algorithm in updateclients to be requested dynamically and cache the results of the hash (https://github.com/kaltura/server/pull/5455)
- PLAT-7253:should be uploadToken instead of appToken (https://github.com/kaltura/server/pull/5451)
- PLAT-7253:add script file (https://github.com/kaltura/server/pull/5448)
- PLAT-7253: add permission for appToken->get to capture devices (https://github.com/kaltura/server/pull/5447)
- Add sessionRequired attribute the generated XML (https://github.com/kaltura/server/pull/5440)
- TR-1860 (https://github.com/kaltura/server/pull/5438)
- SUP-10845: fix delivery profile ids will be set to none if during storage profile update they are not given (https://github.com/kaltura/server/pull/5437)
- Lynx 12.14.0 plat 7178 support eac3 audio generation  (https://github.com/kaltura/server/pull/5435)
- PLAT-7245: downloadUrl should return playmanifest urls instead of the ps2 raw action (https://github.com/kaltura/server/pull/5433)
- PLAT-7234: enable opera and roku syndication feeds xslt to escape XML chars (https://github.com/kaltura/server/pull/5432)
- syndication federated search - remove entry status earlier (https://github.com/kaltura/server/pull/5431)
- disable IRelatedObject on DropFolder and DropFolderFile derived objects (https://github.com/kaltura/server/pull/5430)
- remove redundant logging (https://github.com/kaltura/server/pull/5427)
- add more params to log (https://github.com/kaltura/server/pull/5426)
- add logging to resposne profile couchbase caching (https://github.com/kaltura/server/pull/5425)
- PLAT-7150:construct shouldn't change things in custom_data since it could be before hidration (https://github.com/kaltura/server/pull/5424)
- track repetitive udpates of the same object (https://github.com/kaltura/server/pull/5423)
- PLAT-7240: Prevent deleting live entry while recording flow still running (https://github.com/kaltura/server/pull/5422)
- PLAT-7169:add update event notification script and enable event notifications (https://github.com/kaltura/server/pull/5421)
- PLAT-7194: attachments - enable download using playmanifest (https://github.com/kaltura/server/pull/5420)
- PLAT-7216: allow capture device permission to add/update/list scheduleEvent and scheduleResource (https://github.com/kaltura/server/pull/5419)
- PLAT-7217: add plugin interface && missing fields (https://github.com/kaltura/server/pull/5416)
- PLAT-7150: Adding Roku and Opera syndication feeds to KMC (https://github.com/kaltura/server/pull/5413)
- PLAT-7150: fix for getfeed and new XSLT (https://github.com/kaltura/server/pull/5411)
- PLAT-7194: playmanifest attachement download/url - check asset existance (https://github.com/kaltura/server/pull/5410)
- PLAT-5816: remove eventid from schedule event resource when the schedule event (https://github.com/kaltura/server/pull/5409)
- PLAT-7220: Dont allow adding liveEntries with recording enabled unless recording feature is enabled on the account (https://github.com/kaltura/server/pull/5402)
- PLAT-7218: Support filtering by idIn & idEqual in KalturaAssetParams.. (https://github.com/kaltura/server/pull/5398)
- SUP-10721: In case of text/html file import , ignore size checking  (https://github.com/kaltura/server/pull/5396)
- PLAT-7167: allow only admin_console to insert and update parent-partner-id and artner-package (https://github.com/kaltura/server/pull/5392)
- PLAT-6809: set duration of live recording while recording is still being done (https://github.com/kaltura/server/pull/5391)
- PLAT-7128: Prevent the ability to delete live stream entry while its still streaming (https://github.com/kaltura/server/pull/5389)
- PLAT-7142: ad stitching player awareness patches (https://github.com/kaltura/server/pull/5385)
- PLAT-7194: playmanifest action - enable all asset types download (https://github.com/kaltura/server/pull/5384)
- SUP-10236: merge users with multiple kusers for the same puser by giving a partner (https://github.com/kaltura/server/pull/5383)
- PLAT-7192: allow setting keepOriginalFile when using KalturaServerFile (https://github.com/kaltura/server/pull/5381)

* Mon Mar 27 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.14.0-1
- Ver Bounce to 12.14.0

* Sun Mar 26 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.13.0-9
- PLAT-6942 - Clipped entry offset and duration are not retuned by Kaltura API 
- PLAT-7135 - Drop folder watcher not getting folders 
- PLAT-7163 - Race between old and new recording causes wrong call to cancelReplace
- PLAT-7163 - Add media-server permission get permission

* Tue Mar 14 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.13.0-1
- Ver Bounce to 12.13.0

* Thu Mar 9 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.12.0-8
- PLAT-6916 - Add batch thumbasset delete permission
- PLAT-6663 - User KS allow specific permission to approveReplace
- PLAT-6933 - stored XSS in preview action (KMC)
- PLAT-6934 - reflected XSS in clientTest.php
- PLAT-6935 - reflected XSS in modules/kmc/templates/reportsSuccess.php
- PLAT-6936 - reflected XSS in modules/system/templates/loginSuccess.php
- PLAT-6937 - reflected XSS in kmcEmbed action
- PLAT-6938 - PHP File Inclusion vulnerability in defPartnerservices2baseAction.class.php
- PLAT-6952 - BaseEntry.clone gets error 500 Internal server error occurred
- PLAT-6663 - Trimming or clipping on parent entry should also happen to child entries

* Tue Feb 28 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.12.0-1
- Ver Bounce to 12.12.0

* Fri Feb 23 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.11.0-9
- PLAT-6888 - Push notification redesig + caching optiization
- PLAT-6944 - Drop folder Optimization
- PLAT-6786 - Conditional conversion porfiles
- PLAT-6786 - Preserve Source Key Frames
- PLAT-6663 - Trimming or clipping on parent entry should also happen to child entries
- PLAT-6855 - kMatchMetadataCondition should return false for irrelevant metadata objects

* Mon Feb 13 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.11.0-1
- Ver Bounce to 12.11.0

* Mon Feb 13 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.10.0-5
- SUP-9415 - Comment Limit
- SUP-9904 - Specific size of thumbnails calls for the original one and not the replacement that was uploaded
- SUP-10147 - V18- Custom metadata fields are not distributed when null via KMC
- SUP-9826 - Google Drive Integration
- SUP-10043 - KMS user list does not match the one in the KMC or the API list
- PLAT-6663 - Trimming or clipping on parent entry should also happen to child entries
- PLAT-6783 - Batch service keeps respawning
- PLAT-6679 - partner->register allows for new accounts to be created even if email already exists, without validating password or KS

* Tue Jan 31 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.10.0-1
- Ver Bounce to 12.10.0

* Sun Jan 29 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.9.0-18
- SUP-9380 - Live Manifest delivered over http
- SUP-8904 - flavorAsset -> getDownloadURL provides broken links when there are special characters in the entry name such as %
- SUP-9879 - Generate thumbnail error when uploading short video - 3 seconds
- PLAT-6662 - Entry Deep clone - clone childs
- PLAT-5707 - optimize the thumbnail grabbing
- PLAT-6503 - Add ability to sanitize/block/notify/ignore on a closed list of object attributes

* Mon Jan 9 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.9.0-1
- Ver Bounce to 12.9.0

* Fri Jan 6 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.8.0-10
- PLAT-6650 - New X265/HEVC support
- PLAT-5801 - Design batch optimiztion
- PLAT-6543 - Scheduling - validate resourceEvent is not already allocated at a specific time
- PLAT-6666 - When changing entry UserId change the owner also on the childs.
- PLAT-6668 - When changing entry.entitledUsersEdit/Publish, make the same changes on the child entries
- PLAT-6708 - At rest encryption fails with transcoding operators

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

