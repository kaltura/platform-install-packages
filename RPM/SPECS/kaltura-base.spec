%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define apache_user	apache
%define apache_group	apache
%define prefix /opt/kaltura
%define confdir %{prefix}/app/configurations
%define logdir %{prefix}/log
%define webdir %{prefix}/web
%define codename Quasar

Summary: Kaltura Open Source Video Platform 
Name: kaltura-base
Version: 17.17.0
Release: 3
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
Source35: start_page.php 
Source36: start_page_survey.png
Source37: start_page_newsletter.png
Source38: start_page-landing-page.css
Source39: CrossKalturaDistributionEngine.php 
Source40: KalturaCrossKalturaDistributionProfile.php 
Source41: CrossKalturaProfileConfiguration.php 
Source42: KalturaCrossKalturaDistributionJobProviderData.php 
Source43: CrossKalturaDistributionCustomDataField.php 
Source44: kCrossKalturaDistributionJobProviderData.php 
Source45: CrossKalturaDistributionProfile.php
Source46: CrossKalturaDistributionPlugin.php
Source47: CrossKalturaEntryObjectsContainer.php
Source48: php.yml

URL: https://github.com/kaltura/server/tree/%{codename}-%{version}
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: rsync,mysql,kaltura-monit,kaltura-postinst,cronie, php-cli, php-xml, php-curl, php-mysqli, php-pdo_mysql, php-gd, php-gmp, php-ldap, php-mbstring, php-process, chrony, mailx

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
mkdir -p $RPM_BUILD_ROOT%{prefix}/apps/clientlibs
mkdir -p $RPM_BUILD_ROOT%{logdir}
mkdir -p $RPM_BUILD_ROOT%{prefix}/var/run
mkdir -p $RPM_BUILD_ROOT%{prefix}/tmp
mkdir -p $RPM_BUILD_ROOT%{webdir}
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

mkdir -p $RPM_BUILD_ROOT%{webdir}/tmp
mkdir -p $RPM_BUILD_ROOT%{webdir}/tmp/imports
mkdir -p $RPM_BUILD_ROOT%{webdir}/tmp/convert
mkdir -p $RPM_BUILD_ROOT%{webdir}/tmp/thumb
mkdir -p $RPM_BUILD_ROOT%{webdir}/tmp/xml
mkdir -p $RPM_BUILD_ROOT%{webdir}/dropfolders/monitor
mkdir -p $RPM_BUILD_ROOT%{webdir}/control
mkdir -p $RPM_BUILD_ROOT%{webdir}/content/cacheswf
mkdir -p $RPM_BUILD_ROOT%{webdir}/content/uploads
mkdir -p $RPM_BUILD_ROOT%{webdir}/content/entry
mkdir -p $RPM_BUILD_ROOT%{webdir}/tmp/dropFolderFiles
mkdir -p $RPM_BUILD_ROOT%{prefix}web/content//metadata
mkdir -p $RPM_BUILD_ROOT%{webdir}/content/batchfiles
mkdir -p $RPM_BUILD_ROOT%{webdir}/content/templates



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


sed -i 's@^IsmIndex@;IsmIndex@g' $RPM_BUILD_ROOT%{confdir}/plugins.template.ini
sed -i 's#^;ElasticSearch#ElasticSearch#g' $RPM_BUILD_ROOT%{confdir}/plugins.template.ini
sed -i "s#^;kmc_version = @KMC_VERSION@#kmc_version = %{_kmc_version}#g" $RPM_BUILD_ROOT%{confdir}/local.template.ini
sed -i 's#@KMCNG_VERSION@#%{_kmcng_version}#' $RPM_BUILD_ROOT%{confdir}/local.template.ini
sed -i 's@^otp_required_partners\[\]@;otp_required_partners\[\]@g' $RPM_BUILD_ROOT%{confdir}/local.template.ini
sed -i "s@^partner_otp_internal_ips@;partner_otp_internal_ips@g" $RPM_BUILD_ROOT%{confdir}/local.template.ini
# when this directive is set, `report` requests go to KAVA
sed -i "s@^\(druid_url.*$\)@;\1@g" $RPM_BUILD_ROOT%{confdir}/local.template.ini
sed -i "s#@HTML5LIB_VERSION@#%{html5_version}#g" $RPM_BUILD_ROOT%{confdir}/appVersions.template.ini
sed -i "s#@STUDIO_VERSION@#%{studio_2_version}#g" $RPM_BUILD_ROOT%{confdir}/appVersions.template.ini
sed -i "s#@STUDIO3_VERSION@#%{studio_3_version}#g" $RPM_BUILD_ROOT%{confdir}/appVersions.template.ini
sed -i 's#<html5Url>/html5/html5lib/v.*/mwEmbedLoader.php</html5Url>#<html5Url>/html5/html5lib/%{html5_version}/mwEmbedLoader.php</html5Url>#g' $RPM_BUILD_ROOT%{prefix}/app/deployment/base/scripts/init_content/01.uiConf.99.template.xml
sed -i "s#^;kmc_login_version = @KMC_LOGIN_VERSION@#kmc_login_version = %{kmc_login_version}#g" $RPM_BUILD_ROOT%{confdir}/local.template.ini
sed -i "s@clipapp_version = @CLIPPAPP_VERSION@#clipapp_version = %{clipapp_version}#g" $RPM_BUILD_ROOT%{confdir}/local.template.ini
sed -i "s#^clipapp_version =.*#clipapp_version = %{clipapp_version}#g" $RPM_BUILD_ROOT%{confdir}/base.ini
sed -i "s#^kmc_analytics_version =.*#kmc_analytics_version = %{kmc_analytics_version}#g" $RPM_BUILD_ROOT%{confdir}/base.ini
sed -i "s#^;kdp3_wrapper_version = @KDP3_WRAPPER_VERSION@#kdp3_wrapper_version = %{kdp3_wrapper_version}#g" $RPM_BUILD_ROOT%{confdir}/local.template.ini
sed -i "s#@PLAYKIT_JS_SOURCES_PATH@#%{prefix}/html5/html5lib/playkitSources#g" $RPM_BUILD_ROOT%{confdir}/local.template.ini
sed -i "s#@PLAYKIT_JS_SOURCES_MAP_LOADER@#embedPlaykitJsSourceMaps#g" $RPM_BUILD_ROOT%{confdir}/local.template.ini
sed -i "s#@INERNAL_BUNDLER_URL@#http://127.0.0.1:8880#g" $RPM_BUILD_ROOT%{confdir}/local.template.ini
sed -i "s#^play_kit_js_cache_version = 1#play_kit_js_cache_version = 2#g" $RPM_BUILD_ROOT%{confdir}/local.template.ini
sed -i 's@^writers.\(.*\).filters.priority.priority\s*=\s*7@writers.\1.filters.priority.priority=4@g' $RPM_BUILD_ROOT%{confdir}/logger.template.ini 
# our Pentaho is correctly installed under its own dir and not %prefix/bin which is the known default so, adding -k path to kitchen.sh
sed -i 's#\(@DWH_DIR@\)$#\1 -k %{prefix}/pentaho/pdi/kitchen.sh#g' $RPM_BUILD_ROOT%{confdir}/cron/dwh.template
sed -i 's@2\s*=\s*"kmcng"@;2 = "kmcng"@g' $RPM_BUILD_ROOT%{confdir}/elasticDynamicMap.template.ini
sed -i 's@sphinx_log@kaltura_sphinx_log.sphinx_log@g' $RPM_BUILD_ROOT%{prefix}/app/deployment/updates/sql/2020_11_05_sphinx_log_dc_id_index.sql
rm $RPM_BUILD_ROOT%{prefix}/clients-generator/sources/android/DemoApplication/libs/libWVphoneAPI.so
#rm $RPM_BUILD_ROOT%{prefix}/clients-generator/sources/android2/DemoApplication/libs/libWVphoneAPI.so
rm $RPM_BUILD_ROOT%{confdir}/.project
# we have our own that is provided with the kaltura-monit package
rm $RPM_BUILD_ROOT%{confdir}/monit/monit.template.conf
rm $RPM_BUILD_ROOT%{prefix}/app/deployment/base/scripts/init_content/04.dropFolder.-4.template.xml
sed 's@#!/usr/bin/python@#!/usr/bin/python2@g' -i $RPM_BUILD_ROOT%{prefix}/app/alpha/scripts/utils/apiGrep.py

# we bring our own for kaltura-front and kaltura-batch.
cp %{SOURCE4} $RPM_BUILD_ROOT%{prefix}/app/batch/batches/Mailer/emails_en.template.ini
cp %{SOURCE11} $RPM_BUILD_ROOT%{prefix}/app/alpha/crond/kaltura/clear_cache.sh
mkdir -p $RPM_BUILD_ROOT%{confdir}/monit/monit.avail
cp %{SOURCE13} $RPM_BUILD_ROOT%{confdir}/monit/monit.avail/
cp %{SOURCE20} $RPM_BUILD_ROOT%{confdir}/monit/monit.avail/
cp %{SOURCE14} $RPM_BUILD_ROOT%{confdir}/monit/monit.avail/
cp %{SOURCE15} $RPM_BUILD_ROOT%{confdir}/monit/monit.avail/
cp %{SOURCE16} $RPM_BUILD_ROOT%{confdir}/monit/monit.avail/
rm $RPM_BUILD_ROOT%{confdir}/monit/monit.d/*template*
cp %{SOURCE25} $RPM_BUILD_ROOT%{confdir}/logrotate/
cp %{SOURCE26} $RPM_BUILD_ROOT%{confdir}/logrotate/

# Kalt connector
cp %{SOURCE39} %{SOURCE47} $RPM_BUILD_ROOT%{prefix}/app/plugins/content_distribution/providers/cross_kaltura/lib/batch/
cp %{SOURCE40} %{SOURCE42} $RPM_BUILD_ROOT%{prefix}/app/plugins/content_distribution/providers/cross_kaltura/lib/api 
cp %{SOURCE41} $RPM_BUILD_ROOT%{prefix}/app/plugins/content_distribution/providers/cross_kaltura/lib/admin
cp %{SOURCE43} %{SOURCE44} %{SOURCE45}  $RPM_BUILD_ROOT%{prefix}/app/plugins/content_distribution/providers/cross_kaltura/lib/model
cp %{SOURCE46} $RPM_BUILD_ROOT%{prefix}/app/plugins/content_distribution/providers/cross_kaltura/ 

# David Bezemer's Admin console and monit patches:
cp %{SOURCE17} $RPM_BUILD_ROOT%{prefix}/app/admin_console/configs/navigation.xml
cp %{SOURCE18} $RPM_BUILD_ROOT%{prefix}/app/admin_console/views/scripts/index/monit.phtml
cp %{SOURCE19} $RPM_BUILD_ROOT%{prefix}/app/admin_console/controllers/IndexController.php
# we bring a1nother in kaltura-batch
rm $RPM_BUILD_ROOT%{confdir}/batch/batch.ini.template
cp %{SOURCE32} $RPM_BUILD_ROOT%{prefix}/app/infra/cdl/kdl/KDLOperatorFfmpeg1_1_1.php

# tmp patch for the new start page, to be removed once merged into the server repo
cp %{SOURCE35} $RPM_BUILD_ROOT%{prefix}/app/start/index.php
cp %{SOURCE36} $RPM_BUILD_ROOT%{prefix}/app/start/img/survey.png
cp %{SOURCE37} $RPM_BUILD_ROOT%{prefix}/app/start/img/newsletter.png
cp %{SOURCE38} $RPM_BUILD_ROOT%{prefix}/app/start/css/landing-page.css
mkdir -p $RPM_BUILD_ROOT%{webdir}/content
tar zxf %{SOURCE10} -C $RPM_BUILD_ROOT%{webdir}/content

# tmp patch until https://github.com/kaltura/server/pull/9492 is merged
cp %{SOURCE48} $RPM_BUILD_ROOT%{prefix}/app/vendor/symfony-data/config/php.yml


%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/kaltura_base.sh << EOF
PATH=\$PATH:%{prefix}/bin
export PATH
alias allkaltlog='grep --color "ERR:\|PHP \|Stack trace:\|CRIT\|\[error\]" %{logdir}/*.log %{logdir}/batch/*.log'
alias kaltlog='tail -f %{logdir}/*.log %{logdir}/batch/*.log | grep -A 1 -B 1 --color "ERR:\|PHP \|Stack trace:\|CRIT\|\[error\]"'
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

ln -sf %{confdir}/system.ini /etc/kaltura.d/system.ini
ln -sf %{prefix}/app/api_v3/web %{prefix}/app/alpha/web/api_v3
if [ -d %{prefix}/web/content/clientlibs ];then
	mv %{prefix}/web/content/clientlibs %{prefix}/web/content/clientlibs.orig
fi
ln -sf %{prefix}/apps/clientlibs %{prefix}/web/content
chown apache.kaltura %{webdir}/content/entry %{webdir}/content/uploads/  %{webdir}/tmp/
chmod 775 %{webdir}/content/entry %{webdir}/content/uploads  %{webdir}/tmp
service chronyd start
if [ "$1" = 2 ];then
	if [ -r "%{confdir}/local.ini" -a -r "%{confdir}/base.ini" ];then
		sed -i "s@^\(kaltura_version\).*@\1 = %{version}@g" %{confdir}/local.ini
		echo "Regenarating client libs.. this will take up to 2 minutes to complete."
		if service httpd status;then
			service httpd stop
		fi
		# this is read by kaltura-sphinx-schema-update.sh to determine rather or not to run
		touch %{confdir}/sphinx_schema_update
		find %{prefix}/app/cache/ -type f -exec rm {} \;
		rm -f %{prefix}/app/base-config-generator.lock
		php %{prefix}/app/generator/generate.php
		php %{prefix}/app/deployment/base/scripts/installPlugins.php
		php %{prefix}/app/deployment/base/scripts/populateSphinxMetadata.php
		find %{prefix}/app/cache/ %{logdir} %{prefix}/var/run -type d -exec chmod 775 {} \;
		find %{logdir} -type f -exec chmod 664 {} \;
		# || true because it may fail if root_squash is used
		chown -R %{kaltura_user}.%{apache_user} %{prefix}/app/cache/ %{logdir} %{prefix}/var/run || true
		chmod 775 %{webdir}/content || true

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
		mysql -h$DB1_HOST -u $SUPER_USER -p$SUPER_USER_PASSWD -P$DB1_PORT $DB1_NAME < %{prefix}/app/deployment/updates/fix_version_management.sql 
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
%{prefix}/apps/clientlibs
%{prefix}/clients-generator

%config %{confdir}/*
%config %{prefix}/clients-generator/config/*
%config %{_sysconfdir}/profile.d/kaltura_base.sh
%config %{_sysconfdir}/ld.so.conf.d/kaltura_base.conf


%dir /etc/kaltura.d
%defattr(-, %{kaltura_user}, %{apache_group} , 0775)
%dir %{logdir}
%dir %{prefix}/var/run
%dir %{prefix}/tmp
%dir %{prefix}/app/cache
%{webdir}/*
%defattr(-, %{kaltura_user}, %{kaltura_group} , 0755)
%dir %{prefix}
%dir %{webdir}/control
%dir %{webdir}/dropfolders
%defattr(-, root,root, 0755)
%dir %{confdir}/monit/monit.d
%dir %{prefix}/bin
%dir %{prefix}/lib
%dir %{prefix}/include
%dir %{prefix}/share
%doc %{prefix}/app/release-notes.md
%doc %{prefix}/app/license.txt
%doc %{prefix}/app/VERSION.txt

%changelog
* Sun Dec 26 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.17.0-2
- PLAT-23289: Reset password - replace '.' with spaces in user's display name (https://github.com/kaltura/server/pull/11302)
- PLAT-23325: User login - attempt to prevent brute force attacks (https://github.com/kaltura/server/pull/11300)
- KMS-24338: Reject strings that contain certain special chars for certain properties on `kuser` object (https://github.com/kaltura/server/pull/11298)
- PLAT-23289: Added `myKuserUtils::sanitizeFields()` (https://github.com/kaltura/server/pull/11296)
- SUP-29689: Add support for `MPEG-4`, `MPEG-PS`, `Quicktime`, Windows Media and Flash video container formats (https://github.com/kaltura/server/pull/11292)
- Fix `resetUserPassword()` (https://github.com/kaltura/server/pull/11290)
- apimon: Improve `PS2` tracking (https://github.com/kaltura/server/pull/11289)
- `getDynamicEmailUserRoleName()` - verify `userRoleNames` is not a null value before continuing exec (https://github.com/kaltura/server/pull/11286)
- FOUN-182 - Beacon search - return more descriptive exceptions on missing parameters (https://github.com/kaltura/server/pull/11282)
- SUP-29860: Add an option to change the default audio flavor selection in the manifest file that's created from `LiveNG` (https://github.com/kaltura/server/pull/11279)
- FOUN-290 - Allow `FFMpeg` non-chunk convert to handle `estimatedEffort` threshold (https://github.com/kaltura/server/pull/11277)
- FEC-11387: Move player and studio version directives from `base.ini` to `appVersions.ini` (https://github.com/kaltura/server/pull/11271)
- AN-22688: Add virtual event id to `reportInputFilter` (https://github.com/kaltura/server/pull/11262)
- FOUN-289: Use `kFile` methods in upload flow (https://github.com/kaltura/server/pull/11241)
- FOUN-156: Support `api_rate limit` in `PS2` services (https://github.com/kaltura/server/pull/11210)
- SUP-20297: support REACH automatic rules when updating External-Media type (KMS current flow) (https://github.com/kaltura/server/pull/11199)

* Mon Dec 20 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.17.0-1
- Ver Bounce to 17.17.0

* Sat Dec 11 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.16.0-2
- Allow disabling of admin email notifications on new registration (https://github.com/kaltura/server/pull/11272)
- Less revealing exception messages (https://github.com/kaltura/server/pull/11269)
- PLAT-23312: `KDL` - new optimization mode (https://github.com/kaltura/server/pull/11268)
- PLAT-23311: Add permission for self serve partner to get partner object (https://github.com/kaltura/server/pull/11266)
- SUP-30171: Set `-max_muxing_queue_size` (https://github.com/kaltura/server/pull/11263)
- AN-22681: Add `count_all` metric (https://github.com/kaltura/server/pull/11256)
- Extend the period for `KalturaVodScheduleEvent` to max of 5 years (https://github.com/kaltura/server/pull/11252)
- Removed sub-type validation from Virtual Event (https://github.com/kaltura/server/pull/11251)
- SUP-29836: Added languages to live audio flavours (https://github.com/kaltura/server/pull/11250)
- Virtual Events: Added ability to insert multiple group IDs (https://github.com/kaltura/server/pull/11249)
- PLAT-23063: DRM - Add the ability to change more values in partner config via Admin Console (https://github.com/kaltura/server/pull/11248)
- PLAT-23219: Create EP Admin User - For Event Platform Manager application (https://github.com/kaltura/server/pull/11247)
- SUP-28990: Support the import of `SCC` caption from URL (https://github.com/kaltura/server/pull/11235)
- feat(FEC-11387): move player and studio version directives from `base.ini` to `appVersions.ini` (https://github.com/kaltura/server/pull/10894)
* Thu Dec 2 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.16.0-1
- Ver Bounce to 17.16.0

* Mon Nov 22 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.14.0-1
- SUP-30027 - Zoom `hotfix` (https://github.com/kaltura/server/pull/11228)
- SUP-29888: Zoom `hotfix` (https://github.com/kaltura/server/pull/11217)
- Create the `virtual_event` table (https://github.com/kaltura/server/pull/11214)
- Change `virtual_event.status_index` to `virtual_event.status_partner_index` (https://github.com/kaltura/server/pull/11209)
- Create the `virtual_event` table (https://github.com/kaltura/server/pull/11207)
- SUP-29192: Fix audio desc probing (https://github.com/kaltura/server/pull/11205)
- Fix `getLastFileUpdateTimeStampPath()` (https://github.com/kaltura/server/pull/11202)
- Chunked Encoding: Ensure the video is at least one second long (https://github.com/kaltura/server/pull/11201)
- PLAT-23234: Add credit info view role (https://github.com/kaltura/server/pull/11198)
- SUP-29192: Add audio language codes (https://github.com/kaltura/server/pull/11195)
- PLAT-23236: Remove zoom audio files when deleting the video file (https://github.com/kaltura/server/pull/11194)
- SUP-28825: Check `tff` when probing for interlaced content (https://github.com/kaltura/server/pull/11192)
- PLAT-23242: `report.getCsvAction()` - Support exclusion of fields (https://github.com/kaltura/server/pull/11191)
- PLAT-23233: Add `isSelfServe` property on partner object (https://github.com/kaltura/server/pull/11190)
- PLAT-23257: Fix `getDetails()` response (https://github.com/kaltura/server/pull/11186)
- Chunked Encoding: Support `FFMPEG_VP8` transcoding engine (https://github.com/kaltura/server/pull/11184)
- SUP-29168: Zoom fix (https://github.com/kaltura/server/pull/11182)
- PSVAMB-28716: Entity extraction process - Add support for live stream entries (https://github.com/kaltura/server/pull/11181)
- SUP-29832: Fix image input purification flow (https://github.com/kaltura/server/pull/11180)
- FOUN-166: Reduce the amount of DB updates made to `scheduler_worker` (https://github.com/kaltura/server/pull/11179)
- PLAT-23255: Configurable option: hide admin secrets in `KMCNG` (https://github.com/kaltura/server/pull/11178)
- PLAT-23192: add `systemPartner.updateConfiguration` permission for partner ID -12 (https://github.com/kaltura/server/pull/11167)
- Support graph and `partner_id` filter in `SELF_SERVE_USAGE` report (https://github.com/kaltura/server/pull/11137)
- Virtual Event integration (https://github.com/kaltura/server/pull/11114)


* Tue Nov 2 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.13.0-2
- REFINITIV-2515: Set Calais API `x-calais-selectiveTags` header (https://github.com/kaltura/server/pull/11170)
- Sphinx schema update (https://github.com/kaltura/server/pull/11160)
- FOUN-260: Support cue point table sharding (https://github.com/kaltura/server/pull/11149)
- FOUN-239 Access control - block requests whose GET params include sensitive data (https://github.com/kaltura/server/pull/11140)
- PLAT-23228: Admin console - only return roles that belong to partner ID -2 [Admin Console partner] (https://github.com/kaltura/server/pull/11138)
- Updated live thumbnail code to work with LiveNG (https://github.com/kaltura/server/pull/11024)

* Tue Oct 26 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.13.0-1
- Ver Bounce to 17.13.0

* Mon Oct 18 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.12.0-1
- PLAT-23221: `simulive` - round the duration to avoid stitching issues (https://github.com/kaltura/server/pull/11129)
- FOUN-223: Support ES 7 (https://github.com/kaltura/server/pull/11127)
- KMS-24770: Order user entries by `updatedAt` rather `id` (https://github.com/kaltura/server/pull/11123)
- FOUN-224: ES v7 mappings (https://github.com/kaltura/server/pull/11122)
- PSVAMB-27566: Add `lastEntryId` field to the `ViewHistoryUserEntry` object (https://github.com/kaltura/server/pull/11120)
- PLAT-23215: Grant `report.getTotal()` permission to self serve partner [-12] (https://github.com/kaltura/server/pull/11118)
- Add VP9/AV1 to Chunked Encoding verified codecs (https://github.com/kaltura/server/pull/11115)
- FOUN-230: Allow setting `isDefault=true` when adding new ACP (https://github.com/kaltura/server/pull/11113)
- SUP-28652: Fix Zoom registration failure due to `deletionPolicy=1` (https://github.com/kaltura/server/pull/11111)
- Add caption permissions + change release notes. (https://github.com/kaltura/server/pull/11110)
- FOUN-215 modify batch host wildcard regex (https://github.com/kaltura/server/pull/11109)
- FOUN-240 (https://github.com/kaltura/server/pull/11108)
- PLAT-23202: Internal server error on attempt to filter userGroups wit… (https://github.com/kaltura/server/pull/11107)
- SUP-28549: Set target quality to sharpen image (https://github.com/kaltura/server/pull/11106)
- PLAT-22927: Block sessions from embargoed countries (https://github.com/kaltura/server/pull/11105)
- PLAT-23207: Fix admin console behavior for new event notifications screen (https://github.com/kaltura/server/pull/11104)
- PLAT-23205: retrieve only oldest job in retrieveByJobTypeAndObject (https://github.com/kaltura/server/pull/11103)
- LIV-811 : Add permissions for caption service (update, list) for liveNG (partner -5 ) (https://github.com/kaltura/server/pull/11100)
- PLAT-23204: KDL - Add AV1 support (https://github.com/kaltura/server/pull/11099)
- PLAT-23017: Chunk enc VP9 AV1 (https://github.com/kaltura/server/pull/11098)
- PLAT-23206: `liveStream:authenticate()` - check the status of the partner ID the entry belongs to, rather than that of the -5 partner (https://github.com/kaltura/server/pull/11094)
- PLAT-23197: Add the ability to delete captions via MRSS (https://github.com/kaltura/server/pull/11093)
- PLAT-23201: Create new partner, status and permissions for self serve [-12] (https://github.com/kaltura/server/pull/11090)
- LIV-823: `getExcludeServerNodesFromAPI()` - Increase pager size for `serverNode.list()` (https://github.com/kaltura/server/pull/11088)
- PLAT-23102: Fixed `passwordUsedBefore()` (https://github.com/kaltura/server/pull/11087)
- PLAT-23148: Bulk upload, `addThumbAssets()` - Set the new thumbnail on the updated entry (https://github.com/kaltura/server/pull/11082)
- FOUN-240: Apply rate limiter on responseCacher (https://github.com/kaltura/server/pull/11072)
- FOUN-223: Support ES >= 7.X (https://github.com/kaltura/server/pull/11049)
- SUP-28194: Add fileSyncs in shared storage profile Ids to be queried in `getReadyInternalFileSyncsForKey()`(https://github.com/kaltura/server/pull/10932)

* Wed Oct 6 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.11.0-1
- PLAT-23203: Set `enableZoomTranscription` to true by default (https://github.com/kaltura/server/pull/11091)
- SUP-29337: Support the ability to not return partner API secrets (https://github.com/kaltura/server/pull/11086)
- PLAT-23131: Analytics - add the ability to configure the export method per partner (https://github.com/kaltura/server/pull/11083)
- PLAT-23130: `kFlowHelper::buildCustomUrl()` - call `urldecode()` on `baseUrl` (https://github.com/kaltura/server/pull/11078)
- FOUN-223: Support ES 7.10.2 (https://github.com/kaltura/server/pull/11076)
- PLAT-23144: New schedule event type - `VodScheduleEvent` (https://github.com/kaltura/server/pull/11071)
- PLAT-23130: Analytics - Add the referring URL (https://github.com/kaltura/server/pull/11069)
- Partner registration: move the operation of copying categories and UI confs to batch worker (https://github.com/kaltura/server/pull/11063)
- PLAT-23087: Thumbnail ingestion - restrict allowed content type (https://github.com/kaltura/server/pull/11061)
- REACH2-1085: Add Catalan REACH catalog item (https://github.com/kaltura/server/pull/11060)
- PLAT-23128: Add `session` and `usergroup` permissions to the CNC partner [-11] (https://github.com/kaltura/server/pull/11057)
- PLAT-23083: Purify cloned group properties (https://github.com/kaltura/server/pull/11053)
- PLAT-23046: Enhance admin console event notifications templates page (https://github.com/kaltura/server/pull/11051)
- Handle hashed/masked user ID on filter according to dimension and datasource (https://github.com/kaltura/server/pull/10975)
- Added VPaaS self served report (https://github.com/kaltura/server/pull/10834)

* Fri Sep 17 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.10.0-1
- PLAT-23147: remove base64 encoding in `servePlaybackKeyAction` (https://github.com/kaltura/server/pull/11056)
- Don't override template account permissions (https://github.com/kaltura/server/pull/11055)
- Zoom: Assign a default accuracy value (85%) (https://github.com/kaltura/server/pull/11054)
- PLAT-23135: REACH - allow aborting tasks that are in `pending` status (https://github.com/kaltura/server/pull/11048)
- Adjust abnormal frame rate value (https://github.com/kaltura/server/pull/11044)
- PLAT-22929: Webex - handle stuck files (https://github.com/kaltura/server/pull/11042)
- PLAT-23072: Admin Console - display DRM policies (https://github.com/kaltura/server/pull/11039)
- REACH: Add conditions to dynamic object cross-checks (https://github.com/kaltura/server/pull/11031)
- SUP-25390: Added script to set/update `templatePartnerId` for partner (https://github.com/kaltura/server/pull/11021)
- Add caption permissions API to live partner [ID -5] (https://github.com/kaltura/server/pull/11015)
- plat-23082: Partner registration - move all time consuming parts to run as batch jobs (https://github.com/kaltura/server/pull/10999)
- LIV-756: Simulive - support pre-roll and post-roll (https://github.com/kaltura/server/pull/10983)
- Support encrypted HLS (https://github.com/kaltura/server/pull/10982)
- PLAT-23050: Check that the object has the "getLanguage()" callable function (https://github.com/kaltura/server/pull/10968)
- LIV-780: refactor `checkAndCreateRecordedEntry()` (https://github.com/kaltura/server/pull/10948)
- PLAT-22565: Support `simulive` without specifying delivery profile (https://github.com/kaltura/server/pull/10385)

* Sun Aug 29 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.9.0-1
- Add IF NOT EXIST to all table creation statements (https://github.com/kaltura/server/pull/11019)
- PLAT-23018: C&C partner (https://github.com/kaltura/server/pull/11013)
- PLAT-23041: Fix `KalturaEntryVendorTaskFilter` (https://github.com/kaltura/server/pull/11007)
- SUP-28126: SIP URL encryption (https://github.com/kaltura/server/pull/11002)
- SUP-28126: SIP URL encryption enhancement (https://github.com/kaltura/server/pull/11001)
- FOUN-204: handle static content reconversion (https://github.com/kaltura/server/pull/10998)
- PLAT-23004: Thumbnails and distribution information for virtual (image) entries (https://github.com/kaltura/server/pull/10981)
- FOUN-172: Only index `READY` captions in ES and Sphinx (https://github.com/kaltura/server/pull/10979)
- FOUN-152: Optimise updating of `tag` table records (https://github.com/kaltura/server/pull/10856)

* Sun Aug 15 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.8.0-1
- SUP-28787: Fix drop folder 'match existing' flow (https://github.com/kaltura/server/pull/11012)
- SUP-28787: `KDropFolderFileTransferEngine::isEntryMatch()` - if no entry with the desired `conversionProfileId` exists, use default (https://github.com/kaltura/server/pull/11010)
- SUP-28655: If `recurrenceType == recurring`, populate `endDate` before the if null check (https://github.com/kaltura/server/pull/11008)
- FOUN-174: For static content trimming, we need to pass the `adminTags` to the temp entry in order to convert with the same flow as the original (https://github.com/kaltura/server/pull/10987)
- PLAT-23056: Zoom - Set vendor description only when the `dropfolder` description is updated (https://github.com/kaltura/server/pull/10986)
- PLAT-23066: Fix `playManifest` crash when a live liveEntry has an AC profile applied (https://github.com/kaltura/server/pull/10985)
- PLAT-23052: Teams int - Prevent creation of duplicate entries (https://github.com/kaltura/server/pull/10978)
- FOUN-195: Zoom - inconsistent conversion profile (https://github.com/kaltura/server/pull/10973)
- PLAT-23048: Support displaying system default (partner ID 0) conversion profiles (https://github.com/kaltura/server/pull/10971)
- SUP-28434: Verify that the audio flavor status is `READY` before clipping (https://github.com/kaltura/server/pull/10967)
- PLAT-22934: KMS 2FA authentication (https://github.com/kaltura/server/pull/10966)
- `kBusinessPreConvertDL::shouldCheckStaticContentFlow()` (https://github.com/kaltura/server/pull/10964)
- PLAT-23047: `KalturaIntegrationSetting::toInsertableObject()` Ignore `updateAt` and `createdAt` read only params (https://github.com/kaltura/server/pull/10961)
- PLAT-23020: Added `conversionProfileIdEqual` to `KalturaBaseEntryFilter` (https://github.com/kaltura/server/pull/10957)
- PLAT-23042: Manage caching of `simulive` entries (https://github.com/kaltura/server/pull/10954)
- PSVAMB-25152: MS Teams integration (https://github.com/kaltura/server/pull/10953)
- SUP-25858: Added `kEntryScheduledCondition` (https://github.com/kaltura/server/pull/10949)
- FOUN-174: Handle static content conversions (https://github.com/kaltura/server/pull/10944)
- Fix duration issue for Schedule Events (https://github.com/kaltura/server/pull/10943)
- SUP-27619: Support raw file concat in concat job based on worker params (https://github.com/kaltura/server/pull/10941)
- PLAT-23025: Before indexing in ES, filter captions by language, label and accuracy (https://github.com/kaltura/server/pull/10936)
- Add partner ID filter to webcast highlights report so we can use it in the SF integration (https://github.com/kaltura/server/pull/10933)
- PSVAMB-16509: Add setup script for Webcast event notifications (https://github.com/kaltura/server/pull/10931)
- PLAT-22932: Add the ability to replace captions with `MRSS` (https://github.com/kaltura/server/pull/10924)
- AN-22584: Add `hasSegmentDownloadTime`, `hasManifestDownloadTime` to RT discovery reports (https://github.com/kaltura/server/pull/10913)
- SUP-27588: Change query for replacing entry drop folder file (https://github.com/kaltura/server/pull/10738)

* Sun Aug 1 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.7.0-1
- FOUN-174-HF: Better handling of static content "Talking heads" conversion (https://github.com/kaltura/server/pull/10960)
- Added handling of duration update on linked events (https://github.com/kaltura/server/pull/10937)
- SUP-28507: isConcatOfAllChildrenDone() return true once conversion is over (https://github.com/kaltura/server/pull/10934)
- SUP-28338: Added `CONTAINER_FORMAT_MPEG_AUDIO` and `CONTAINER_FORMAT_MPEG_TS` constants to `assetParams` (https://github.com/kaltura/server/pull/10927)
- SUP-28364 : Do not copy default live conversion profile from template (https://github.com/kaltura/server/pull/10925)
- PLAT-23005: Create DRM custom data even if the entry has no flavours (https://github.com/kaltura/server/pull/10922)
- Fix Reach profile credit update check (https://github.com/kaltura/server/pull/10921)
- SUP-27422: Support additional elements when generating `webvtt` from `DFXP` caption (https://github.com/kaltura/server/pull/10919)
- SUP-27559: Fix `SRT` line index when clipping the beginning of the entry (https://github.com/kaltura/server/pull/10918)
- Always prefer file syncs from current DC (https://github.com/kaltura/server/pull/10917)
- SUP-27990: Support long UTF8 strings for `kuser` `firstName` and `lastName` (https://github.com/kaltura/server/pull/10916)
- PLAT-22925: Validate caption content upon ingest (https://github.com/kaltura/server/pull/10907)
- REG-202: Support Elastic split indexes (https://github.com/kaltura/server/pull/10837)

* Sun Jul 18 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.6.0-1
- SUP-27609: Fix issue in Zoom transcript processing (https://github.com/kaltura/server/pull/10923)
- PLAT-23016: Ignore short name in password validations (https://github.com/kaltura/server/pull/10910)
- Export script: Improve original DC logic (https://github.com/kaltura/server/pull/10908)
- Export script touch-ups (https://github.com/kaltura/server/pull/10906)
- SUP-28225: Invoke `kEntitlementUtils::getEntitlementEnforcement()` to handle execution of playlist with privacyContext (https://github.com/kaltura/server/pull/10905)
- PLAT-23003: Scheduling - fix error when deleting events (https://github.com/kaltura/server/pull/10904)
- SUP-28338: Added `CONTAINER_FORMAT_MPEG_AUDIO` and `CONTAINER_FORMAT_MPEG_TS` to `assetParams` (https://github.com/kaltura/server/pull/10903)
- SUP-27609: Use `zoomIntegration` param rather than property which is undefined at `kZoomTranscriptProcessor` (https://github.com/kaltura/server/pull/10901)
- Support skip regex per file sync `type:objectType` (https://github.com/kaltura/server/pull/10900)
- LIV-529 : Upload source when media info changed (https://github.com/kaltura/server/pull/10899)
- Fix fatal during convert job creation + refactor tmp bucket usage (https://github.com/kaltura/server/pull/10897)
- PLAT-22995: `addLoginData()`: Avoid validating password if `checkPasswordStructure` is false (https://github.com/kaltura/server/pull/10896)
- Added `encryptedSeed` field to user object (https://github.com/kaltura/server/pull/10893)
- SUP-28338: Added `CONTAINER_FORMAT_QT` to `assetParams` (https://github.com/kaltura/server/pull/10892)
- FOUN-153: Disable `rate_limiter` check when running in batch context (https://github.com/kaltura/server/pull/10890)
- FOUN-129: Handle '#' in URL when importing (https://github.com/kaltura/server/pull/10889)
- Add graph to webcast highlights report (https://github.com/kaltura/server/pull/10885)
- FOUN-150: Support file deletion from S3 (https://github.com/kaltura/server/pull/10884)
- SUP-27743: Change type of `sizeInBytes` from `int` to `bigint` (https://github.com/kaltura/server/pull/10882)
- PLAT-22973: Allow setting of ES search options per partner (https://github.com/kaltura/server/pull/10879)
- PLAT-22976: Add null protection for `limitLiveByAdminTag` (https://github.com/kaltura/server/pull/10876)
- FOUN-153: Disable `rate_limiter` when running in batch context (https://github.com/kaltura/server/pull/10875)
- FOUN-127: Move writing of tmp files created by clip|trim operations to the temp bucket so they will be purged by the policy lifecycle  (https://github.com/kaltura/server/pull/10873)
- FOUN-150: Support file deletion from S3 (https://github.com/kaltura/server/pull/10872)
- FOUN-129: Handle '#' in URL when importing (https://github.com/kaltura/server/pull/10871)
- PLAT-22966: Fix `getDetailsAction` for `Simulive` (https://github.com/kaltura/server/pull/10861)
- FOUN-66 - Fix `kSitCondition` to work with `endSwith` (https://github.com/kaltura/server/pull/10854)
- plat-22775: Allow admins to schedule the time to redirect a recording to another entry (https://github.com/kaltura/server/pull/10852)

* Thu Jul 8 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.5.0-1
- PLAT-22874: Fix checkIsLive for LiveDash (https://github.com/kaltura/server/pull/10868)
- Support AV1 video codec (https://github.com/kaltura/server/pull/10867)
- Support AV1 video codec (https://github.com/kaltura/server/pull/10866)
- Support AV1 video codec (https://github.com/kaltura/server/pull/10865)
- Support AV1 video codec (https://github.com/kaltura/server/pull/10864)
- PLAT-22972: Multi Audio Clipping - One multi audio flavor is missing if clipping for which there's a different clipping operation in progress (https://github.com/kaltura/server/pull/10863)
- PLAT-22874: Support Live AWS DASH Playback for Manual Entries (https://github.com/kaltura/server/pull/10860)
- SUP-28118: add file extension when creating original flavor asset in `attachFileSync` (https://github.com/kaltura/server/pull/10859)
- FEC-11008: Correctly pass player version (https://github.com/kaltura/server/pull/10857)
- PLAT-22961: Support enabling 2FA for admin users only (https://github.com/kaltura/server/pull/10850)
- SUP-28207: Zoom - Pass correct filter object when fetching user by email (https://github.com/kaltura/server/pull/10849)
- PLAT-22961: Support enabling 2FA for admin users only (https://github.com/kaltura/server/pull/10848)
- SUP-27954: Call `setSizeInBytesOnAsset()` when using share and remote storage (https://github.com/kaltura/server/pull/10847)
- Add support for `OpenCalais` API Endpoint configuration in `partner.custom_data` (https://github.com/kaltura/server/pull/10846)
- PLAT-22961: Support enabling 2FA for admin users only (https://github.com/kaltura/server/pull/10845)
- PLAT-22960: Zoom - don't upload old meetings (https://github.com/kaltura/server/pull/10842)
- PLAT-22955: Do not register sub partners on Marketo (https://github.com/kaltura/server/pull/10840)
- SUP-28076: Fix `restoreDeletedEntriesByEntryList.php` to work with S3 file sync path (https://github.com/kaltura/server/pull/10836)
- PLAT-22841: For multi audio files, do not reconvert when clipping (https://github.com/kaltura/server/pull/10829)
- SUP-27690: Prevent sending of "Entry Was Added To Category" email notifications for live entries (https://github.com/kaltura/server/pull/10826)
- FEC-11288: Define product version by core components (https://github.com/kaltura/server/pull/10802)
- PSVAMB-25378, PSVAMB-24119: Support Pexip >= v21 (https://github.com/kaltura/server/pull/10783)

* Tue Jun 22 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.4.0-1
- PLAT-22740: Trigger the distribution last (https://github.com/kaltura/server/pull/10833)
- PLAT-22950: `dynamicGetter()` in case of `simuliveFlow` return playable only once we're at least 18 seconds into playback (https://github.com/kaltura/server/pull/10832)
- SUP-27856: Verify that asset is not a `CaptionAsset` before updating entry status to prevent the entry from being stuck at `import` state when adding captions from `urlResource` (https://github.com/kaltura/server/pull/10830)
- PLAT-22906: Add the ability to auto delete specific drop folder files based on regex (https://github.com/kaltura/server/pull/10828)
- PLAT-22933: Fix `firstNameOrLastNameStartsWith` filter (https://github.com/kaltura/server/pull/10827)
- SUP-26045: Fix `PeerUtils::setExtension()` (https://github.com/kaltura/server/pull/10822)
- SUP-27927: `kMetadataKavaUtils()` - Fetch metadata from shared storage (https://github.com/kaltura/server/pull/10821)
- PLAT-22740: Fix distribution of thumbnails after update via XML bulk upload (https://github.com/kaltura/server/pull/10820)
- Specific origin `CORS` fix (https://github.com/kaltura/server/pull/10819)
- PLAT-22916: Handle audio files in Zoom (https://github.com/kaltura/server/pull/10818)
- SUP-24729: Change `execute()` action to go to elastic if no filter is provided (https://github.com/kaltura/server/pull/10817)
- PLAT-22872: `kUser` password validation - block "common" passwords (https://github.com/kaltura/server/pull/10798)
- PLAT-22871: API to fetch password structure rules (https://github.com/kaltura/server/pull/10779)


* Mon Jun 14 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.3.0-1
- PLAT-22921: Resubmission should not be possible for tasks while an active task exists in the queue. (https://github.com/kaltura/server/pull/10810)
- PLAT-22917: Can't edit and save a recurring event (https://github.com/kaltura/server/pull/10809)
- PLAT-22915: Support obtaining legacy content from Zoom (https://github.com/kaltura/server/pull/10808)
- FOUN-147: Support setting `userAgent` when using S3 client (https://github.com/kaltura/server/pull/10804)
- Handle error in `jobRequeue` when no token is defined + avoid chunk job loop when timeout is reached (https://github.com/kaltura/server/pull/10797)
- PLAT-22902: Chunked Encoding - fix user CPU metrics (https://github.com/kaltura/server/pull/10796)
- PLAT-22900: Zoom - do not pull content when it already uploaded with an old reference (https://github.com/kaltura/server/pull/10795)
- SUP-27646: `ThumbAssetService::attachFileSync()` - Resolve to `linked_id` `fileSync` if exists so that height, width and size be set properly (https://github.com/kaltura/server/pull/10794)
- PLAT-22840: Partner Registration validation (https://github.com/kaltura/server/pull/10791)
- PLAT-22901: REACH - HTTP 500 when ordering caption (https://github.com/kaltura/server/pull/10790)
- PSVAMB-18194: Develop REACH middleware layer (https://github.com/kaltura/server/pull/10789)
- PLAT-22888: Zoom - handle both `fullName` and `name` in categories (https://github.com/kaltura/server/pull/10788)
- PLAT-22895: Event scheduling - unable to update event (https://github.com/kaltura/server/pull/10787)
- PLAT-22885: `KalturaObject::generateFromObjectClass()` pass response profile (https://github.com/kaltura/server/pull/10786)
- No-Plat: Fix `s3Mgr` `isDir()` check to take into account file names with no extension (https://github.com/kaltura/server/pull/10784)
- PLAT-22891: Change `autoDeletionDays`, set default values on integration, update `deletionPolicy` on drop folder according to integration (https://github.com/kaltura/server/pull/10781)
- PLAT-22889: On transcription completed event, search the `parentEntry` for every transcription file (https://github.com/kaltura/server/pull/10776)
- PLAT-22888: Zoom - fix category assoc (https://github.com/kaltura/server/pull/10773)
- FOUN-103: Correct elastic populate (check for `is_null()` as well as `empty()`) (https://github.com/kaltura/server/pull/10772)
- PLAT-22884: `zoomRecordingProcessor::approveEntryIfNeeded()` (https://github.com/kaltura/server/pull/10771)
- PSVAMB-18194: Develop REACH middleware layer (https://github.com/kaltura/server/pull/10769)
- PLAT-22858: Sphinx - "starts with" expressions incorrectly interpreted (https://github.com/kaltura/server/pull/10755)
- PLAT 22767: `infraRequestUtils::getRequestParams()` - incorrect JSON parsing (https://github.com/kaltura/server/pull/10750)
- PLAT-22844: added error code and message to bulk upload failed HTTP notification (https://github.com/kaltura/server/pull/10749)

* Wed May 26 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.2.0-1
- Add playback base role update script (https://github.com/kaltura/server/pull/10758)
- PLAT-22864: Changing label name on `zoomRegistrationPage` (https://github.com/kaltura/server/pull/10756)
- PLAT-22864: Zoom: Registering multiple PIDs to same Zoom account creates inconsistency in uploads (https://github.com/kaltura/server/pull/10754)
- `callOauth`: Zoom: Replace action names `oauthValidationAction` and `preOauthValidation` (https://github.com/kaltura/server/pull/10752)
- Introduced `loadDropFolderFiles()` (https://github.com/kaltura/server/pull/10748)
- PLAT-22865: `KZoomDropFolderEngine` - Introduced `enableMeetingUpload` to `registrationPage()`(https://github.com/kaltura/server/pull/10745)
- `Simulive`: `mpeg-ts` wraparound fix (https://github.com/kaltura/server/pull/10744)
- PLAT-22865: Added `EnableMeetingUpload` flag on `vendorIntegration` (https://github.com/kaltura/server/pull/10743)
- PLAT-22865: Added `EnableMeetingUpload` flag on `vendorIntegration` (https://github.com/kaltura/server/pull/10742)
- PLAT-22867: Add webinar handling on new zoom (https://github.com/kaltura/server/pull/10740)
- FOUN-143: Support setting bulk size dynamically (https://github.com/kaltura/server/pull/10739)
- PLAT-22862: Remove certain fields when zoom integration is without drop folder (https://github.com/kaltura/server/pull/10736)
- PLAT-22860: When `ZoomTranscription` field is disabled, do not pull Zoom transcription (https://github.com/kaltura/server/pull/10734)
- SUP-27631: `KCurlWrapper` - Remove double quotation marks on 'user-agent' header (https://github.com/kaltura/server/pull/10728)
- AN-22489: `playsviews` copy VOD metrics to live (https://github.com/kaltura/server/pull/10727)
- FOUN-132: Add missing permission to `PLAYBACK_BASE_ROLE` (https://github.com/kaltura/server/pull/10726)
- PLAT-22774: Schedule event - block creation of multiple events in the same time window (https://github.com/kaltura/server/pull/10725)
- PLAT-22853: Support setting `access-control-allowed-domain` on `playManifest` calls (https://github.com/kaltura/server/pull/10723)
- SUP-26045: When `rowData` is longer than what the DB can contain, save the rest in `custom_data` (https://github.com/kaltura/server/pull/10722)
- PLAT-22848: Mapping `createdAt` and `updatedAt` fields on `KalturaZoomIntegrationSetting` (https://github.com/kaltura/server/pull/10721)
- PLAT-22838: Pass `partnerId` to the Facebook `OAuth2` flow (https://github.com/kaltura/server/pull/10720)
- Refactored partner registration and validation (https://github.com/kaltura/server/pull/10715)
- SUP-27196: Add `inputEntitledUsersView` to MR (https://github.com/kaltura/server/pull/10708)
- SUP-24966: Check container format using `MediaInfo` (https://github.com/kaltura/server/pull/10707)
- Fix dynamic `confiugred_id` allocation (https://github.com/kaltura/server/pull/10703)

* Wed May 5 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.1.0-1
- Config for collecting Sphinx Search stats (https://github.com/kaltura/server/pull/10716)
- PLAT-22839: Fix wrong handling of updating pre-configured `LiveStreamScheduleEvents` (https://github.com/kaltura/server/pull/10702)
- SUP-24181: Prevents sending email notifications for temporary entries (https://github.com/kaltura/server/pull/10701)
- PLAT-22800: `KalturaLiveStreamScheduleEvent` - refactor start /end date calculation (https://github.com/kaltura/server/pull/10697)
- Use config to disable Zoom drop folder (https://github.com/kaltura/server/pull/10696)
- PLAT-22737: For `thumbAssets`, when entry is image, create file sync per asset (not per entry) (https://github.com/kaltura/server/pull/10694)
- PLAT-22836: Pre/post simulive config not honoured (https://github.com/kaltura/server/pull/10693)
- PLAT-22836: `Simulive` - Wrong calculation of `startDate` and `endDate` (https://github.com/kaltura/server/pull/10692)
- PLAT-22836 - `LiveScheduling` index issue (https://github.com/kaltura/server/pull/10691)
- PLAT-22835: Handle 2 recording on the same scheduling event (https://github.com/kaltura/server/pull/10690)
- Zoom: block auto transcript when `flavorAsset` has changed (https://github.com/kaltura/server/pull/10689)
- PLAT-22647: Allow creating of Zoom Integration without oAuth2 call from Zoom (https://github.com/kaltura/server/pull/10686)
- PLAT-22800: `KalturaLiveStreamScheduleEvent` - refactor start /end date calculation (https://github.com/kaltura/server/pull/10685)
- PLAT-22737: Update every `flavorAsset` status to ready when import finishes (https://github.com/kaltura/server/pull/10684)
- LIV-511 : Revise recording creation check (https://github.com/kaltura/server/pull/10683)
- SUP-24181: Do not trigger email notification for temporary entries (https://github.com/kaltura/server/pull/10682)
- PLAT-22800: Live Stream Schedule Event (https://github.com/kaltura/server/pull/10681)
- Zoom: Check entry by `refernceId` for the last hours, fix auto deletion policy (https://github.com/kaltura/server/pull/10680)
- `KalturaLiveStreamScheduleEvent` - refactor start /end date calculation (https://github.com/kaltura/server/pull/10678)
- SUP-26711: `YouTubeApi` prefer file sync from `periodic_storage_ids` if exists (https://github.com/kaltura/server/pull/10677)
- SUP-26711: `postConvert` -  prefer file sync from `periodic_storage_ids` if exists (https://github.com/kaltura/server/pull/10676)
- PLAT-22799: Zoom drop folder was not editable via adminConsole without param `FileNamePatterns` (https://github.com/kaltura/server/pull/10675)
- PLAT-22797: Zoom V2 integration user is NOT added to Co-Publishers when performing host/invite meeting (https://github.com/kaltura/server/pull/10673)
- Zom: Add page redirection to the regional cloud (derived by the kmc url) (https://github.com/kaltura/server/pull/10671)
- PLAT-22773: VendorIntegration.listAction() - return all Zoom integrations per partner (https://github.com/kaltura/server/pull/10670)
- PLAT-22772: Add Zoom account description to vendor integration (https://github.com/kaltura/server/pull/10669)
- plat 22769: Live code with schedule events refactoring (https://github.com/kaltura/server/pull/10668)
- PLAT-22793: Allow all partners dropfolder access (https://github.com/kaltura/server/pull/10666)
- Enable mapping of secondary secret to a specific user role (https://github.com/kaltura/server/pull/10664)
- PLAT-22779: `zoomClient` creation with `access_token` (https://github.com/kaltura/server/pull/10663)
- SUP-27074: Add null check for asset before use to prevent errors (https://github.com/kaltura/server/pull/10662)
- `apiV3/playManifest`:  referrer cache fix (https://github.com/kaltura/server/pull/10659)
- export script: support original only mode (https://github.com/kaltura/server/pull/10658)
- AN-22544: KAVA - add reactions and `addToCalander` events to webcast reports (https://github.com/kaltura/server/pull/10642)

* Mon Apr 26 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.0.0-1
- Ver Bounce to 17.0.0

* Mon Apr 26 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.0.0-1
- Support asset labels in `simulive` (https://github.com/kaltura/server/pull/10643)
- SUP-27036: Change `bumperdata` type in `KalturaPlaybackContext` to fix parsing error in client library (https://github.com/kaltura/server/pull/10639)
- `appToken.startSessionAction()` does not require a KS (https://github.com/kaltura/server/pull/10638)
- Number of categories limited if there are more than 1 privacy context (https://github.com/kaltura/server/pull/10637)
- FOUN-98: save `importedFile` to shared path if size exceeds the size threshold (https://github.com/kaltura/server/pull/10634)
- PLAT-22760: Improve `S3` drop folder ingest time (https://github.com/kaltura/server/pull/10632)
- PLAT-22741: Add map between objects to `KalturaMeetingScheduleEvent` (https://github.com/kaltura/server/pull/10627)
- PLAT-22711: Increase category limit (without privacy context) to 1000 (https://github.com/kaltura/server/pull/10626)
- SUP-27046: Get width/height from file in `S3` (https://github.com/kaltura/server/pull/10625)
- PLAT-22738: Return correct `recorededEntryId` when `RedirectScheduleEvent` is active (https://github.com/kaltura/server/pull/10624)
- Add `StorageClass` & `ArchiveStatus` values to the head object result (https://github.com/kaltura/server/pull/10620)
- PLAT-22592: add `video/x-m4v` to allowed file types (https://github.com/kaltura/server/pull/10616)
- PLAT-22719: Restrict Access-Control-Allow-Origin Domains (https://github.com/kaltura/server/pull/10615)

* Mon Mar 15 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.19.0-1
- ExportToDifferentStorage.php: Cross partner ID link bug fix (https://github.com/kaltura/server/pull/10576)
- PLAT-22695: Handle uninstall/install of Zoom integration (https://github.com/kaltura/server/pull/10575)
- ExportToDifferentStorage.php: Handle null file type (https://github.com/kaltura/server/pull/10574)
- FOUN-126: Don't set enc key on post convert when asset format is `mpegts` (https://github.com/kaltura/server/pull/10571)
- Use `kDataCenterMgr::getSharedStorageProfileIds()` instead of `kStorageExporter::getPeriodicStorageIds()` (https://github.com/kaltura/server/pull/10570)
- Fix parse error on `kuser_mapping.json` (https://github.com/kaltura/server/pull/10567)
- PLAT-22606: Add parameter `entry_reference_id` to `EventNotificationTemplate` `HTTP_ENTRY_DISTRIBUTION_STATUS_CHANGED` (https://github.com/kaltura/server/pull/10566)
- Avoid Undefined variable notice when `calc_vid_sec` is unset (https://github.com/kaltura/server/pull/10565)
- VIRTC-2103: Allow dynamic adding of mapped fields to report (https://github.com/kaltura/server/pull/10564)
- PLAT-22679: Add parameter `file_name` to HTTP `EventNotificationTemplate` (https://github.com/kaltura/server/pull/10563)
- FOUN-124: Fix MR flow to delete local content file syncs (https://github.com/kaltura/server/pull/10562)
- PSVAMB-19547: VOD thumbnail to be applied to the live entry (https://github.com/kaltura/server/pull/10561)
- PLAT-22684 : Add schedule event type MEETING (https://github.com/kaltura/server/pull/10557)
- If prev `calc_vid_sec` is the same as the current one, re-use existing image (https://github.com/kaltura/server/pull/10556)
- PLAT-22683: Invalidate cache after `userLogin` was disabled (https://github.com/kaltura/server/pull/10555)
- FOUN-85: Set conversion log ext to conv.log (https://github.com/kaltura/server/pull/10551)
- HF: Prevent-Chk0-Reconverts (https://github.com/kaltura/server/pull/10548)
- PLAT-22622: Add `ClosedCaptions` to `PlayManifest` (https://github.com/kaltura/server/pull/10545)
- SUP-25895: Add flavour asset to `addImportJob()` in `handleVideoRecord()` (https://github.com/kaltura/server/pull/10543)

* Fri Feb 26 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.18.0-1
- `thumbnailAction()`: Avoid hitting the JPEG 64k limit (https://github.com/kaltura/server/pull/10534)
- Export script: Fix incorrect print for pending FS (https://github.com/kaltura/server/pull/10533)
- PLAT-22676: Fix S3 drop folder XML file handler (https://github.com/kaltura/server/pull/10532)
- PLAT-22670: `handleSignleRecordingInfo()` - revert `isPlayableUser` default to true (https://github.com/kaltura/server/pull/10531)
- SUP-24410: Add `entitledPusersView` in entry.php to support `entitledUsersView` (https://github.com/kaltura/server/pull/10527)
- SUP-26477: Add `PENDING_ENTRY_READY` status to `retrieveActiveTasks()` to prevent duplication of entry vendor tasks (https://github.com/kaltura/server/pull/10526)
- PLAT-22657: Update purify whitelist [`xss_allowed_object_properties`] (https://github.com/kaltura/server/pull/10522)
- AN-22495: Add download attachment clicked event (https://github.com/kaltura/server/pull/10521)
- PLAT-22617: Add the ability to set default KS privileges per user (https://github.com/kaltura/server/pull/10520)
- PLAT-22663: Zoom integration UI - added `createUserIfNotExist` (https://github.com/kaltura/server/pull/10519)
- PLAT-22657: Purifier - whitelist `ScheduleEvent` description (https://github.com/kaltura/server/pull/10516)
- PLAT-22661: Add the entry `viewMode` to the `EntryServerNode` object (https://github.com/kaltura/server/pull/10515)
- REACH2-1044: Support label addition for service CAPTIONS only (https://github.com/kaltura/server/pull/10512)
- FOUN-114: Add mandatory `confmap` description to keep track of change reason (https://github.com/kaltura/server/pull/10509)
- PLAT-22607: Set default `kuserId` for manager in `category.list()` (https://github.com/kaltura/server/pull/10507)
- PLAT-9940: Add filter options to `WidgetController` (https://github.com/kaltura/server/pull/10505)
- SUP-24964: Add domain + canonical URL to report filter (https://github.com/kaltura/server/pull/10504)
- Set `MinExection` Timeout (https://github.com/kaltura/server/pull/10500)
- PLAT-22638: Moved `kZoomClient` to infra folder (https://github.com/kaltura/server/pull/10497)
- SUP-24898: Allow reach vendors to access entries with access control (https://github.com/kaltura/server/pull/10496)
- PLAT-22614: Remove `remoteDir` from the S3 file path (https://github.com/kaltura/server/pull/10495)
- FOUN-116: Fix Sphinx delete command constructing index name incorrectly (https://github.com/kaltura/server/pull/10489)
- SUP-25018: Support live URL without redirect for internal media servers (https://github.com/kaltura/server/pull/10488)
- PLAT-11136: Show list of all `user_entry` if user is a entitled for entry (https://github.com/kaltura/server/pull/10438)

* Mon Feb 15 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.17.0-1
- FOUN-101: Doc conv., Webcasting and Webex - save output files to s3 (https://github.com/kaltura/server/pull/10490)
- Avoid internal redirect for files stored in shared storage (https://github.com/kaltura/server/pull/10485)
- PLAT-22650: oauthValidationAction() - do not disable `ZoomIntegration` (https://github.com/kaltura/server/pull/10483)
- Workaround for long audio conversions of MXF files (https://github.com/kaltura/server/pull/10481)
- FOUN-54: reset populate elastic client if ping check failed (https://github.com/kaltura/server/pull/10480)
- Fix `validateObjectContent` when working with encrypted files (https://github.com/kaltura/server/pull/10479)
- FOUN-113: if `mime_content_type()` doesn't exist, get type from `file` util (https://github.com/kaltura/server/pull/10478)
- Add played entries metric to category highlights report (https://github.com/kaltura/server/pull/10477)
- SUP-26014: groupUser - support removal of user from all groups (https://github.com/kaltura/server/pull/10475)
- Add played entries metric to category highlights report (https://github.com/kaltura/server/pull/10474)
- VIRTC-1606: Prevent saving on dry-run mode (https://github.com/kaltura/server/pull/10472)
- Limit number of failed job fetching attempts (https://github.com/kaltura/server/pull/10471)
- FOUN-101: Handle windows conversion for s3 (https://github.com/kaltura/server/pull/10470)
- PLAT-22609: Add new property called `adminTags` to category (https://github.com/kaltura/server/pull/10469)
- Plat-22608: Add company and title to `kuser.custom_data`  (https://github.com/kaltura/server/pull/10468)
- AN-22486: Add unique played entries metric (https://github.com/kaltura/server/pull/10467)
- Allow Chunked Encoding to process short contents (https://github.com/kaltura/server/pull/10464)
- FOUN-111: Handle dir listing on S3 buckets (https://github.com/kaltura/server/pull/10462)
- PLAT-22455: Fix purifier behaviour caused due to bad caching (https://github.com/kaltura/server/pull/10460)
- VIRTC-1606: Script for deleting non admin kusers (https://github.com/kaltura/server/pull/10457)
- FOUN-110: Change S3 dir list output logic to match non-S3 (https://github.com/kaltura/server/pull/10455)
- REACH2-1026: Cancel pending jobs via admin console (https://github.com/kaltura/server/pull/10454)
- FOUN-101: Doc conv., Webcasting and Webex - save output files to s3 (https://github.com/kaltura/server/pull/10453)
- FOUN-109: Support fetching shared directories to local storage for conversions (https://github.com/kaltura/server/pull/10452)
- FOUN-108 - Fix `cloud_storage` conf loading in batches (https://github.com/kaltura/server/pull/10449)
- FOUN-101: Make windows batches work with shared Storage (https://github.com/kaltura/server/pull/10447)
- FOUN-105: Support pushing src files created by clip concat flow directly to shared storage (https://github.com/kaltura/server/pull/10442)
- FOUN-106: File sync path should be generated with the next version suffix (https://github.com/kaltura/server/pull/10441)
- PLAT-11247: Added a script to update `flavorAsset->SizeInBytes` (https://github.com/kaltura/server/pull/10439)
- PLAT-22561: Expose `setEnforceHttpsApi` as checkbox in Admin Console `configure` view (https://github.com/kaltura/server/pull/10437)
- PLAT-22514: Zoom registration new UI (https://github.com/kaltura/server/pull/10425)


* Fri Jan 29 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.16.0-1
- Chunked Encoding range (https://github.com/kaltura/server/pull/10432)
- `KFFMpegMediaParser::detectEmptyFrames()`: handle empty lines (https://github.com/kaltura/server/pull/10430)
- PLAT-22544: `BulkUploadService::serve()` - set Content-Type to `text/plain` (https://github.com/kaltura/server/pull/10427)
- FOUN-100: Support running antivirus on remotely shared files using file pipe (https://github.com/kaltura/server/pull/10426)
- REACH2-1009: Enable Resubmission when job is in Pending/Processing mode for new version cases (https://github.com/kaltura/server/pull/10424)
- Handle edge case resulting in empty final chunks (https://github.com/kaltura/server/pull/10421)
- SUP-25701: Try to overcome possible zeroed frames issue, caused by too large GOP values in source files (https://github.com/kaltura/server/pull/10419)
- KAVA: Added `playlistId` filter (https://github.com/kaltura/server/pull/10418)
- Add full name to user usage report (https://github.com/kaltura/server/pull/10417)
- FOUN-82: Use `ffprobe` instead of `mediainfo` (https://github.com/kaltura/server/pull/10416)
- FOUN-96: Add kill method for memcache chunk encoder wrapper to support job re queuing (https://github.com/kaltura/server/pull/10415)
- SUP-25195: Thumbnail adapter support auto rotation (https://github.com/kaltura/server/pull/10412)
- Query cache: when caching use the hydration time (https://github.com/kaltura/server/pull/10410)
- REACH2-989: validate statuses before updating `entryVendorTask` status (https://github.com/kaltura/server/pull/10408)
- KChunkedEncodeMemcacheWrap: Increase `fetchRangeRandMax` (https://github.com/kaltura/server/pull/10407)
- PLAT-22547: Reload event notification templates after adding new ones (https://github.com/kaltura/server/pull/10396)
- FOUN-81: Support importing file directly to shared storage (https://github.com/kaltura/server/pull/10390)
- PLAT-22575: New drop folder type S3 (https://github.com/kaltura/server/pull/10388)
- FOUN-70: Support setting S3 upload concurrency (https://github.com/kaltura/server/pull/10361)


* Tue Jan 19 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.15.0-2
- Chunked encoding: support `fetchRangeRandMax` (https://github.com/kaltura/server/pull/10409)
- HF: Increase `fetchRangeRandMax` default value (https://github.com/kaltura/server/pull/10406)
- PLAT-22587: Do not use packager for download for encrypted content (https://github.com/kaltura/server/pull/10401)
- PLAT-22584 - Zoom user is missing when trying to match `cms_id` (https://github.com/kaltura/server/pull/10399)
- FOUN-72: Export CSV to S3 - do not use `seek()` (https://github.com/kaltura/server/pull/10398)
- Remove disallowed temp file (https://github.com/kaltura/server/pull/10395)
- FOUN-83: ES index `kuser.picture` (https://github.com/kaltura/server/pull/10394)
- FOUN-52: Support S3 read and write of bulk upload files (https://github.com/kaltura/server/pull/10393)
- PLAT-22579: `Simulive` - add id to sequence (`serveFlavor()`) (https://github.com/kaltura/server/pull/10392)
- FOUN-84: Retry file not found only when running on NFS mounted FS (https://github.com/kaltura/server/pull/10391)
- PLAT-22576: Avoid using different storage profiles for download (https://github.com/kaltura/server/pull/10389)
- `thumbnailAction()`: set `ignore_user_abort(true)` (https://github.com/kaltura/server/pull/10387)
- PLAT-11239: Avoid double slash chars on URL (https://github.com/kaltura/server/pull/10386)
- PLAT-22564: `attachementasset::get()` must have a KS (https://github.com/kaltura/server/pull/10384)
- SUP-24551: Add `sshUrlContentResource` support for subtitles (https://github.com/kaltura/server/pull/10383)
- SUP-25087: Add retry mechanism to `concatFiles`, increasing `FFmpeg` probe values upon attempt (https://github.com/kaltura/server/pull/10381)
- FOUN-80: Sync convert logs to shared storage in case conversion failed (https://github.com/kaltura/server/pull/10380)
- FOUN-79: Add reconnect params when working with `FFmpeg` aux (https://github.com/kaltura/server/pull/10379)
- PLAT-22544: Sanitise XML and HTML content on bulk (https://github.com/kaltura/server/pull/10378)
- apimon: Send the `hostname` on DB events (https://github.com/kaltura/server/pull/10376)
- PLAT-10788: Prevent default symfony page from loading (https://github.com/kaltura/server/pull/10375)
- REACH2-990: Add the ability to change the caption's label for ASR (https://github.com/kaltura/server/pull/10372)
- FOUN-50: Conversion profile XSLT to S3 (https://github.com/kaltura/server/pull/10370)
- FOUN-72: Export CSV to S3 (https://github.com/kaltura/server/pull/10369)
- FOUN-72: Export CSV to S3 (https://github.com/kaltura/server/pull/10368)
- REACH2-999: Add REACH job only after requested flavor params in REACH profile are ready (https://github.com/kaltura/server/pull/10367)
- SUP-24555: Add country name map in geo reports (https://github.com/kaltura/server/pull/10366)
- SUP-23739: Fix entries stuck in MR processing scripts (https://github.com/kaltura/server/pull/10365)
- Plat-22514: Zoom (https://github.com/kaltura/server/pull/10364)
- SUP-25701: Increase Keyframe seek interval (https://github.com/kaltura/server/pull/10362)
- SUP-25144: Add exception when elastic max matches threshold was reached (https://github.com/kaltura/server/pull/10360)
- AN-22457: Add a calendar clicked event metric (https://github.com/kaltura/server/pull/10359)
- FOUN-77: Add `ffmpeg` reconnect params in ngs and 2pass flow (https://github.com/kaltura/server/pull/10358)
- SUP-24759: Add `targetLanguage` in REACH export CSV (https://github.com/kaltura/server/pull/10356)
- FOUN-76: Move `kconf` methods to infra batch utils (https://github.com/kaltura/server/pull/10355)
- FOUN-75: Add `ffmpeg|ffprobe` reconnect params when running media info parser (https://github.com/kaltura/server/pull/10354)
- SUP-25559: Check if source asset is still in convert grace period (https://github.com/kaltura/server/pull/10353)
- PLAT-11239: Support download through `getServeFlavorUrl()` (https://github.com/kaltura/server/pull/10352)
- apimon: Improve partner ID coverage (https://github.com/kaltura/server/pull/10351)
- REACH2-998: Include media version in `reach_vendor` response profile (https://github.com/kaltura/server/pull/10345)
- FOUN-74 - Support S3 read and write generic syndication feed files (https://github.com/kaltura/server/pull/10344)
- FOUN-72 - Support writing & reading CSV export files directly to & from S3 (https://github.com/kaltura/server/pull/10339)
- S3 content set entry distribution (https://github.com/kaltura/server/pull/10337)
- SUP-23752: Handle HTTP 204 response code (https://github.com/kaltura/server/pull/10336)
- KAVA: Add `crmId` filter (https://github.com/kaltura/server/pull/10331)
- SUP-20297: Add REACH2 support for `external_media` of type YouTube (https://github.com/kaltura/server/pull/10268)

* Tue Jan 12 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.15.0-1
- Ver Bounce to 16.15.0

* Tue Jan 5 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.14.0-2
- FOUN-77: Add `ffmpeg` reconnect params to 2pass flow (https://github.com/kaltura/server/pull/10357)
- FOUN-75: Add `ffmpeg|ffprobe` reconnect params when running `mediainfo` parser (https://github.com/kaltura/server/pull/10348)
- PSVAMB-19304: Memcache - prevent attempt to connect when config is not present (https://github.com/kaltura/server/pull/10347)
- REACH2-973: Group zoom recording by start time (https://github.com/kaltura/server/pull/10335)
- PLAT-22550: Vid/Aud track duration detection (https://github.com/kaltura/server/pull/10330)
- SUP-24714: Allow download of assests for document type entries (https://github.com/kaltura/server/pull/10328)
- AN-22440: Add playbackType filter to total completion rate metric (https://github.com/kaltura/server/pull/10327)
- FOUN-71: Construct external URLs for shared file syncs as if they were local (https://github.com/kaltura/server/pull/10326)
- FOUN-48: S3 content set `fileAsset|Attachement|Transcript` (https://github.com/kaltura/server/pull/10325)
- Revert population of `liveStatus` attribute on manual live entry (https://github.com/kaltura/server/pull/10322)
- REACH2-981: Do not resubmit job while an older version is in progress (https://github.com/kaltura/server/pull/10320)
- FOUN-69: Support setting custom storage class when uploading files to S3 (https://github.com/kaltura/server/pull/10310)
- apimon: Additional `curl_exec()` monitors (https://github.com/kaltura/server/pull/10309)
- apimon: Monitor the different PHP exec functions (https://github.com/kaltura/server/pull/10308)
- REACH2-981: Do not resubmit job while an older version is in progress (https://github.com/kaltura/server/pull/10307)
- SUP-24350: Detect file extension for flavor assets when missing (https://github.com/kaltura/server/pull/10306)
- PLAT-22530: Support captions in `simulive` mode (https://github.com/kaltura/server/pull/10302)
- REACH2-982: Prevent resubmission when task is in Pending/Processing mode (https://github.com/kaltura/server/pull/10292)
- PLAT-11239: Add expiry to kaltura URL `tokenizer` and `recognizer` (https://github.com/kaltura/server/pull/10279)

* Mon Jan 4 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.14.0-1
- Ver Bounce to 16.14.0

* Thu Dec 31 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.13.0-4
- https://github.com/kaltura/server/pull/10340

* Mon Dec 21 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.13.0-3
- Fix deployment/updates/sql/2020_11_05_sphinx_log_dc_id_index.sql

* Mon Dec 21 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.13.0-2
- apimon: Reset Memcache & sleep vars in `multireq` (https://github.com/kaltura/server/pull/10301)
- FOUN-68: Avoid `fseek` notices when grabbing thumbnails from shared storage (https://github.com/kaltura/server/pull/10300)
- apimon fixes: Make sure Memcached wrapper is loaded (https://github.com/kaltura/server/pull/10299)
- FOUN-68: Avoid php notices due to early resolution of file sync path to shared URI (https://github.com/kaltura/server/pull/10297)
- apimon: Add `strval` on client tag (https://github.com/kaltura/server/pull/10295)
- Output the external err code to analytics & apimon (https://github.com/kaltura/server/pull/10294)
- `openFile()` and `readBytesFromStream()` should be static methods (https://github.com/kaltura/server/pull/10293)
- FOUN-67: Use `file_path` when invoking `isSharedPath()` (https://github.com/kaltura/server/pull/10290)
- FOUN-67: Handle shared storage dir serving as if they were local (https://github.com/kaltura/server/pull/10288)

- FOUN-65: Avoid writing to shared if file already exists and size matches (https://github.com/kaltura/server/pull/10287)
- apimon: Add upload event (https://github.com/kaltura/server/pull/10285)
- apimon: Monitor PS2 actions (https://github.com/kaltura/server/pull/10283)
- FOUN-64: Avoid saving file ext that contains none alphanumeric chars (https://github.com/kaltura/server/pull/10282)
- apimon: Track sleep time (https://github.com/kaltura/server/pull/10280)
- apimon: Add events on `KCurlWrapper` (https://github.com/kaltura/server/pull/10277)
- apimon: Add Memcache events (https://github.com/kaltura/server/pull/10275)
- apimon: API exec time fix (https://github.com/kaltura/server/pull/10272)
- FOUN-61: Use FS wrapper methods when working with files + resolve file path when building `FFmpeg` CLI command (https://github.com/kaltura/server/pull/10267)
- `Filesync` should be resolved before retuning it to handle links (https://github.com/kaltura/server/pull/10266)
- Compat check fixes (https://github.com/kaltura/server/pull/10260)
- KAVA - Add max result size to report def (https://github.com/kaltura/server/pull/10253)
- PLAT-22458 - Update flavour param configuration (https://github.com/kaltura/server/pull/10251)
- PSVAMB-16978 - Update LC conversion profiles (https://github.com/kaltura/server/pull/10249)
- SUP-25324: Treat shared storage file syncs as if they were local (https://github.com/kaltura/server/pull/10248)
- Sup-25292: Revert zoom pairing records into parent-child (https://github.com/kaltura/server/pull/10245)
- SUP-24970: `KDispatchEmailNotificationEngine` - support multiple BCC email addresses (https://github.com/kaltura/server/pull/10242)
- SUP-25292: Zoom - different records in same event (https://github.com/kaltura/server/pull/10241)
- PLAT-22504: Add stream password on clone (https://github.com/kaltura/server/pull/10240)
- PLAT-22489 [Zoom Integration] Configurable Transcoding Profile release notes (https://github.com/kaltura/server/pull/10238)
- fix(FEC-10733): `embedPlaykit` service doesn't throw critical error when `confvars` are not present (https://github.com/kaltura/server/pull/10237)
- `contextdata` cache fix (https://github.com/kaltura/server/pull/10236)
- Support forcing cached result (https://github.com/kaltura/server/pull/10230)
- KAVA - modify `partnerUsageEditFilter` (https://github.com/kaltura/server/pull/10227)
- Support defining group co existence constraints (https://github.com/kaltura/server/pull/10226)
- Doc conversion: Support pop-up windows closer for office 2013 (https://github.com/kaltura/server/pull/10225)
- psvamp-18174: Zoom transcoding profile configuration (https://github.com/kaltura/server/pull/10224)
- KAVA - edit filter for `simulive` webcast analytics (https://github.com/kaltura/server/pull/10223)
- Log the file path in case of file not found (https://github.com/kaltura/server/pull/10217)
- Export script - skip `dir` file syncs (https://github.com/kaltura/server/pull/10216)
- ExportToDifferentStorage: Export all types in assets mode (https://github.com/kaltura/server/pull/10213)
- If available, use S3 file sync for thumbnail action (https://github.com/kaltura/server/pull/10212)
- PLAT-22486: Remove the access control validation on a Bumper entry (https://github.com/kaltura/server/pull/10211)
- SUP-25014: Adjust Sphinx query in case there's no privacy context (https://github.com/kaltura/server/pull/10208)
- PLAT-22485: Support ClamAV 0.102.4 (https://github.com/kaltura/server/pull/10207)
- Support remote ffmpeg convert (https://github.com/kaltura/server/pull/10203)
- SUP-24970: Get `maxPagesToScan` value from worker `params` config, default is 7 (https://github.com/kaltura/server/pull/10200)
- SUP-24473: Fix thumbnail rotation (https://github.com/kaltura/server/pull/10199)
- SUP-23216: Volume map support on `filesync` on S3 (https://github.com/kaltura/server/pull/10192)
- PLAT-22454: Prevent `media.set/updateContent()` when restricted filetypes is enabled (https://github.com/kaltura/server/pull/10177)
- VIRTC-920: Support manual live status (https://github.com/kaltura/server/pull/10167)
- SUP-25064, PSVAMB-17989 - Not All cue points are copied (https://github.com/kaltura/server/pull/10165)
- Support pushing & getting metadata files to & from shared storage (https://github.com/kaltura/server/pull/10120)

* Mon Dec 14 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.13.0-1
- Ver bounce to 16.13.0

* Tue Nov 24 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.12.0-1
- Sup-23216: Audio track display is missing from the Editor (https://github.com/kaltura/server/pull/10202)
- Support remote convert via packager when working with shared storage (https://github.com/kaltura/server/pull/10194)
- PLAT-22465: entry::allowEdit() - auth validation enhancement (https://github.com/kaltura/server/pull/10190)
- Add invalidation keys for `ReachProfile` and `VendorCatalogItem` (https://github.com/kaltura/server/pull/10189)
- KMS-22652: `eSearch` - add max metadata index length to dynamic config (https://github.com/kaltura/server/pull/10188)
- PLAT-11197: Fix retrieval of sources of bumper entry (https://github.com/kaltura/server/pull/10187)
- Handle large source files in case local tmp storage is not shared + handle subs flow and watermark in tmp local disk (https://github.com/kaltura/server/pull/10186)
- PLAT-22459: system::pingAction() - add cache expiry (https://github.com/kaltura/server/pull/10185)
- kKavaReportsMgr: Increase memory limit, exec time and result size limit for CSV (https://github.com/kaltura/server/pull/10184)
- PLAT-22464: Check update attempts and return generic message (https://github.com/kaltura/server/pull/10183)
- SUP-24551: `sshUrlResource` - Add support for `CaptionAsset` (https://github.com/kaltura/server/pull/10182)
- REACH2-973: Multiple zoom entries to have 1 parent entry (https://github.com/kaltura/server/pull/10181)
- PLAT-11197: Support Bumper for live stream (https://github.com/kaltura/server/pull/10180)
- PLAT-22458: Align flavour spec with SaaS (https://github.com/kaltura/server/pull/10179)
- PLAT-22459: Add cache section per action in `api_v3` (https://github.com/kaltura/server/pull/10175)
- PLAT-11197: Add playback sources to `KalturaBumper` (https://github.com/kaltura/server/pull/10174)
- PSVAMB-17989: Start pageIndex at 1 (https://github.com/kaltura/server/pull/10173)
- `getSingleItemSearchQuery()`: Use dedicated index if exists (https://github.com/kaltura/server/pull/10172)
- Remove tmp files post convert (https://github.com/kaltura/server/pull/10168)
- Add `simulive` and manual live to the "broadcasting now" report (https://github.com/kaltura/server/pull/10161)
- PLAT-11221: Add option to delete the recorded live entry automatically when deleting live entry (https://github.com/kaltura/server/pull/10160)
- `kBaseMemcacheConf`: Support persistent/flags (https://github.com/kaltura/server/pull/10159)
- REACH2-959: Allow resubmission of entry vendor task (https://github.com/kaltura/server/pull/10158)
- PLAT-22452: Support Thumbs from images stored on S3 (https://github.com/kaltura/server/pull/10157)
- SUP-24970: `KEmailNotificationCategoryRecipientEngine` - get `max_pages_to_scan` value from config, default is 7 (https://github.com/kaltura/server/pull/10156)
- PLAT-11197: Add Bumper plugin (https://github.com/kaltura/server/pull/10155)
- `KCurlWrapper` - allow relative redirect operations (https://github.com/kaltura/server/pull/10152)
- get `playbackTypes` from filter in case it is missing in the report definition (https://github.com/kaltura/server/pull/10151)
- SUP-24940: Fix language codes to prevent duplications (https://github.com/kaltura/server/pull/10150)
- Allow 8K resolution source ingestion (https://github.com/kaltura/server/pull/10147)
- `KChunkedEncodeMemcacheWrap`: `FetchNextJob()` default `fetchRangeRandMax` param set to 20 (https://github.com/kaltura/server/pull/10146)
- Fix `getClearTempPath()` (https://github.com/kaltura/server/pull/10144)
- `getDetails()`: Support manual live (https://github.com/kaltura/server/pull/10142)
- PLAT-11244: Do not add captions to child manifest if `disableCaptions` flag is set to `true` (https://github.com/kaltura/server/pull/10141)
- SUP-24985: fix `getImportUrl()` (https://github.com/kaltura/server/pull/10140)
- FEC-10567: Bundle builder - better error handling/reporting (https://github.com/kaltura/server/pull/10139)
- PLAT-22449: Only access `remoteMemCache` if a value is requested (https://github.com/kaltura/server/pull/10138)
- PLAT-11119: Kaltura SSO server - support login via POST (https://github.com/kaltura/server/pull/10134)
- Support multiple CDN ratios on a single account (https://github.com/kaltura/server/pull/10132)
- PLAT-22444: `EntryVendorTask::preSave()` - Remove entry duration update (https://github.com/kaltura/server/pull/10130)
- PLAT-22426: use default filter when getting MRSS entry (https://github.com/kaltura/server/pull/10129)
- `getLiveStreamConfigurations()`: Detect protocol using `requestUtils::getProtocol()` by default (https://github.com/kaltura/server/pull/10127)
- Introduced `myCloudUtils::shouldExportThumbToCloud()` (https://github.com/kaltura/server/pull/10126)
- PLAT-22441: Fix in `captionAsset::list()` when user is not entitled (https://github.com/kaltura/server/pull/10125)
- PLAT-22429: Return an API error when the DB cannot be accessed (https://github.com/kaltura/server/pull/10124)
- PLAT-22428 and PLAT-22428: `document.addFromUploadedFile()` - enforce file type restriction (https://github.com/kaltura/server/pull/10123)
- KAVA realtime reports - add query cache (https://github.com/kaltura/server/pull/10015)

* Mon Nov 9 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.11.0-2
- PLAT-11190: Correctly create thumbnail destination path (https://github.com/kaltura/server/pull/10119)
- PLAT-22437-Reach: Fix transcription addition (https://github.com/kaltura/server/pull/10116)
- KCurlWrapper fixes (https://github.com/kaltura/server/pull/10113)
- `KalturaRequestDeserializer`: call `validateFile()` (https://github.com/kaltura/server/pull/10112)
- Add the server `time()` to x-kaltura-session header (https://github.com/kaltura/server/pull/10109)
- sphinx_log: Add DC,ID index and force it (https://github.com/kaltura/server/pull/10108)
- `KFFMpegMediaParser`: Handle `S3` paths in `checkForScanType()` (https://github.com/kaltura/server/pull/10103)
- PLAT-11259: Init `kUser` in case user ID or partner ID were changed (https://github.com/kaltura/server/pull/10102)
- AWS: Add FFmpeg reconnect params to support error recovery when working with remote files (https://github.com/kaltura/server/pull/10100)
- PLAT-11113: Thumbnail adapter handling of `src_x, src_y, src_h, src_w` (https://github.com/kaltura/server/pull/10098)
- PLAT-11266: Fix `loadLanguageCodeMap()`: verify file exists (https://github.com/kaltura/server/pull/10095)
- SUP-24553: `checkForScanType()` - fix detection (https://github.com/kaltura/server/pull/10094)
- PLAT-11257: Always require `OTP` if `getUseTwoFactorAuthentication()` returns true (https://github.com/kaltura/server/pull/10093)
- PLAT-11256: Exit with error when preview page is disabled (https://github.com/kaltura/server/pull/10090)
- PLAT-11258: Limit number of failing `OTP` login attempts (https://github.com/kaltura/server/pull/10088)
- PLAT-11257: `OTP` login - throw an exception if user doesn't exist (https://github.com/kaltura/server/pull/10087)
- Reach: Allow vendor accounts to fetch catalog item data when using a response profile (https://github.com/kaltura/server/pull/10086)
- Sphinx populate: issue a separate query per DC (https://github.com/kaltura/server/pull/10085)
- PLAT-11256: Add option to disable preview page using config (https://github.com/kaltura/server/pull/10084)
- Export script: Support list of file sync keys (https://github.com/kaltura/server/pull/10083)
- SUP-24521: When `FEATURE_DISABLE_CATEGORY_LIMIT` is enabled, its indexed entries do not get the privacy-context if their status is pending (https://github.com/kaltura/server/pull/10082)
- AWS: Validate resolved file sync is pending before returning it (https://github.com/kaltura/server/pull/10080)
- PLAT-11249: `shortlink.list()` - remove `WIDGET_SESSION_PERMISSION` (https://github.com/kaltura/server/pull/10079)
- SUP-24583: Fixing thumbnails capture (https://github.com/kaltura/server/pull/10077)
- PLAT-11171: Get expiry of exported files according to partner config (https://github.com/kaltura/server/pull/10075)
- aws: Use legacy cloud storage ID when pushing src to remote and converting from remote (https://github.com/kaltura/server/pull/10074)
- PLAT-11246: Add support for raw action in case the file sync exists in shared DC (https://github.com/kaltura/server/pull/10069)
- `KCurlWrapper` cleanup (https://github.com/kaltura/server/pull/10068)
- AWS: Shared DC file syncs should also served as remote DC (https://github.com/kaltura/server/pull/10067)
- AWS: Prefer shared file sync for chunk convert flow only (https://github.com/kaltura/server/pull/10066)
- AWS: Do not use remote convert flow in `KAsyncConvert.convert()` (https://github.com/kaltura/server/pull/10060)
- PLAT-11246: Only redirect raw requests to packager if the file exists in shared storage (https://github.com/kaltura/server/pull/10058)
- kava - Add users registration info enrichment (https://github.com/kaltura/server/pull/10056)
- SUP-23292: Access control `SiteRestriction` - use the entry id in order to identify the partner ID when a KS isn't present (https://github.com/kaltura/server/pull/10055)
- plat-11245: [KMS->my-media] user can't see content that he is co-editor of, unless the content has been published (https://github.com/kaltura/server/pull/10052)
- Don't create file sync in shared DC if `sharedPath` was not provided on `jobData` (https://github.com/kaltura/server/pull/10050)
- REACH2-970: Add languages (https://github.com/kaltura/server/pull/10047)
- PLAT-11243: Validate user is allowed to edit entry assets (https://github.com/kaltura/server/pull/10046)
- No-Plat: Delete tmp local merged video file in case concat failed to save disk space (https://github.com/kaltura/server/pull/10045)
- PLAT-11241: Support reconvert operation from `S3` (https://github.com/kaltura/server/pull/10044)
- CLOUDMGT-893: Source to `S3` flow + convert directly from `S3` (https://github.com/kaltura/server/pull/10043)
- Source to `S3` flow + convert directly from `S3` (https://github.com/kaltura/server/pull/10042)
- VIRTC-655: `getLiveStatus()` - support `simulive` (https://github.com/kaltura/server/pull/10038)
- Simulive: Add offset support (https://github.com/kaltura/server/pull/10037)
- Add exception for entry not found in `getPlaybackContext` action (https://github.com/kaltura/server/pull/10035)
- PLAT-11190: Thumbnail creation on `S3` (https://github.com/kaltura/server/pull/9903)
- PSVAMB-16978: Update LC conversion profile (https://github.com/kaltura/server/pull/9806)

* Mon Nov 2 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.11.0-1
- Ver Bounce to 16.11.0

* Mon Oct 26 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.10.0-3
- serveFlavorAction: Round the initial segment time (https://github.com/kaltura/server/pull/10028)
- PLAT-11232: Support alt configuration for base url for local volume (https://github.com/kaltura/server/pull/10027)
- VIRTC-587: `Simulive` - set initial segment index for `simulive` (https://github.com/kaltura/server/pull/10026)
- PLAT-11214: Ensure at least 2 secs passed since the last MRP run (https://github.com/kaltura/server/pull/10025)
- Doc convert scripts: Use `WMI` for listing processes (https://github.com/kaltura/server/pull/10024)
- REACH2-965: Set caption asset as default only if requested (https://github.com/kaltura/server/pull/10023)
- SUP-24570: `addFromUploadedFileAction()` - call `kFileUtils::dumpApiRequest()` if remote DC (https://github.com/kaltura/server/pull/10022)
- Set web/tmp/convert/$DIR to 775 (`kaltura.apache`) (https://github.com/kaltura/server/pull/10021)
- PLAT-11161: Remove calls that generate sig tokenized URL (https://github.com/kaltura/server/pull/10020)
- Support loading slave list dynamically from DB config (https://github.com/kaltura/server/pull/10016)
- SUP-24553: Fix Interlace issue (https://github.com/kaltura/server/pull/10008)
- PLAT-11076: Generate thumbnails from sources at `S3` via `ffmpeg` using signed URL (https://github.com/kaltura/server/pull/10007)
- PLAT-11225: manual live stream - handle backups (https://github.com/kaltura/server/pull/10006)
- VIRTC-490: add `postEnd` to event (https://github.com/kaltura/server/pull/10004)
- Chunk convert: `fopen` video concat + retry chunks + video file to local tmp folder (https://github.com/kaltura/server/pull/10001)
- PLAT-11214: Ensure at least 2 secs passed since the last MRP run (https://github.com/kaltura/server/pull/10000)
- output `Memcache` stats to log after bootstrap (https://github.com/kaltura/server/pull/9997)
- FixChunks and Merge retries (https://github.com/kaltura/server/pull/9996)
- AWS: Fix bug caused when UNIX timestamp drifts between setting `httpDate` and `X-Amz-Date` (https://github.com/kaltura/server/pull/9992)
- PLAT-11161: Add download support using the packager by adding kaltura `tokenizer` and `recognizer` to sign serve URLs (https://github.com/kaltura/server/pull/9990)
- PLAT-11205: Thumbnail generation using packager (https://github.com/kaltura/server/pull/9989)
- SUP-24282: Fix clipping and treaming (https://github.com/kaltura/server/pull/9988)
- VIRTC-166: `simulive` improvements (https://github.com/kaltura/server/pull/9986)
- Ignore validate local source on `replaceResource` (https://github.com/kaltura/server/pull/9984)
- query cache: increase query master threshold (https://github.com/kaltura/server/pull/9982)
- PLAT-11220: Support private indices per partner (https://github.com/kaltura/server/pull/9979)
- AWS: Support max session duration allowed when assuming role `ASSUME_ROLE_CREDENTIALS_EXPIRY_TIME` (https://github.com/kaltura/server/pull/9977)
- PLAT-11207: Fix export `flavorAsset` when the file sync does not exist in the other DC (https://github.com/kaltura/server/pull/9966)
- SUP-22605: Kaltura Cross Distribution Connector - Do not set `parentEntryId` on `targetEntry` (https://github.com/kaltura/server/pull/9964)
- AWS: Support upload retry with rand sleep + avoid calling `mkdir()` (https://github.com/kaltura/server/pull/9961)
- Propus-16.9.0-PLAT-11215: `Simulive` - `getPlayableSimuliveEvent()`  (https://github.com/kaltura/server/pull/9960)
- Fix support for chunk to S3 flow when using key and token (https://github.com/kaltura/server/pull/9958)
- Fix chunk convert onto `s3` (https://github.com/kaltura/server/pull/9954)
- CLOUDMGT-750: Fix thumbnail generation for playlist (https://github.com/kaltura/server/pull/9945)
- REACH2-948: Boolean event notification condition rule should not be cloned from source partner (https://github.com/kaltura/server/pull/9773)
- WEBC-2048: Allow dynamic batch hostname config with wildcard and dynamic scheduler loading (https://github.com/kaltura/server/pull/9699)
- SUP-21354: Log unknown encoding for all CSV bulk upload types (https://github.com/kaltura/server/pull/9655)

* Wed Oct 21 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.10.0-1
- Ver Bounce to 16.10.0

* Wed Oct 14 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.9.0-1
- PLAT-11215: HotFix - simulive fix playable (https://github.com/kaltura/server/pull/9955)
- Fix chunk convert flow to S3 + reduce `kconf` calls during chunk convert + fix `sharedMgr` bugs (https://github.com/kaltura/server/pull/9948)
- `KAsyncExtractMedia`: Clean up tmp complexity eval files (https://github.com/kaltura/server/pull/9947)
- Update `roku_syndication.xslt` (https://github.com/kaltura/server/pull/9943)
- Export: make sure custom data fields are not lost (https://github.com/kaltura/server/pull/9942)
- SUP-24198 and SUP-24358: Support generating download URL based on configuration for remote file syncs (https://github.com/kaltura/server/pull/9941)
- PLAT-11182: verify job DC is not null (https://github.com/kaltura/server/pull/9938)
- Set one flavor only to `simulive` (https://github.com/kaltura/server/pull/9937)
- CLOUDMGT-750: failing packager capture thumbnail when we get a file with size 0 (https://github.com/kaltura/server/pull/9936)
- PLAT-11193-removal: Remove import through S3 transfer manager (https://github.com/kaltura/server/pull/9935)
- PLAT-11182: take batch version from dc config in case we add job with… (https://github.com/kaltura/server/pull/9934)
- `serveFlavor`: support skipping packager cache (https://github.com/kaltura/server/pull/9932)
- VIRTC-166: `Simulive` - change duration calculation (https://github.com/kaltura/server/pull/9930)
- VIRTC-166: `isLive()` condition cache fix (https://github.com/kaltura/server/pull/9929)
- PLAT-11196: Support download action when content is on S3 (https://github.com/kaltura/server/pull/9928)
- VIRTC-166: `Simulive` - `isLive()` conditional cache (https://github.com/kaltura/server/pull/9927)
- VIRTC-166: Print event details and change units (https://github.com/kaltura/server/pull/9925)
- Move clip to array (https://github.com/kaltura/server/pull/9920)
- CLOUDMGT-846-facebook: distribution with caption (https://github.com/kaltura/server/pull/9919)
- CLOUDMGT-845: FFmpeg concat - whitelist `tls` protocol (https://github.com/kaltura/server/pull/9917)
- REACH2-955: Performing the serve action from the admin console (https://github.com/kaltura/server/pull/9916)
- PLAT-11172: Extract media with `fprobe` (https://github.com/kaltura/server/pull/9914)
- SUP-24073: Prevent execution of `sftp` command if passphrase exists (https://github.com/kaltura/server/pull/9912)
- VIRTC-166: Add `Simulive` ability (https://github.com/kaltura/server/pull/9906)
- PLAT-11195: Support storing upload chunks in S3 object storage (https://github.com/kaltura/server/pull/9905)
- PLAT-11191: Support reconvert when sec file exists only in S3 (https://github.com/kaltura/server/pull/9901)
- PLAT-11187: Support passing cloud storage config to batch + fix bugs caused due to auto merge (https://github.com/kaltura/server/pull/9898)
- Chunked encode - Fix auto merge check (https://github.com/kaltura/server/pull/9897)
- Add `thumbAssetId` when generating thumb unique path (https://github.com/kaltura/server/pull/9894)
- PLAT-11191: Support reconvert when source exists only in S3 (https://github.com/kaltura/server/pull/9890)
- PLAT-11189: Filter out old upload tokens when calling upload token list with `fileName` and `statusEqual` (https://github.com/kaltura/server/pull/9884)
- Block upload resume operation for uploads created more than max resume time allowed (https://github.com/kaltura/server/pull/9882)
- SUP-23931: `getPlaybackContext` supply correct delivery profile (https://github.com/kaltura/server/pull/9875)
- PLAT-11176: Enforce HTTPS on partner in the cache layer (https://github.com/kaltura/server/pull/9869)
- Reduce file operations when handling chunk upload (https://github.com/kaltura/server/pull/9868)
- CLOUDMGT-750: Fix thumbnail for playlists (https://github.com/kaltura/server/pull/9864)
- PLAT-11177: Get correct DC ID (https://github.com/kaltura/server/pull/9863)
- Split shared convert dir based on entry ID suffix (https://github.com/kaltura/server/pull/9860)
- Preview action - add access control validation (https://github.com/kaltura/server/pull/9851)
- `kUploadTokenMgr:handleResume()`: Change lock logic (https://github.com/kaltura/server/pull/9850)
- control Concurrent Multipart Connections (https://github.com/kaltura/server/pull/9846)
- Verify dir exists before trying to download the file (https://github.com/kaltura/server/pull/9826)
- ChunkedEncode: Create chunk on local temp file (https://github.com/kaltura/server/pull/9823)
- Override chunk convert flow if entry duration is more than is allowed (https://github.com/kaltura/server/pull/9817)
- Support fetching file resolved as external when running convert (https://github.com/kaltura/server/pull/9816)
- feat(FEC-10420): Support playlist auto/iframe embed (https://github.com/kaltura/server/pull/9811)
- PLAT-11164: `basEentry.list()` fallback handling (https://github.com/kaltura/server/pull/9810)
- Beacon rotation script fix when index doesn't exists (https://github.com/kaltura/server/pull/9807)
- SUP-23608: `createTempEntryForClip()` - call `setIsTemporary(true)` (https://github.com/kaltura/server/pull/9805)
- PLAT-11165: Fix root path in `s3PathManager` and remove `kS3SharedPathManager` (https://github.com/kaltura/server/pull/9803)
- PSVAMB-15535: Update DB regardless of cache (https://github.com/kaltura/server/pull/9801)
- PLAT-11160: Add user custom data params: `registrationInfo` and `attendanceInfo` (https://github.com/kaltura/server/pull/9800)
- PLAT-11143: Prevent skipping on file syncs for export to cloud (https://github.com/kaltura/server/pull/9719)
- PLAT-11140: Confirm that path is not empty for preferred and fallback storages (https://github.com/kaltura/server/pull/9715)
- PLAT-11139 - Fix thumbnail adapter for entries without width and height (https://github.com/kaltura/server/pull/9714)
- PLAT-11125: Add fallback storage support in `serveFlavor` and allow requests using auth header (https://github.com/kaltura/server/pull/9713)
- PLAT-11135: Add `objectId` param to `serveFile` (https://github.com/kaltura/server/pull/9712)
- Add user engagement report for webcast analytics (https://github.com/kaltura/server/pull/9711)
- PLAT-11082: New parameter on KalturaAsset - `actualFileSizeOnDisk` (https://github.com/kaltura/server/pull/9705)
- AN-1392: Webcast analytics reports (https://github.com/kaltura/server/pull/9702)
- Add timestamp auth header validation and don't cache failed requests (https://github.com/kaltura/server/pull/9700)
- Align auth tokens between API & UDRM (https://github.com/kaltura/server/pull/9692)
- Move entry validation to top of method to avoid fatal errors (https://github.com/kaltura/server/pull/9688)
- PLAT-11072: Add `S3_arn_role` to batch configuration (https://github.com/kaltura/server/pull/9683)
- SUP-23006: Allow calling `isLiveAction` without protocol, check if at least one stream is live (https://github.com/kaltura/server/pull/9682)
- PLAT-11117- Add section prefix filter to the beacon index rotation script (https://github.com/kaltura/server/pull/9680)
- PLAT-11106: Delete local file sync siblings only after all jobs on entry finished (https://github.com/kaltura/server/pull/9678)
- REACH2-917: When cloning reach profile to the same partner, copy all rules (https://github.com/kaltura/server/pull/9677)
- PLAT-11098 - Show diff of `confMaps` in admin console before submitting (https://github.com/kaltura/server/pull/9676)
- LIV-197: Output `adminTag` live limits to logs (https://github.com/kaltura/server/pull/9675)
- PLAT-11115: Update beacon rotation index to create indices for new machines (https://github.com/kaltura/server/pull/9674)
- PLAT-11044: Prevent service dispatching upon invalid JSONP callback (https://github.com/kaltura/server/pull/9673)
- PLAT-11086: Add `EnforceDelivery` for `RemotePlaybackSources` (https://github.com/kaltura/server/pull/9672)
- PLAT-10924: Support streaming a specific source from the Video Conference to Kaltura (https://github.com/kaltura/server/pull/9667)
- SUP-22711: `kAssetUtils:getFileName()` - Use `cdnUrl` from map if exist (https://github.com/kaltura/server/pull/9648)
- PLAT-11072 - Load `s3arn` from task config (https://github.com/kaltura/server/pull/9616)

* Sun Aug 9 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.8.0-1
- PLAT-10924: Stream a specific video conference source (https://github.com/kaltura/server/pull/9663)
- PLAT-10924: Support sip dual stream (https://github.com/kaltura/server/pull/9661)
- PLAT-10924: VCI modifications (https://github.com/kaltura/server/pull/9652)
- AN-1448: Add filtered users to CSV report (https://github.com/kaltura/server/pull/9651)
- FEC-10291: Migrate Analytics Plugins Injection from Kaltura Player to Server (https://github.com/kaltura/server/pull/9650)
- PLAT-11073: Thumbnail resize - handle cases where height or width is 0 (https://github.com/kaltura/server/pull/9649)
- PLAT-10731: Configurable live `segmentDuration` and `dvrWindowSize` (https://github.com/kaltura/server/pull/9647)
- PLAT-11090: adjusted chunk timeout (https://github.com/kaltura/server/pull/9645)
- Do not round `fromDate/toDate` (in order to get the same results both from KMC and API) (https://github.com/kaltura/server/pull/9644)
- PLAT-11089: FFmpeg 4.2.2 regression - metadata mapping (https://github.com/kaltura/server/pull/9643)
- PLAT-11043: Allow updating `KalturaPartner.additionalParams` (https://github.com/kaltura/server/pull/9642)
- LIV-197: Dynamically change live limits (https://github.com/kaltura/server/pull/9641)
- Support loading sphinx config using `kConf` (https://github.com/kaltura/server/pull/9640)
- Support redirecting all `embedIframeJs` action via redirect host and overriding dc list values (https://github.com/kaltura/server/pull/9638)
- PLAT-11085: Fix `Youtube` CSV distribution failure when `thumbAssetId` is empty (https://github.com/kaltura/server/pull/9637)
- `KalturaDeliveryProfileCondition`: set `type` to `ConditionType::DELIVERY_PROFILE` in the constructor (https://github.com/kaltura/server/pull/9635)
- PSVAMB-14576: Drop folder enhancements (https://github.com/kaltura/server/pull/9634)
- REACH2-911: `KAsyncReachJobCleaner.php` - clean pending and processing stuck jobs (https://github.com/kaltura/server/pull/9631)
- AN-1345: Add unique viewers metric (https://github.com/kaltura/server/pull/9630)
- Support overriding file group in a `kAsyncImport` job (https://github.com/kaltura/server/pull/9629)
- AN-1345: Add unique viewers metric (https://github.com/kaltura/server/pull/9628)
- AN-1449: add `customVars` to `playmanifest` beacon (https://github.com/kaltura/server/pull/9627)
- SUP-21926: Ignore entries with `display_in_search=-1` in elastic free text search (https://github.com/kaltura/server/pull/9626)
- PLAT-10924: Expose SIP source type to client (https://github.com/kaltura/server/pull/9625)
- PLAT-10924: Expose SIP source type to client (https://github.com/kaltura/server/pull/9624)
- SUP-21354: `BulkUploadUserEngineCsv` - log unknown encoding errors (https://github.com/kaltura/server/pull/9623)
- LIV-167: Enable streaming both primary + backup on the same cluster (2 RTMP pods, 2 packagers) (https://github.com/kaltura/server/pull/9622)
- Export to remote storage by parsing entry list from file (https://github.com/kaltura/server/pull/9619)
- PLAT-11013: `quiz->serve()` - fix invalid PDF (https://github.com/kaltura/server/pull/9611)
- PLAT-10876: New KMS user reset password link (https://github.com/kaltura/server/pull/9606)
- PLAT-11037: Support using different batch versions when jobs are added|pulled (https://github.com/kaltura/server/pull/9565)

* Sun Jul 26 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.7.0-10
- Nightly build.

* Sun Jul 26 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.7.0-9
- PSVAMB-13444: KAVA DB name can be different than "kava" (https://github.com/kaltura/server/pull/9612)
- PLAT-11067: Fix thumbnail adapter with encrypted file (https://github.com/kaltura/server/pull/9610)
- Export to remote storage by entry list file (https://github.com/kaltura/server/pull/9609)
- PLAT-11057: Remove check for the existence of private storage profiles on export to periodic storage (https://github.com/kaltura/server/pull/9608)
- PLAT-11055: Thumbnail adapter fixes (https://github.com/kaltura/server/pull/9607)
- Support defining different mount point based on partner ID (https://github.com/kaltura/server/pull/9605)
- WEBC-1925: Add description to `qna` response profile user (https://github.com/kaltura/server/pull/9604)
- Elastic population script fix (https://github.com/kaltura/server/pull/9602)
- PLAT-11057: Delete local file syncs siblings only if partner is dedicated AWS (https://github.com/kaltura/server/pull/9601)
- PLAT-10953: Add privileges field to widget (https://github.com/kaltura/server/pull/9600)
- SUP-23001: Export to periodic storage once file sync is ready (https://github.com/kaltura/server/pull/9599)
- moveConvertJobs - Exclude `PIDs` param (`excludePartnerIds`) for auto mode (https://github.com/kaltura/server/pull/9598)
- REACH2-900: Add lock to `entryVendorTask.add()` action (https://github.com/kaltura/server/pull/9597)
- KAVA - round filter `fromDay/fromDate` to partner creation date (https://github.com/kaltura/server/pull/9596)
- WEBC-1925: Add more user data to `QnA` response profile (https://github.com/kaltura/server/pull/9593)
- PLAT-11027 - `compatcheck` new alerts on new server errors (https://github.com/kaltura/server/pull/9591)
- Update `deploy_v2.php` (https://github.com/kaltura/server/pull/9590)
- SUP-21781: For VOD get single edge server for all flavors (https://github.com/kaltura/server/pull/9589)
- PLAT-11052: Thumbnail adapter when there isn't vid sec or vid slices (https://github.com/kaltura/server/pull/9588)
- REACH2-901: Enable reach request with price 0 even if the credit expired (https://github.com/kaltura/server/pull/9586)
- Plat-11051: Release lock in case we failed processing the thumbnail (https://github.com/kaltura/server/pull/9584)
- PLAT-11048: Temporarily disable content type setting on notifications (https://github.com/kaltura/server/pull/9583)
- Add new permission allowing admin KS to set `userId` on new cue point (https://github.com/kaltura/server/pull/9581)
- PLAT-11048: Fix http notification if no `dataType` (https://github.com/kaltura/server/pull/9580)
- REACH2-879: Limit export reach requests to 9999 results (https://github.com/kaltura/server/pull/9575)
- PLAT-10924 - Handle Dual Stream (talking heads and screenshare) for `VCI` (https://github.com/kaltura/server/pull/9554)

* Tue Jul 14 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.7.0-1
- Ver Bounce to 16.7.0

* Wed Jul 8 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.6.0-1
- Ver Bounce to 16.6.0

* Mon Jun 29 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.5.0-15
- PLAT-10898: Storage profiles - add ability to block export entries by type (https://github.com/kaltura/server/pull/9531)
- PLAT-11009: Explicit RTMP overriding per partner for SIP adp creation (https://github.com/kaltura/server/pull/9528)
- PLAT-11009: Explicit RTMP overriding per partner for SIP adp creation (https://github.com/kaltura/server/pull/9527)
- Apply dynamic granularity for topN query (https://github.com/kaltura/server/pull/9526)
- PLAT-10970: Set Kaltura auth time to expiry time (https://github.com/kaltura/server/pull/9525)
- Edit filter to include only live entries (https://github.com/kaltura/server/pull/9524)
- PLAT-10997: If delete flag is set but the partner doesn't have additional storage profiles, export anyway (https://github.com/kaltura/server/pull/9523)
- PLAT-11002 - Don't export sources to remote storage (https://github.com/kaltura/server/pull/9522)
- PLAT-11001: `prepareStorageProfilesForSort()`: Return `partnerIds` as an array (https://github.com/kaltura/server/pull/9521)
- PLAT-10998: Export assets to remote storage script (https://github.com/kaltura/server/pull/9519)
- SUP-22163: New script for deleting Webex files by recording id (https://github.com/kaltura/server/pull/9518)
- PLAT-10968: Add S3 serve support for stitched playlist and sequence (https://github.com/kaltura/server/pull/9516)
- PLAT-10932: Support logical or condition in advanced search (https://github.com/kaltura/server/pull/9514)
- SUP-22509: Revised caption asset logic (https://github.com/kaltura/server/pull/9510)
- Support time conversion in table reports (https://github.com/kaltura/server/pull/9508)
- PLAT-10957 - Support partial search in `description` field (https://github.com/kaltura/server/pull/9506)
- LIV-145: Add `partner.get()` permission to partner ID -5 (https://github.com/kaltura/server/pull/9505)
- AN-1388: Add avg bitrate to QOS overview report (https://github.com/kaltura/server/pull/9504)
- plat-10936: Extending `interactivity.get()` (https://github.com/kaltura/server/pull/9503)
- PLAT-10875: Allow additional parameters in partner creation (https://github.com/kaltura/server/pull/9502)
- SUP-22619: Make sure `clipTo` is part of the signature (https://github.com/kaltura/server/pull/9501)
- Fix deprecation errors and warnings (https://github.com/kaltura/server/pull/9498)
- Add hotspot click percentiles report (both for hotspot_clicked and `node_switch` events) (https://github.com/kaltura/server/pull/9491)
- Broadcast controller view - new reports (https://github.com/kaltura/server/pull/9440)

* Wed Jun 17 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.5.0-1
- Ver Bounce to 16.5.0

* Mon Jun 15 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.4.0-9
- Support GB units for usage in custom reports (https://github.com/kaltura/server/pull/9494)
- PLAT-10785: Handle attachment filename CRLF HTML chars (https://github.com/kaltura/server/pull/9493)
- PLAT-10897: `batchJob` - add `urgency` member (https://github.com/kaltura/server/pull/9487)
- REACH2-849: Added notification to be sent when caption is ready and all the conditions are fulfilled (https://github.com/kaltura/server/pull/9486)
- REACH2-678: Do not retrieve captions for `getPlaybackContext` when `displayOnPlayer` is false (https://github.com/kaltura/server/pull/9483)
- PLAT-10914: Support searching for terms in specific fields (https://github.com/kaltura/server/pull/9481)
- PLAT-10944: Export source once conversion is done (https://github.com/kaltura/server/pull/9480)
- PLAT-10914: Support excluding search group when using free text search (https://github.com/kaltura/server/pull/9477)
- Support S3 authentication using ARN role name  (https://github.com/kaltura/server/pull/9476)
- `KalturaConvertJobData`: store CPU usage stats (https://github.com/kaltura/server/pull/9475)
- PLAT-10934: Add v7 player UI Conf to KMC wrapper (https://github.com/kaltura/server/pull/9470)
- REACH2-871: Change to the way bulk upload result is displayed in REACH (https://github.com/kaltura/server/pull/9467)
- PATH-837: Add `PLAYBACK_BASE_PERMISSION` permission to `interactivity.get()` (https://github.com/kaltura/server/pull/9466)
- FEC-9495: Add canary version to `embedPlaykit` action (https://github.com/kaltura/server/pull/9461)
- REACH2-867: Support adding `captionAssetId` to translation `EntryVendorTask` (https://github.com/kaltura/server/pull/9459)
- PLAT-10943: Periodic export - update `lastId` when there're no hits in … (https://github.com/kaltura/server/pull/9456)
- PLAT-10782: deployment/uiconf/deploy_v2.php fix (https://github.com/kaltura/server/pull/9455)
- PLAT-10916: Add `user.validateHashKay()` (https://github.com/kaltura/server/pull/9454)
- PLAT-10933: Generate direct URL to packager with auth header for internal use (https://github.com/kaltura/server/pull/9451)

* Tue Jun 9 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.4.0-1
- Ver Bounce to 16.4.0

* Thu Jun 4 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.3.0-11
- Fix Admin Console and Chrome 83 bug - https://github.com/kaltura/server/pull/9473

* Tue Jun 2 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.3.0-9
- PLAT-10930: Add permission ANALYTICS_BASE to tag search (https://github.com/kaltura/server/pull/9453)
- PLAT-10938: MR infinite loop (https://github.com/kaltura/server/pull/9452)
- REACH2-863: Fix error in audit trail service (https://github.com/kaltura/server/pull/9450)
- PLAT-10935: Enable interactivity for RAPT playlist (https://github.com/kaltura/server/pull/9449)
- PLAT-10937: Fix crash that was introduced in PLAT-10780 (https://github.com/kaltura/server/pull/9448)
- Always check if `pathOnly` is sent before checking the second condition (https://github.com/kaltura/server/pull/9446)
- PLAT-10931: Use `serveFlavor` when exporting from remote storage periodic (https://github.com/kaltura/server/pull/9442)
- PLAT-10780: Make account owner the owner of all copied content from template partner (99) (https://github.com/kaltura/server/pull/9441)
- SUP-22038: OnPrem: Add `playsviews` cache update (https://github.com/kaltura/server/pull/9438)
- PLAT-10769: `lockFileSyncsAction`: set `updatedAt` (https://github.com/kaltura/server/pull/9437)
- LIV-114: Get max stream limit from partner (https://github.com/kaltura/server/pull/9436)
- REACH2-863: Add audit trail to admin console (https://github.com/kaltura/server/pull/9435)
- PLAT-10889: `kClipManager`: introduce `LOCK_EXPIRY` (https://github.com/kaltura/server/pull/9434)
- PLAT-10769: `KAsyncStoragePeriodicPurge`: add range to the query (https://github.com/kaltura/server/pull/9433)
- PLAT-10927: `playManifest`: Return local and remote flavors (https://github.com/kaltura/server/pull/9432)
- PLAT-10889 - `startConcat()` add locking mechanism during clip/trim flow (https://github.com/kaltura/server/pull/9431)
- PLAT-10919: Added `UserService::validateLoginDataParams()` (https://github.com/kaltura/server/pull/9430)
- PLAT-10920 chunked encoding updates (https://github.com/kaltura/server/pull/9429)
- PLAT-10895: Add storage class to `S3` uploaded objects (https://github.com/kaltura/server/pull/9425)
- REACH2-857: Import catalog item CSV from admin console (https://github.com/kaltura/server/pull/9424)
- PLAT-10913 - Handle `storagePriority` and local/external `fileSync` retrieval (https://github.com/kaltura/server/pull/9423)
- PLAT-10894: Periodically delete local file syncs that were exported (https://github.com/kaltura/server/pull/9420)
- PLAT-10892: Return S3 file location or local file path for `pathOnly` requests coming from `S3` supported packager (https://github.com/kaltura/server/pull/9419)
- Support external YouTube as entry source type in analytics reports (https://github.com/kaltura/server/pull/9416)
- PLAT-10890 - retrieve `lastFileSyncId` from DB in case it's not found in cache (https://github.com/kaltura/server/pull/9414)
- PLAT-10806: Introduced `kNetworkUtils::isAuthenticatedURI()` (https://github.com/kaltura/server/pull/9413)
- PLAT-10874: Add ability to set partner package type in cloud storage (https://github.com/kaltura/server/pull/9411)
- PLAT-10810: Export content using serve from local or remote (https://github.com/kaltura/server/pull/9376)
- QOE-256: update `QOE` error tracking (https://github.com/kaltura/server/pull/9286)
- QOE-254: update `QOE` experience (https://github.com/kaltura/server/pull/9285)
- Util script to move file syncs to the other DC(https://github.com/kaltura/server/pull/9274)

* Mon May 25 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.3.0-1
- Ver Bounce to 16.3.0

* Thu May 21 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.2.0-11
- Upgrade process should not require interactive inputs (https://github.com/kaltura/server/pull/9428)

* Mon May 18 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.2.0-9
- PLAT-10889: Entry replacement: pass assets rather than IDs to export (https://github.com/kaltura/server/pull/9412)
- Update myEntryUtils.class.php (https://github.com/kaltura/server/pull/9405)
- REACH2-845: Add Reach profile to audit trail (https://github.com/kaltura/server/pull/9404)
- PLAT-10846: Add captions export support for all remote storage types (https://github.com/kaltura/server/pull/9403)
- `serveFlavor` - support encrypted captions (https://github.com/kaltura/server/pull/9401)
- PLAT-10854: handle delivery profile IDs order in `playmanifest` and `playbackContext` according to partner configuration order and remote storage order (https://github.com/kaltura/server/pull/9400)
- Handle cases where the uploaded chunk partially overrides content that was already concatenated to the output file (https://github.com/kaltura/server/pull/9399)
- PLAT-10865: exclude invalid flavors when checking if we should delete… (https://github.com/kaltura/server/pull/9397)
- Check if `pcntl` is enabled before using it (https://github.com/kaltura/server/pull/9396)
- PLAT-10829 - DRM license URL handling (https://github.com/kaltura/server/pull/9393)
- REACH2-848: fix incorrect TAT displayed on REACH requests in admin console (https://github.com/kaltura/server/pull/9392)
- PLAT-10856 : Add `remotestorage` from global partner when searching by profile ID (https://github.com/kaltura/server/pull/9391)
- Batch mgr intercept `SIGINT` and `SIGTERM` (https://github.com/kaltura/server/pull/9389)
- PLAT-10683 - Add dedicated S3 path manager (https://github.com/kaltura/server/pull/9386)
- REACH2-853: Add missing fields to export file (https://github.com/kaltura/server/pull/9385)
- PLAT-10838: Add entry server node id to the M3U8 URL as `sessionId` (https://github.com/kaltura/server/pull/9380)
- PLAT-10835 - Handle `volume_map` and thumbs with remote packager (https://github.com/kaltura/server/pull/9370)


* Tue May 12 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.2.0-2
- Disable KMCng ES search by defaul as some ENVs may not have it.

* Tue May 12 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.2.0-1
- Ver Bounce to 16.2.0

* Sat Apr 4 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.0.0-1
- Nightly build.

* Fri Apr 3 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.0.0-1
- Nightly build.

* Fri Apr 3 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.0.0-1
- Ver Bounce to 16.0.0

* Fri Mar 27 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.20.0-1
- Add date of map creation in admin console (https://github.com/kaltura/server/pull/9297)
- PLAT-10758: `cuePointDeleted()` - avoid multiple queries in case of children (https://github.com/kaltura/server/pull/9296)
- `KalturaMonitorClient::prettyPrintCounters()` - additional session counters info (https://github.com/kaltura/server/pull/9295)
- SUP-19377: `ReachProfile::fulfillsRules()` PHP 5 fix  (https://github.com/kaltura/server/pull/9292)
- PLAT-10758: Avoid setting entry `updated_at` when deleting an entry (https://github.com/kaltura/server/pull/9291)
- PLAT-10759: Entry stuck in pending status when doing clip & trim on parent+child entry (https://github.com/kaltura/server/pull/9290)
- Write temp MP4 to local FS dir (/tmp) (https://github.com/kaltura/server/pull/9289)
- PLAT-10751 `DisableEntitlementForPlaylist` in execute playlist (https://github.com/kaltura/server/pull/9288)
- Update report title with `categories/playbackContext` IDs (https://github.com/kaltura/server/pull/9287)
- Fix zoom enum name convention (https://github.com/kaltura/server/pull/9284)
- PLAT-10752: `kUploadTokenMgr` - dismiss chunks that are of 0 bytes (https://github.com/kaltura/server/pull/9282)
- PLAT-10750: Avoid multiple handling of tags in case of entry deletion (https://github.com/kaltura/server/pull/9281)
- PLAT-10745- Segment duration part removed from packager URL for `LiveClusterMediaServerNode` (https://github.com/kaltura/server/pull/9280)
- AN-1273: Add `nodeIdsIn` to report filter (https://github.com/kaltura/server/pull/9279)
- SUP-19377: Prevent auto rule when `categoryEntry` is created (https://github.com/kaltura/server/pull/9278)
- PLAT-10726: Wild card entry name search does not return list of entries with matching names  (https://github.com/kaltura/server/pull/9277)
- SUP-21111: handle syndication feed according to syndication `confmap` (https://github.com/kaltura/server/pull/9276)
- PLAT-10747: Block chunk uploads that have more than 1000 chunks waiting to be concatenated (debug mode) (https://github.com/kaltura/server/pull/9272)
- Adding the playlist ID to the eligible entires (https://github.com/kaltura/server/pull/9271)
- PLAT-10746: Zoom chat files (https://github.com/kaltura/server/pull/9268)
- REACH2-727: Caption fix (https://github.com/kaltura/server/pull/9267)
- PLAT-10743: Correctly handle the `PRIVILEGE_DISABLE_ENTITLEMENT_FOR_PLAYLIST` privilege (https://github.com/kaltura/server/pull/9264)
- Handle `*` and `!` on Free text search and make free text search partial rather than exact match (https://github.com/kaltura/server/pull/9263)
- PLAT-10741: Fix HTTP 500 when calling `executeStaticPlaylist()` with an empty ID (https://github.com/kaltura/server/pull/9262)
- PLAT-10740: Fix permissions on `systemPartner` and jobs services (https://github.com/kaltura/server/pull/9260)
- Support entitlement check skip validation flag (https://github.com/kaltura/server/pull/9258)
- PLAT-10665: Reduce the `isLive` expiry cache when not live from `10` to `5` (https://github.com/kaltura/server/pull/9256)
- SUP-21037: update `kuser_id` column to match `sessionUserId = puser_id`, generate user on the fly if does not exist (https://github.com/kaltura/server/pull/9254)
- Add avg. drop-off metric for `TOP_USER_CONTENT` to use it for category analytics (https://github.com/kaltura/server/pull/9252)
- PLAT-10651: Added `disableentitlementforplaylist` privilege (https://github.com/kaltura/server/pull/9250)
- Add new report type for category analytics - highlights report (https://github.com/kaltura/server/pull/9248)
- PLAT-10739: Add an option for media repurposing to delete MR metadata(https://github.com/kaltura/server/pull/9245)
- webc-1856: Set `wasBroadcast` to true only when the entry was in 'live' mode (https://github.com/kaltura/server/pull/9243)
- plat-10128: As a Zoom user, I'd like to have my webinar recordings also transferred to Kaltura (https://github.com/kaltura/server/pull/9220)

* Mon Mar 16 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.19.0-14
- Increase `copy_partner_limit_metadata_profiles` default from 10 to 13 (https://github.com/kaltura/server/pull/9242)
- PSVAMB-11201: New event notification template - `HTTP_ENTRY_TRIM_JOB_FINISHED` (https://github.com/kaltura/server/pull/9239)
- When building current thumb path use the original `thumbName` without the `uniqid` (https://github.com/kaltura/server/pull/9237)
- PLAT-10625: Grant access to `listTemplates()` to the `ecdn` monitoring proxy partner (-7) (https://github.com/kaltura/server/pull/9236)
- PLAT-10736: `KAsyncDirectoryCleanup` fix (https://github.com/kaltura/server/pull/9234)
- PLAT-10725: Support defining multiple old thumb dirs (https://github.com/kaltura/server/pull/9224)
- PLAT-10725: Support defining multiple old thumb dirs (https://github.com/kaltura/server/pull/9223)
- PLAT-10725: Support defining multiple old thumb dirs (https://github.com/kaltura/server/pull/9222)
- PLAT-10733: `ElasticSearch` - Use reduced results (optimised) mode by default (https://github.com/kaltura/server/pull/9219)
- PLAT-10732: Avoid fatal error in auto archive when the live entry was deleted (https://github.com/kaltura/server/pull/9217)
- PLAT-10725: Support switching temp thumbnail dir to allow storage cleanup (https://github.com/kaltura/server/pull/9213)
- PLAT-10636 - Display `systemName` column to event notification in admin console (https://github.com/kaltura/server/pull/9212)
- feat(FEC-9465): `embedPlaykitJsAction (player v3)` - Internationalisation (i18n) (https://github.com/kaltura/server/pull/9211)
- PLAT-10610: `KalturaEntryServerNodeBaseFilter` - add `serverNodeIdNotIn` criterion (https://github.com/kaltura/server/pull/9208)
- KAVA: Get source from external data if external source is defined (https://github.com/kaltura/server/pull/9199)

* Wed Mar 4 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.19.0-1
- Ver Bounce to 15.19.0

* Mon Mar 2 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.18.0-9
- New entry source type for KMS GO (https://github.com/kaltura/server/pull/9209)
- PLAT-10720: `eSearch` - support external video type criteria (https://github.com/kaltura/server/pull/9207)
- PLAT-10718: Fixing internal server error when filtering by custom data (https://github.com/kaltura/server/pull/9205)
- PLAT-10714: `eSearch` support advanced search criteria (https://github.com/kaltura/server/pull/9203)
- SUP-21097: Use total result in case pager is not being sent (https://github.com/kaltura/server/pull/9202)
- PLAT-10713: Support Sphinx sticky session during read operations (https://github.com/kaltura/server/pull/9201)
- PLAT-10708: Duration type support (https://github.com/kaltura/server/pull/9200)
- PLAT-10706: `esearch` - add support for isQuiz filter (https://github.com/kaltura/server/pull/9197)
- PLAT-10697: Fix categories fields search when converting `KalturaMediaEntryFilter` to `eSearch` (https://github.com/kaltura/server/pull/9195)
- PLAT-10694: Add Linux batch for PDF doc conversion (https://github.com/kaltura/server/pull/9194)
- PLAT-10641: Fix `KalturaExternalMediaEntryFilter` (https://github.com/kaltura/server/pull/9193)
- Increase dictionary max chars to 4000 (https://github.com/kaltura/server/pull/9189)
- SUP-20389: Convert SCC caption time stamps (https://github.com/kaltura/server/pull/9185)
- FEC-9465: player v3: internationalisation (i18n) - player localisation (https://github.com/kaltura/server/pull/9182)
- New entry source types for KMS GO (https://github.com/kaltura/server/pull/8332)
* Mon Feb 24 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.18.0-1
- Ver Bounce to 15.18.0

* Mon Feb 17 2020 jess.portnoy@kaltura.com <Jess Portnoy> -
- AN-1230: limit report CSV file name length (https://github.com/kaltura/server/pull/9183)
- Add `LiveCluster` plugin (https://github.com/kaltura/server/pull/9180)
- PLAT-10646 : Indexing of caption incomplete if there is an empty line (https://github.com/kaltura/server/pull/9179)
- PLAT-10646 : Indexing of caption incomplete if there is an empty line (https://github.com/kaltura/server/pull/9178)
- WEBC-1820: Fix auto archive with self serve (https://github.com/kaltura/server/pull/9177)
- SUP-20392: Syndication fix `getEntryCount` (https://github.com/kaltura/server/pull/9176)
- PLAT-10626 - `ClipConcat` convert jobs should run with high priority (https://github.com/kaltura/server/pull/9174)
- PLAT-10626 - `ClipConcat` convert jobs should run with high priority (https://github.com/kaltura/server/pull/9173)
- REACH allowed for partner fix (https://github.com/kaltura/server/pull/9172)
- SUP-20392: Syndication fix (https://github.com/kaltura/server/pull/9170)
- PLAT-10642: `baseentry.list()` does not work when filtering by `KalturaEntryCaptionAdvancedFilter`  (https://github.com/kaltura/server/pull/9169)
- PLAT-10607 : indexing issues when building elastic index (https://github.com/kaltura/server/pull/9168)
- QOE-249: Add application version to report filter (https://github.com/kaltura/server/pull/9166)
- CSV Bulk Event Scheduling - Add option to specify resource by ID (https://github.com/kaltura/server/pull/9164)
- PSVAMB-10351: Drop folder item getting created for MRSS item that has no content node  (https://github.com/kaltura/server/pull/9163)
- QOE-237: Move error tracking reports to dynamic `datasource` (https://github.com/kaltura/server/pull/9162)
- PLAT-10265: Filter entries by captions (https://github.com/kaltura/server/pull/9160)
- SUP-20262: Print log limit size in GB instead of bytes (https://github.com/kaltura/server/pull/9159)
- SUP-20420: `groupUser.list()` returns wrong number of users (https://github.com/kaltura/server/pull/9158)
- SUP-19410: Change `noex` flavour extension by its container type (https://github.com/kaltura/server/pull/9156)
- reach-779: Allow catalog item pricing view from KMC (https://github.com/kaltura/server/pull/9155)
- PLAT-10609: Get entry after waiting in lock for replacement to end (https://github.com/kaltura/server/pull/9154)
- PLAT-10547: Add timezone to `liveentry` recording options for archive (https://github.com/kaltura/server/pull/9153)
- PLAT-10610: Avoid validation of NG live entry server node (https://github.com/kaltura/server/pull/9152)
- PLAT-10616: add exception catch for connection close and increase timeout (https://github.com/kaltura/server/pull/9151)
- SUP-20392: make syndication feed with dynamic playlist work the same as playlist `executeFromFilter` (https://github.com/kaltura/server/pull/9149)
- Add partner package to partner audit trail config (https://github.com/kaltura/server/pull/9148)
- Allow setting cache expiry on rule + allow setting multiple partner IDs for rule (https://github.com/kaltura/server/pull/9143)
- PLAT-10598: Return entry-server-node value to action level (https://github.com/kaltura/server/pull/9132)
- KMS-19964: Registration module report (https://github.com/kaltura/server/pull/9126)
- feat(FEC-9465): Internationalization (i18n) - player localization (https://github.com/kaltura/server/pull/9123)
- Orion-15.13.0-PLAT-10358: new live cluster server node (https://github.com/kaltura/server/pull/9067)


* Tue Feb 4 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.17.0-1
- Ver Bounce to 15.17.0

* Mon Feb 3 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.16.0-7
- SUP-20831: Fix `Media.List()` filter by `userIdNotEqual` (https://github.com/kaltura/server/pull/9142)
- QOE-215: Add OS + browsers to `reportInputFilter` (https://github.com/kaltura/server/pull/9141)
- SUP-19976: Increase `MAX_SQL_LENGTH` to 262144 (https://github.com/kaltura/server/pull/9140)
- SUP-20681: Fix Zoom `expire_in` incorrect calculation + small refactor (https://github.com/kaltura/server/pull/9139)
- PLAT-10387: Media Repurposing UX bug (https://github.com/kaltura/server/pull/9138)
- PLAT-10596: Add exceptions catch for rabbit connection and sending failures (https://github.com/kaltura/server/pull/9137)
- PLAT-10553: Lock replace entry flow to avoid race condition in case two flavours become ready at the same time (https://github.com/kaltura/server/pull/9135)
- QOE-215: Added filter by `ispIn` to `reportInputFilter` (https://github.com/kaltura/server/pull/9133)
- SUP-20262: Youtube connector - increase process timeout to 20 min for entries > 2GB (https://github.com/kaltura/server/pull/9131)
- `KalturaMediaInfo` - added missing 'colorSpace' prop (https://github.com/kaltura/server/pull/9130)
- View entry information within the player (https://github.com/kaltura/server/pull/9129)
- PLAT-10546: New notification template `Item_Pending_Moderation_Extended` (https://github.com/kaltura/server/pull/9128)
- youtubeFix: Increase `TIME_TO_WAIT_FOR_YOUTUBE_TRANSCODING` to 20 seconds (https://github.com/kaltura/server/pull/9127)
- REACH2-769: Remove `toDate` and `addOn` from unlimited credit (https://github.com/kaltura/server/pull/9125)
- SUP-20076: Handle copying cue points during clipping and trimming according to partner configuration (https://github.com/kaltura/server/pull/9124)
- PLAT-10583: Add `serverNodeIdIn` field to filter (https://github.com/kaltura/server/pull/9122)
- REACH2-761: Display 0 in reach profile credit edit page (https://github.com/kaltura/server/pull/9121)
- PLAT-10575: Create SIP `ADPs` with `RTMPS` stream URLs (https://github.com/kaltura/server/pull/9118)
- PLAT-10561: In the event of a conversion failure, verify that the entry exists before throwing `flavorAsset` exception (https://github.com/kaltura/server/pull/9113)
- PLAT-10510: Send `apimon` data to Kafka (https://github.com/kaltura/server/pull/9112)
- QOE reports fixes (https://github.com/kaltura/server/pull/9096)

* Tue Jan 28 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.16.0-1
- Ver Bounce to 15.16.0

* Tue Jan 7 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.15.0-1
- Ver Bounce to 15.15.0

* Mon Jan 6 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.14.0-19
- Ignore loading remote and local memcache instances when PHP_SAPI is CLI (https://github.com/kaltura/server/pull/9083)
- PLAT-10518: Zoom meeting participant owner match case insensitive (https://github.com/kaltura/server/pull/9082)
- `ReachFixCategoryEntry`: Validate that category entry status was modified (https://github.com/kaltura/server/pull/9081)
- KAVA: Set default value for descending ordering (https://github.com/kaltura/server/pull/9078)
- AP drop folder config not being saved (https://github.com/kaltura/server/pull/9077)
- SUP-19947: Zoom source file missing file extensions (https://github.com/kaltura/server/pull/9074)
- PLAT-10466: handle invalid chars for partner `describeYourself` field (https://github.com/kaltura/server/pull/9073)
- KAVA: align metric headers for QOE reports (https://github.com/kaltura/server/pull/9072)
- `confMaps`: `strtolower(hostname)` (https://github.com/kaltura/server/pull/9071)
- QOE-173: Add `eventVar1` to `datasource` dimension map (https://github.com/kaltura/server/pull/9070)
- Avoid trying to log FS access when monitor client is not loaded (https://github.com/kaltura/server/pull/9068)
- `ConfMaps` table fix modify content column size (https://github.com/kaltura/server/pull/9066)
- PLAT-10267: Zoom: case insensitive user matching (https://github.com/kaltura/server/pull/9065)
- PLAT-10453: Add apiMon stats for file operations (https://github.com/kaltura/server/pull/9063)
- KAVA: Add `entry_source` in order to identify interactive video entries (https://github.com/kaltura/server/pull/9061)
- REACH: updating credits (https://github.com/kaltura/server/pull/9060)
- PSVAMB-9373: `KalturaExportToCsvOptions()` additional documentation (https://github.com/kaltura/server/pull/9059)
- Enable range searches for entry::votes property (https://github.com/kaltura/server/pull/9058)
- PSVAMB-9513: Support expanding specific nodes in the AP feed (https://github.com/kaltura/server/pull/9056)
- Load batch service configuration from server/disc according to config (https://github.com/kaltura/server/pull/9053)
- Add recently played entries report (https://github.com/kaltura/server/pull/8994)
- Add partner ID check for storage profile retrieval by ID (https://github.com/kaltura/server/pull/8021)

* Fri Dec 27 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.13.0-1
- Fix mounts (https://github.com/kaltura/server/pull/9049)
- `category::getSphinxIndexName()`: fix index name (https://github.com/kaltura/server/pull/9047)
- Revert auto archive (WEBC-1574) (https://github.com/kaltura/server/pull/9044)
- PLAT-10373: Media Repurposing - Duplicate entries in the dry run mode (https://github.com/kaltura/server/pull/9038)
- SUP-20500: Handle temp recorded entry flavors when updating entry status (https://github.com/kaltura/server/pull/9035)
- Add report for QOE - funnel analysis (https://github.com/kaltura/server/pull/9034)
- Node avg completion rate should be based on `nodePlay` event rather than play event (https://github.com/kaltura/server/pull/9033)
- PLAT-10370: Fix PHP warning on notification template (https://github.com/kaltura/server/pull/9032)
- Don't block queries coming from batch servers (https://github.com/kaltura/server/pull/9031)
- Create abstract of `getEnvDc` (https://github.com/kaltura/server/pull/9029)
- PLAT-10373: Media Repurposing - Duplicated entries in the dry run (https://github.com/kaltura/server/pull/9026)
- SUP-20258: Fix 'invalid user' message when setting initial passwd for KMC admins (https://github.com/kaltura/server/pull/9025)
- SUP-20381: Check flavour type before switching and marking as ready (https://github.com/kaltura/server/pull/9023)
- Align `getPlaybackHost()` signature across `serverNode` types (https://github.com/kaltura/server/pull/9022)
- PLAT-10340: Add http header condition for access control profile (https://github.com/kaltura/server/pull/9020)
- LEC-10358: Refactor abstraction for `serverNode` (https://github.com/kaltura/server/pull/9019)
- REACH2-737: Reach: boolean event notification for privacy context (https://github.com/kaltura/server/pull/9017)
- Add new reports for interactive video (https://github.com/kaltura/server/pull/9010)
- Enable range searches for entry::votes property (https://github.com/kaltura/server/pull/9007)
- PLAT-10366: Fix event notifications not being triggered when vendors call `entryVendorTask.updateJob()` (https://github.com/kaltura/server/pull/9005)
- PLAT-10138: Add specific choice of audio language in multi audio entry VOD manifest (https://github.com/kaltura/server/pull/8987)

* Mon Dec 23 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.14.0-1
- Ver Bounce to 15.14.0

* Mon Dec 9 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.12.0-19
- PLAT-10357: partner -8 partner.get() permission (https://github.com/kaltura/server/pull/8998)
- PLAT-10108: Annotation cuepoints - grant access to all partners (https://github.com/kaltura/server/pull/8996)
- PLAT-10347: Make `baseentry.list()` work with elastic for scheduled tasks (https://github.com/kaltura/server/pull/8993)
- Fix placeholders (https://github.com/kaltura/server/pull/8992)
- PLAT-10246: Move batch configuration to maps (https://github.com/kaltura/server/pull/8990)
- PLAT-10354: Allow batch partner access to confmaps without user (https://github.com/kaltura/server/pull/8988)
- PLAT-10246: Move batch configuration to maps (https://github.com/kaltura/server/pull/8986)
- PLAT-10352: Batch alert exception fix (https://github.com/kaltura/server/pull/8985)
- PLAT-10246: Move batch configuration to maps (https://github.com/kaltura/server/pull/8984)
- PLAT-10351: Add permission for restore delete entry in admin console (https://github.com/kaltura/server/pull/8983)
- PLAT-10339: use replaced entry for flavors deletion on `handleConvertFailed` (https://github.com/kaltura/server/pull/8979)
- PLAT-10246: Move batch configuration to maps   (https://github.com/kaltura/server/pull/8978)
- PLAT-10246: move batch configuration to run from remote (https://github.com/kaltura/server/pull/8977)
- PLAT-10338: Don't copy flavors in case replacement entry was deleted (https://github.com/kaltura/server/pull/8976)
- PLAT-10282: Custom metadata for `userEntry`, defining `MetadataUserEntryPeer` (https://github.com/kaltura/server/pull/8975)
- PLAT-10317: Clip concat closer (https://github.com/kaltura/server/pull/8974)
- PLAT-10246: Move batch configuration to run from remote (https://github.com/kaltura/server/pull/8973)
- PLAT-10245: `confMaps` permissions (https://github.com/kaltura/server/pull/8968)
- Add new role file (https://github.com/kaltura/server/pull/8966)
- PLAT-10282: custom metadata for `userEntry` (https://github.com/kaltura/server/pull/8965)
- SUP-19884: Escape special characters for `WebVTT` compliance support (https://github.com/kaltura/server/pull/8963)
- PLAT-10346: Add new role for KMC Analytics (https://github.com/kaltura/server/pull/8962)
- PLAT-10345: Thumbnail crop gravity point fix (https://github.com/kaltura/server/pull/8961)
- PLAT-10245: Batch `confMaps` (https://github.com/kaltura/server/pull/8960)
- PLAT-10188: Add login using SSO to admin console (https://github.com/kaltura/server/pull/8957)
- AN-1108: Add force total count on users discovery realtime report (https://github.com/kaltura/server/pull/8956)
- SUP-20245: Fetch SUM(price) + price <> 0 to avoid reaching PHP `memory_limit` due to too many results + method improvements (https://github.com/kaltura/server/pull/8955)
- PLAT-10245: Moving configuration from file system to DB maps (https://github.com/kaltura/server/pull/8954)
- PLAT-10245: Moving configuration from file system to DB maps (https://github.com/kaltura/server/pull/8952)
- Deprecate analytics.query() (https://github.com/kaltura/server/pull/8951)
- PLAT-10292: Add new index to `entry_vendor_task` table to improve table query time (https://github.com/kaltura/server/pull/8950)
- PLAT-10341: If connection provided and its sphinx log connection use it instead of creating a new one to the master (https://github.com/kaltura/server/pull/8949)
- PLAT-10333: `disableentitlementforentry` fix (https://github.com/kaltura/server/pull/8948)
- PLAT-10055: output action for thumbnail (https://github.com/kaltura/server/pull/8947)
- Support working with PHP `FPM` (the default PHP `SAPI` with RHEL/CentOS 8) (https://github.com/kaltura/server/pull/8942)
- PLAT-10253: Thumbnail support for remote storage (https://github.com/kaltura/server/pull/8910)
- PLAT-10246: move batch configuration to run from remote (https://github.com/kaltura/server/pull/8896)
- fix(FEC-9326): Send actual player version, not the client lib ver (https://github.com/kaltura/server/pull/8847)

* Wed Nov 27 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.12.0-1
- Ver Bounce to 15.12.0

* Mon Nov 25 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.11.0-9
- PLAT-10332: Invalidate flavor cache when relinking assets on replacement (https://github.com/kaltura/server/pull/8941)
- PLAT-10322: Use replaced entry ID for for temp flavors deletion and other finished conversion tasks (https://github.com/kaltura/server/pull/8940)
- PLAT-10332: Invalidate flavor cache when relinking assets on replacement (https://github.com/kaltura/server/pull/8939)
- PLAT-10294: Optimize slow MySQL query when fetching `batch_job_log` records (https://github.com/kaltura/server/pull/8937)
- SUP-20245: Add Price <> 0 when fetching vendor tasks to avoid returning unnecessary results, which may exceed the `memory_limit` value (https://github.com/kaltura/server/pull/8935)
- Event notification: Fix a warning caused by unhandled flow (https://github.com/kaltura/server/pull/8932)
- PLAT-10303: Privacy context and category names are not indexed on entry in `setContent()` (https://github.com/kaltura/server/pull/8930)
- SUP-19501: Clone file asset with the file sync (https://github.com/kaltura/server/pull/8929)
- PLAT-10318: Don't create a `batchJobSep` on boolean event notifications (https://github.com/kaltura/server/pull/8925)
- Add permission `RATING_LIST_ADMIN` const (https://github.com/kaltura/server/pull/8924)
- PLAT-10316: Don't create `entryVendorTasks` for media which is not of type video or audio (https://github.com/kaltura/server/pull/8923)
- Handle stuck batch job lock objects (https://github.com/kaltura/server/pull/8922)
- PLAT-10283: Add `registration` `KalturaUserEntryType`  (https://github.com/kaltura/server/pull/8919)
- PSVAMB-8935: `kvote` enhancements (https://github.com/kaltura/server/pull/8918)
- KAVA - move `array_map` to `genericQueryEnrich()` (https://github.com/kaltura/server/pull/8917)
- AN-1106: Add `int_ids_only` flag + check IDs are of the same type (https://github.com/kaltura/server/pull/8916)
- AN-1106: Add top playback context VPaaS report (https://github.com/kaltura/server/pull/8915)
- PLAT-10256: Optimise quiz queries (https://github.com/kaltura/server/pull/8914)
- PLAT-10223: Optimise Sphinx queries (https://github.com/kaltura/server/pull/8912)
- KAVA - Add playback context IDs in to filter (https://github.com/kaltura/server/pull/8909)
- AN-1014: Add metrics to `TOP_PLAYBACK_CONTEXT` report (https://github.com/kaltura/server/pull/8908)
- PSVAMB-8935: New user-conscious 5-star rating functionality (https://github.com/kaltura/server/pull/8907)
- Allow more than one recipient in event notification template (https://github.com/kaltura/server/pull/8905)
- Fix timezone mapping (https://github.com/kaltura/server/pull/8902)
- PLAT-10304: Provide support for HEVC codecs generating HDR content (https://github.com/kaltura/server/pull/8901)
- SUP-19501: Clone file asset when cloning playlist (https://github.com/kaltura/server/pull/8900)
- AN-1093: Update reports with player impressions and unique viewers (https://github.com/kaltura/server/pull/8898)
- KAVA: `ctype_digit` is interpreted as the ASCII value of a single character (https://github.com/kaltura/server/pull/8891)
- PLAT-10245 - Move all configurations from file system to db map (https://github.com/kaltura/server/pull/8890)
- KAVA: Add QOE reports (https://github.com/kaltura/server/pull/8889)
- PLAT-10178: Replace and trim entry based on conversion profile readiness rules (https://github.com/kaltura/server/pull/8888)
- PLAT-10295: Remove REACH vendor partner permission when calling `entryVendorTask.list()` with a -2 KS (https://github.com/kaltura/server/pull/8885)
- SUP-18799: Add default recording conversion profile per partner (https://github.com/kaltura/server/pull/8866)
- PLAT-10223: Disable partner optimisations when optimisation addition… (https://github.com/kaltura/server/pull/8838)

* Tue Nov 12 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.11.0-1
- Nightly build.

* Tue Nov 12 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.11.0-1
- Ver Bounce to 15.11.0

* Sun Nov 10 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.10.0-14
- PLAT-10247: Update Kaltura favicon (https://github.com/kaltura/server/pull/8877)
- PLAT-10285: populateElasticFromLog - reduce log size  (https://github.com/kaltura/server/pull/8870)
- Limit sphinx slow queries (https://github.com/kaltura/server/pull/8869)
- PSVAMB-6815: `FeedDropFolder` plugin (https://github.com/kaltura/server/pull/8867)
- PLAT-10266: Add session counters to API response headers (https://github.com/kaltura/server/pull/8865)
- Add the option to use parameter for report granularity in custom report (https://github.com/kaltura/server/pull/8863)
- SUP-19359: Add `partner_id` to criteria when disabling criteria filter (https://github.com/kaltura/server/pull/8862)
- PLAT-10266: Added `HTTP_X_KALTURA_SESSION_COUNTERS` header (https://github.com/kaltura/server/pull/8860)
- PSVAMB-6815: `FeedDropFolder` plugin (https://github.com/kaltura/server/pull/8859)
- SUP-20050 + SUP-20061: `eSearch` add `last_played_at` and `plays` filters (https://github.com/kaltura/server/pull/8856)
- Add missing metrics for KMS (https://github.com/kaltura/server/pull/8855)
- SUP-19359: Allow retrieval of deleted scheduled resources (https://github.com/kaltura/server/pull/8854)
- REACH2-704: Enable access to `expectedFinishTime` in Sphinx (https://github.com/kaltura/server/pull/8853)
- PSVAMB-6815: `FeedDropFolder` plugin (https://github.com/kaltura/server/pull/8852)
- Update thumbnail locations and file sizes to match origin (https://github.com/kaltura/server/pull/8851)
- PLAT-10209: `eSearch` - Do not interpret single quotation marks as a request for an exact match (https://github.com/kaltura/server/pull/8850)
- Query cache triggers - add set function variable (https://github.com/kaltura/server/pull/8848)
- PLAT-10251: SSO redirect URL, data, new dedicated partner (https://github.com/kaltura/server/pull/8843)
- PLAT-10239: `eSearch` - support additional filter options (https://github.com/kaltura/server/pull/8841)
- PSVAMB-8780: Additional `kuser` filters (https://github.com/kaltura/server/pull/8840)
- PLAT-10213: Batch workers - validate file access permissions on remote storage volume (https://github.com/kaltura/server/pull/8831)
- Real-time reports (https://github.com/kaltura/server/pull/8829)
- PLAT-10206: Media repurposing - add retry mechanism for entry listing (https://github.com/kaltura/server/pull/8828)

* Thu Oct 31 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.10.0-1
- Ver Bounce to 15.10.0

* Mon Oct 28 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.9.0-18
- Disable access to `expectedFinishTime` in sphinx (https://github.com/kaltura/server/pull/8835)
- REACH2-704: Fix warning in reach dashboard (https://github.com/kaltura/server/pull/8834)
- PLAT-10242: Distribution - error on new profile (https://github.com/kaltura/server/pull/8830)
- REACH2-688: Add audio description file (https://github.com/kaltura/server/pull/8827)
- Pass `partnerId` when getting entry vendor task objects (https://github.com/kaltura/server/pull/8826)
- REACH2-704: Add `createdAt` to query in reach dashboard (https://github.com/kaltura/server/pull/8825)
- Reduce sphinx connections (https://github.com/kaltura/server/pull/8823)
- Reduce sphinx connections (https://github.com/kaltura/server/pull/8822)
- PLAT-10238: Added `getElasticEntryIndexNameForPartner()` (https://github.com/kaltura/server/pull/8821)
- REACH2-704: Fix warnings in reach dashboard (https://github.com/kaltura/server/pull/8820)
- PLAT-10231: Caption search - index all caption text on entry document (https://github.com/kaltura/server/pull/8819)
- PLAT-10234: eSearch - reduce results in partial search (https://github.com/kaltura/server/pull/8818)
- Handle stuck batch job lock objects (https://github.com/kaltura/server/pull/8817)
- REACH-649: Don't update `updatedAt` when daily credit sync process is done (https://github.com/kaltura/server/pull/8815)
- Limit bad query execution (https://github.com/kaltura/server/pull/8814)
- SUP-19641: issue `groupBy` instead of `topN` when ordering by `engagement_ranking` (https://github.com/kaltura/server/pull/8813)
- PLAT-9903: Add `lastplayed` lower then or equal or null (https://github.com/kaltura/server/pull/8812)
- SUP-19196: `children_count` on parent annotation cue point should decrease when deleting child (https://github.com/kaltura/server/pull/8811)
- PLAT-10216: Update last login when logging in via SSO (https://github.com/kaltura/server/pull/8806)
- REACH2-704: Reach new dashboard in admin console (https://github.com/kaltura/server/pull/8805)
- SUP-18336: Avoid getting external URL when storage protocol is missing (https://github.com/kaltura/server/pull/8804)
- PLAT-10222: Add session level caching to entry entitlement check (https://github.com/kaltura/server/pull/8801)
- PLAT-9903: Media Repurposing - `lastPlayedAtLessThanOrEqual` should include 0 plays as well (https://github.com/kaltura/server/pull/8800)
- SUP-19224: Add `map_between_objects` values to `KalturaPager.php` (https://github.com/kaltura/server/pull/8796)
- PLAT-10214: Should `unsetMediaServer` only when playable entry `server_node` doesn't exist (https://github.com/kaltura/server/pull/8792)
- PLAT-10177: Dump request to other dc in case we have the clip source there and this is not part of a `multirequest` (https://github.com/kaltura/server/pull/8774)

* Thu Oct 10 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.9.0-1
- Ver Bounce to 15.9.0

* Mon Oct 7 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.8.0-21
- AN-931: remove media type filter from USER HIGHLIGHTS report (https://github.com/kaltura/server/pull/8788)
- WEBC-1554: add `systemName` to the `QandA` response profile (https://github.com/kaltura/server/pull/8787)
- Include the entry ID in the `pexip` email (https://github.com/kaltura/server/pull/8785)
- PLAT-10200: Add ability to search history indexing per partner (https://github.com/kaltura/server/pull/8784)
- PLAT-10199: Remove `str_entry_id` from Sphinx `kaltura_cue_point` table (https://github.com/kaltura/server/pull/8783)
- PLAT-10143: eSearch - support double quotes for exact match of multiple strings (https://github.com/kaltura/server/pull/8781)
- PLAT-10115: Fix total count when listing likes (https://github.com/kaltura/server/pull/8780)
- SUP-17762: allow `playlist->clone()` when `display_in_search` is set to 2 (https://github.com/kaltura/server/pull/8779)
- PLAT-10143: eSearch - support double quotes for exact match of multiple strings (https://github.com/kaltura/server/pull/8778)
- SUP-19263: Fix Kaltura Capture source corruption when using WV (encryption) (https://github.com/kaltura/server/pull/8777)
- Handle backslashes when filter is Equal or In (https://github.com/kaltura/server/pull/8776)
- Update entry plays/views from KAVA (https://github.com/kaltura/server/pull/8775)
- PLAT-10120: Add the option to remove synonyms in esearch (https://github.com/kaltura/server/pull/8772)
- PLAT-10170: Enable SSO login with no user parameter (https://github.com/kaltura/server/pull/8767)
- Enrich report with entry source (https://github.com/kaltura/server/pull/8721)
 
* Tue Sep 17 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.8.0-1
- Ver Bounce to 15.8.0

* Mon Sep 16 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.7.0-9
- PLAT-9973: SSO - Fix email body not being included in the message (https://github.com/kaltura/server/pull/8768)
- SUP-19231: Email notification fix to handle more than 150 users when filtering with `idIn` (https://github.com/kaltura/server/pull/8764)
- REACH2-699: Reach Admin console fix for dictionary display (https://github.com/kaltura/server/pull/8763)
- PLAT-9973: SSO email templates (https://github.com/kaltura/server/pull/8762)
- PLAT-9908: Add implementation for `nameEqual` in ServerNodeFilter (https://github.com/kaltura/server/pull/8761)
- PLAT-9973: Determine email template to use based on SSO configuration (https://github.com/kaltura/server/pull/8759)
- PLAT-9838: SSO shouldn't be configured on partner 0 (https://github.com/kaltura/server/pull/8757)
- LEC-1784: Add `flavorparam` permission for capture app (https://github.com/kaltura/server/pull/8746)
- PLAT-9838: KMC SSO Support (https://github.com/kaltura/server/pull/8745)
- KAVA: fix adding comment to druid query (https://github.com/kaltura/server/pull/8733)
- Analytics: additional user level reports (https://github.com/kaltura/server/pull/8722)
- PLAT-10113: Add script that checks for duplicated users created since the last run and merges them (https://github.com/kaltura/server/pull/8719)
- WEBC-1429: QnA - display given name rather than user ID (https://github.com/kaltura/server/pull/8585)

* Mon Sep 9 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.7.0-1
- Ver Bounce to 15.7.0

* Sun Sep 8 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.6.0-18
- ElasticPopulate: run elastic index call inside current DC synchronously (https://github.com/kaltura/server/pull/8748)
- PLAT-10142: Ensure `populateFromLog.php` will never run an older sphinx log ID for a given object ID (https://github.com/kaltura/server/pull/8743)
- REACH2-690: Add ability to set transcript asset associated IDs on the caption asset (https://github.com/kaltura/server/pull/8742)
- PLAT-10100: The trim() function is not, by default, unicode safe. (https://github.com/kaltura/server/pull/8741)
- Fixes following static code analysis (https://github.com/kaltura/server/pull/8740)
- PLAT-10095: Preserve caption file extension when uploading via URL (https://github.com/kaltura/server/pull/8738)
- Reach-666: Add Hungarian + remove duplicate language (https://github.com/kaltura/server/pull/8736)
- plat 10072: Fix `filterEntriesByPartnerOrKalturaNetwork()` (https://github.com/kaltura/server/pull/8735)
- `eSearch`: call ` SphinxCriteria::enableForceSkipSphinx()` in populate scripts (https://github.com/kaltura/server/pull/8734)
- SUP-18356: Add locking mechanism to `categoryUser.add()` (https://github.com/kaltura/server/pull/8731)
- PLAT-10072: Fix `filterEntriesByPartnerOrKalturaNetwork()` (https://github.com/kaltura/server/pull/8730)
- REACH2-666: Add additional languages to REACH (Indonesian, Greek, Romanian) (https://github.com/kaltura/server/pull/8729)
- PLAT-10122: Add watch later user entry advanced filter (https://github.com/kaltura/server/pull/8728)
- AN-900: Add missing dimension map (https://github.com/kaltura/server/pull/8727)
- Sphinx populate fixes (https://github.com/kaltura/server/pull/8726)
- Update elastic mapping (https://github.com/kaltura/server/pull/8725)
- Fix `ExampleDistributionProfile.php` (https://github.com/kaltura/server/pull/8724)
- PLAT-10121: Zoom - fix login page URI (https://github.com/kaltura/server/pull/8723)
- Introduce `enableForceSkipSphinx()` and `disableForceSkipSphinx()` (https://github.com/kaltura/server/pull/8720)
- Adjust `chunkDuration` to 4K contents (https://github.com/kaltura/server/pull/8718)
- KMS-19596: When recurring by day for N weeks, check first occurrence in upcoming week, not just last week (https://github.com/kaltura/server/pull/8717)
- Adjust `chunkDuration` to 4K contents (https://github.com/kaltura/server/pull/8716)
- PLAT-10112: Catch specific `AMQPRuntimeException` exception rather than generic PHP `Exception` (https://github.com/kaltura/server/pull/8715)
- PLAT-10050: L3 CDN tokenizer - fix ACL implementation (https://github.com/kaltura/server/pull/8714)
- PLAT-10084: Add read only permission for `eSearch` (https://github.com/kaltura/server/pull/8713)
- Add retry mechanism to Rabbit MQ connection + reduce connection timeout from 3 to 2 (https://github.com/kaltura/server/pull/8710)
- Add permission for multi account analytics (https://github.com/kaltura/server/pull/8709)
- PLAT-10089: Zoom vendor refactor (https://github.com/kaltura/server/pull/8708)
- PLAT-10081: Add anonymous `kuser` on every partner (https://github.com/kaltura/server/pull/8704)
- PLAT-9986: Allow adding external values to dispatch of email event notifications (https://github.com/kaltura/server/pull/8702)
- PLAT-10050: Support L3 CDN tokenizer (https://github.com/kaltura/server/pull/8700)
- AN-835: Add VPaaS reports (https://github.com/kaltura/server/pull/8698)
- `CONVERT_CAPTION_ASSET` job type enum to string mapping (https://github.com/kaltura/server/pull/8658)


* Thu Aug 22 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.6.0-1
- Ver Bounce to 15.6.0

* Tue Aug 20 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.5.0-10
- Parse errors (https://github.com/kaltura/server/pull/8703)
- Reach-audioDescription: Add clear audio flavor param ID to catalog definition (https://github.com/kaltura/server/pull/8701)
- SUP-18989: check if PID enforce HTTPS API and modify Report Service URL accordingly (https://github.com/kaltura/server/pull/8697)
- maxExecutionTime=6000,for 4K/H265 chunks (https://github.com/kaltura/server/pull/8694)
- SUP-18972: Set the source entry ID when clipping/trimming from remote dc (https://github.com/kaltura/server/pull/8689)
- Add missing `eventNotification` directives (https://github.com/kaltura/server/pull/8680)
- PLAT-9986: Add monitoring proxy partner, permissions and e-mail alert (https://github.com/kaltura/server/pull/8677)


* Thu Aug 8 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.5.0-1
- Ver Bounce to 15.5.0

* Mon Aug 5 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.4.0-15
- PLAT-10026: Fix error in partner controller (https://github.com/kaltura/server/pull/8684)
- REACH2-659: Add 5 days TAT option (https://github.com/kaltura/server/pull/8683)
- PLAT-9949:  When permissions query returns empty, throw Exception before storing in cache (https://github.com/kaltura/server/pull/8682)
- PLAT-10026: Validate domains from partner configuration allowed from email whitelist (https://github.com/kaltura/server/pull/8679)
- Change `populateFromLog.php` to load shredded index config from DB config file (https://github.com/kaltura/server/pull/8676)
- REACH2-663: Change REACH notifications subject (https://github.com/kaltura/server/pull/8668)
- REACH2-563: Update REACH credit notification, sending notifications (https://github.com/kaltura/server/pull/8666)
- REACH2-662: Update Reach notification Task Pending Moderation (https://github.com/kaltura/server/pull/8663)
- PLAT-10052: Move `three_code_language_partners` to DB (https://github.com/kaltura/server/pull/8662)
- SUP-19010: Add default `eventTypes` to live reports base filter (https://github.com/kaltura/server/pull/8661)
- PLAT-9999: `liveStream.list()` with isRecordedEntryIdEmpty = 0 returns incorrect results (https://github.com/kaltura/server/pull/8654)

* Mon Jul 22 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.4.0-1
- Ver Bounce to 15.4.0

* Mon Jul 22 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.3.0-7
- PLAT-10043: Set access control profile correct type for esearch aggs (https://github.com/kaltura/server/pull/8656)
- PLAT-10020: Zoom transcription label and language (https://github.com/kaltura/server/pull/8655)
- PLAT-10043: E-search Aggregations - move on to the next bucket if no sub-buckets exist (https://github.com/kaltura/server/pull/8652)
- PLAT-10024: Fix admin console OTP exploit (https://github.com/kaltura/server/pull/8651)
- SUP-17451: Download user list as CSV: dedup records with the same kuser ID (https://github.com/kaltura/server/pull/8648)
- PLAT-9998: Introducing the `WatchLater` Plugin (https://github.com/kaltura/server/pull/8647)
- When filtering categoryEntry by `createdAt`, add `updatedAt` to the query to utilize an existing index (https://github.com/kaltura/server/pull/8646)
- PLAT-10019: Fix resource reservation bug (https://github.com/kaltura/server/pull/8644)
- SUP-18254: Correctly handle mutiple groupUser.delete() actions on user (https://github.com/kaltura/server/pull/8643)
- SUP-16933: Rule based playlist incorrectly sorted (https://github.com/kaltura/server/pull/8642)
- PLAT-10011: Zoom - handle duplicate transcription complete events (https://github.com/kaltura/server/pull/8639)
- PLAT-10014: Zoom chat and transcript file types (https://github.com/kaltura/server/pull/8638)
- PLAT-10002: Handle duplicate Zoom record complete events (https://github.com/kaltura/server/pull/8637)
- PLAT-9959: Add `Timing-Allow-Origin` to the response header (https://github.com/kaltura/server/pull/8636)
- PLAT-10001: eSearch - `searchUser()` and `searchCategory()` broken with PHP 7.2 (https://github.com/kaltura/server/pull/8635)
- PLAT-9942: Add 2FA support to `adminUser->updatePassword()` and `user->updateLoginData()` (https://github.com/kaltura/server/pull/8633)
- PLAT-9974: If moderation is enabled for the entry, only distribute after the entry has been approved (https://github.com/kaltura/server/pull/8631)
- PLAT-9902: Support conversion of captions from scc/srt/dfxp/webvtt to scc/srt/dfxp/webvtt (https://github.com/kaltura/server/pull/8628) 
- PSVAMB-7785: MRSS Roku syndication feed - live entry support (https://github.com/kaltura/server/pull/8626)
- Creation date update script (https://github.com/kaltura/server/pull/8625)
- SUP-16933: Use eSearch instead of Sphinx for playlist execute from filter (https://github.com/kaltura/server/pull/8624)
- `partner->getSecrets()` should accept the optional $otp and pass it on to `userLoginByEmail()` (https://github.com/kaltura/server/pull/8622)
- Fix upgrade sql alters (https://github.com/kaltura/server/pull/8618)
- PLAT-9936: Zoom chat file support (https://github.com/kaltura/server/pull/8611)
- Plat 9889: Add support in eSearch aggregations (https://github.com/kaltura/server/pull/8504)
- PLAT-9784: Add whitelist of allowed `from_emails` on partner info (https://github.com/kaltura/server/pull/8388)

* Tue Jul 9 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.3.0-1
- Ver Bounce to 15.3.0

* Sun Jul 7 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.2.0-14
- Nightly build.

* Sat Jul 6 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.2.0-13
- Nightly build.

* Fri Jul 5 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.2.0-1
- Nightly build.

* Fri Jul 5 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.2.0-12
- SUP-18108: Avoid endless loop when generating entry vendor task CSV (https://github.com/kaltura/server/pull/8616)
- PLAT-9993: Quiz - report.getTotal() supporting filtering (https://github.com/kaltura/server/pull/8614)
- PLAT-9933: Fix Zoom auth validation (https://github.com/kaltura/server/pull/8613)
- PLAT-9992: Fix Zoom registration bug (https://github.com/kaltura/server/pull/8612)
- PLAT-9933: Fix Zoom auth validation (https://github.com/kaltura/server/pull/8607)
- Update kPexipUtils.php (https://github.com/kaltura/server/pull/8605)
- PLAT-9547: Zoom enchanments (https://github.com/kaltura/server/pull/8602)
- PLAT-9855: Quiz report API - support filtering by datee (https://github.com/kaltura/server/pull/8599)
- PLAT-9898: Fix defect in `quizUser` entry validation (https://github.com/kaltura/server/pull/8596)
- PLAT-9943: 2FA - handle the case of a user associated with multiple partners (https://github.com/kaltura/server/pull/8594)
- Forced keyframes not generated (https://github.com/kaltura/server/pull/8593)
- PLAT-9952: KMC preview and embed: altered the fonts size and hight (https://github.com/kaltura/server/pull/8579)
- FEC-9040: Redesigned preview page (https://github.com/kaltura/server/pull/8577)
- PLAT-9706: Fix Zoom authentication flow (https://github.com/kaltura/server/pull/8572)

* Mon Jun 24 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.2.0-1
- Ver Bounce to 15.2.0

* Mon Jun 24 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.1.0-29
- PLAT-9929: return language code in `captionAsset` (https://github.com/kaltura/server/pull/8567)
- KMCNG-2114: remove check for seed on login data (https://github.com/kaltura/server/pull/8565)
- PLAT-9927: handle cases where login ID on partner object is null (https://github.com/kaltura/server/pull/8563)
- PLAT-9896: Prevent non-admin users from changing roles (https://github.com/kaltura/server/pull/8562)
- kCategoryEntryCondition.php: Always trim values to avoid extra spaces (https://github.com/kaltura/server/pull/8561)
- kCategoryEntryCondition.php: Always trim values to avoid extra spaces (https://github.com/kaltura/server/pull/8560)
- PLAT-9886: Handle `dynamic playList` updates (https://github.com/kaltura/server/pull/8558)
- PLAT-9923: Avoid unnecessary DB writes (https://github.com/kaltura/server/pull/8557)
- SUP-17775: Not all caption assets are fetched (https://github.com/kaltura/server/pull/8556)
- FEC-9040: redesigned KMC's preview and embed view (https://github.com/kaltura/server/pull/8554)
- PLAT-9921 update SIP permission to allow admin only usage (https://github.com/kaltura/server/pull/8553)
- SUP-18314: Allow users with KMC access the ability to order caption requests (https://github.com/kaltura/server/pull/8552)
- PLAT-9841: Block access to `loginByLoginId()` for certain partners (sometimes desired when SSO is used for auth) (https://github.com/kaltura/server/pull/8551)
- REACH2-627: Ensure `consumers` array contains unique values to avoid consuming the same event twice (https://github.com/kaltura/server/pull/8549)
- KMCNG-2114: In preparation for supporting SSO and 2FA in KMCng (https://github.com/kaltura/server/pull/8548)
- Fix schema update flow (https://github.com/kaltura/server/pull/8546)
- PLAT-9719: thumbnail filters (https://github.com/kaltura/server/pull/8544)
- PLAT-9664: Support additional languages (https://github.com/kaltura/server/pull/8543)
- SUP-17451: Incorrect user roles in CSV export (https://github.com/kaltura/server/pull/8542)
- PLAT-9841: Block access to `loginByLoginId()` for certain partners (sometimes desired when SSO is used for auth) (https://github.com/kaltura/server/pull/8541)
- SUP-18392: Compress indexing queries based on (configurable) size threshold (https://github.com/kaltura/server/pull/8540)
- SUP-18090: When a user is deleted, delete all its `appTokens` (https://github.com/kaltura/server/pull/8538)
- PLAT-9664: Support additional languages (https://github.com/kaltura/server/pull/8537)
- PSVAMB-7338: CSV bulk upload for scheduled events (https://github.com/kaltura/server/pull/8536)
- PLAT-9721: Image transformations (https://github.com/kaltura/server/pull/8535)
- SUP-18428: set `creatorId` to `userId` in case no `creatorId` was passed (https://github.com/kaltura/server/pull/8533)
- PLAT-9916: Prevent `loginByKs` when origin partner auth is not `PartnerAuthenticationType::PASSWORD_ONLY` (https://github.com/kaltura/server/pull/8531)
- SUP-18208: When storage protocol is null, we don't need to get the remote URL (https://github.com/kaltura/server/pull/8529)
- KMCNG-2114: change types for clients (https://github.com/kaltura/server/pull/8527)
- Pass type to `duplicateTemplateEntry` (https://github.com/kaltura/server/pull/8526)
- REACH2-605: Allow updating existing reach profile's credit object type (https://github.com/kaltura/server/pull/8525)
- KMCNG-2114: Change qr code dimensions (https://github.com/kaltura/server/pull/8519)
- REACH2-575: support sending notifications for the `NotifiedUsers` per profile configuration (https://github.com/kaltura/server/pull/8517)
- REACH2-583: Add new chaptering service (https://github.com/kaltura/server/pull/8511)
- PSVAMB-7338: CSV bulk upload for scheduled events (https://github.com/kaltura/server/pull/8510)
- KMCNG-2130: 2FA mail notification strings (https://github.com/kaltura/server/pull/8509)
- PLAT-9896: Prevent non-admin users from changing roles (https://github.com/kaltura/server/pull/8507)
- `SipIntegration` (https://github.com/kaltura/server/pull/8505)

* Wed May 29 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.1.0-1
- Ver Bounce to 15.1.0

* Tue May 28 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.0.0-14
- PLAT-9844: use `retrieveByPK()` rather than calling `doSelectOne()` (https://github.com/kaltura/server/pull/8459)
- PLAT-9867: `kCuePointManager::parseXml()` - Cast `entryId` to string (https://github.com/kaltura/server/pull/8458)
- PLAT-9844: `setAnalyticsHost()` - include the protocol (https://github.com/kaltura/server/pull/8456)
- plat-9877: Support the Michif Language (https://github.com/kaltura/server/pull/8453)
- SUP-18262: When sending values with spaces the params should be encoded (https://github.com/kaltura/server/pull/8451)
- PLAT-9844: Added `partner.getPublicInfo()` (https://github.com/kaltura/server/pull/8450)
- SIP integration (https://github.com/kaltura/server/pull/8445)
- SIP integration: Handling alerts (https://github.com/kaltura/server/pull/8443)
- PLAT-9851: TVinci connector - Support catalog and ingest format type (https://github.com/kaltura/server/pull/8438)
- SIP integration (https://github.com/kaltura/server/pull/8437)
- Index `sipToken` in the Sphinx entry table (https://github.com/kaltura/server/pull/8436)
- PLAT-9871: Move cache version to dynamic map (https://github.com/kaltura/server/pull/8435)
- Support multiple `embedPlaykitJsAction uiconf` tags (https://github.com/kaltura/server/pull/8433)
- pexip Integration (https://github.com/kaltura/server/pull/8431)
- PLAT-9869: Avoid long query exec time by adding partner ID to the criteria when querying `uiConf` (https://github.com/kaltura/server/pull/8430)
- PLAT-9867: Fix quiz plugin schema contribution to avoid API error when trying to bulk upload cue points (https://github.com/kaltura/server/pull/8429)
- pexip Integration (https://github.com/kaltura/server/pull/8428)
- SUP-18105: Support Luxembourgisch (https://github.com/kaltura/server/pull/8426)
- PLAT-9564: thumbnail.transform() - disable caching (https://github.com/kaltura/server/pull/8425)
- SUP-18026: `generateReachVendorKs()` - take output moderation into account (https://github.com/kaltura/server/pull/8424)
- PLAT-9849: DFP support multiple options in keys (https://github.com/kaltura/server/pull/8423)
- SUP-18105: Support Luxembourgisch (https://github.com/kaltura/server/pull/8422)
- PLAT-9868: Set default value for task creation mode manual (https://github.com/kaltura/server/pull/8420)
- Avoid DB query when fetching cue point objects (https://github.com/kaltura/server/pull/8419)
- Auto and iframe embeds: pass KS to `embedPlaykitAction()` (https://github.com/kaltura/server/pull/8418)
- `XmlClientGenerator`: fix warnings (https://github.com/kaltura/server/pull/8417)
- Avoid notices when when loading old job data that does not contain the scheduler name (https://github.com/kaltura/server/pull/8416)
- PLAT-9862: `media.approveReplace()` -  return immediately if `KalturaMediaType::IMAGE` since no conversion needs to take place (https://github.com/kaltura/server/pull/8415)
- Add live fields if the template is a live entry one (https://github.com/kaltura/server/pull/8414)
- REACH2-581: Support both boolean and regular rules on the same reach profile (https://github.com/kaltura/server/pull/8413)
- New thumbnail service (https://github.com/kaltura/server/pull/8404)
- plugins/beacon/scripts/BeaconsIndexesRotation.php: support removal of unused indices (https://github.com/kaltura/server/pull/8273)
- PLAT-9401: Sphinx - support distributed (across nodes) indices (https://github.com/kaltura/server/pull/7828)

* Tue May 14 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.0.0-1
- Ver Bounce to 15.0.0

* Mon May 13 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.0.0-1
- Nightly build.

* Mon May 13 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.20.0-14
- Make `PHPMailer` code compatible with both PHP 5 and 7 (https://github.com/kaltura/server/pull/8409)
- REACH2-579: Correctly handle cases where the task could not be created (https://github.com/kaltura/server/pull/8407)
- PLAT-9857: Correctly handle `kCountryCondition` when replying from cache layer (https://github.com/kaltura/server/pull/8406)
- SUP-17908: `user.list` - retrieve both USER and GROUP objects if TYPE filter wasn't passed (https://github.com/kaltura/server/pull/8401)
- REACH2-577: When vendor marks the task status as error, set its price to 0 while saving old price value (https://github.com/kaltura/server/pull/8400)
- PLAT-9852 - Align with SaaS' `flavorParams` config (https://github.com/kaltura/server/pull/8398)
- PLAT-9848: `group.clone()` - add the option to set the new group name (`$newGroupName`) (https://github.com/kaltura/server/pull/8397)
- KMS-19393: `groupUser.sync()` - probe for separator char (can be either ',' or ';') (https://github.com/kaltura/server/pull/8395)
- PLAT-9850: kDataCenterMgr::getRedirectExternalUrl() - added timeout param (https://github.com/kaltura/server/pull/8393)
- PLAT-9843: Added option to limit the number of allowed actions per partner (https://github.com/kaltura/server/pull/8392)
- PLAT-9668: Admin console - entry investigation improvements (https://github.com/kaltura/server/pull/8391)
- REACH2-553: Handle live recording flows -  only set the job status to `pending` after the entire content is received (https://github.com/kaltura/server/pull/8385)
- KMCNG-2101: Add `X-Frame-Options` header to prevent potential iframe exploits (https://github.com/kaltura/server/pull/8382)
- PLAT-9845: Newer PHP versions incorrectly parse the URL when user or passwd contain the "#" char (https://github.com/kaltura/server/pull/8381)
- REACH2-573: Handle cases where catalog item is deleted (https://github.com/kaltura/server/pull/8379)
- NO-PLAT: Support ElasticSearch 6 (https://github.com/kaltura/server/pull/8376)
- PLAT-9814: New boolean event notification template for Reach (https://github.com/kaltura/server/pull/8367)
- PLAT-9795: Allow asset type condition when serving caption asset (https://github.com/kaltura/server/pull/8366)
- Fix PHP warnings (https://github.com/kaltura/server/pull/8130)
- `protocol` is Undefined use `params->getFormat()` instead (https://github.com/kaltura/server/pull/7923)

* Tue Apr 30 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.20.0-1
- Ver Bounce to 14.20.0

* Sun Apr 28 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-11
- Nightly build.

* Sat Apr 27 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-10
- Nightly build.

* Fri Apr 26 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-9
- Nightly build.

* Thu Apr 25 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-8
- Nightly build.

* Wed Apr 24 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-6
- Nightly build.

* Tue Apr 23 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-5
- Nightly build.

* Mon Apr 22 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-4
- Nightly build.

* Sun Apr 21 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-1
- Nightly build.

* Sat Apr 20 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-3
- Nightly build.

* Fri Apr 19 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-1
- Nightly build.

* Thu Apr 18 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-1
- Nightly build.

* Wed Apr 17 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-2
- Nightly build.

* Tue Apr 16 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-1
- Nightly build.

* Tue Apr 16 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-1
- Ver Bounce to 14.19.0

* Tue Apr 16 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.18.0-5
- Fix `kmc_analytics_version` value

* Mon Apr 15 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.18.0-2
- PLAT-9782: Change action name to `userEntryBulkDelete()` (https://github.com/kaltura/server/pull/8322)
- PLAT-9807: `group.membersCount()` - reduce the chance of getting out of sync (https://github.com/kaltura/server/pull/8313)
- PLAT-9806: Call concat() action after every trim (https://github.com/kaltura/server/pull/8312)
- When searching drop folder file using `fileNameEqual` use the MD5 hash for matching (https://github.com/kaltura/server/pull/8311)
- DB table index enhancements (https://github.com/kaltura/server/pull/8309)
- `kuserKgroup`: add query cache rule on group ID (https://github.com/kaltura/server/pull/8308)
- Deployment script for listFeatureStatus permission (https://github.com/kaltura/server/pull/8307)
- Add `STUDIO_BASE` permission for capture role (https://github.com/kaltura/server/pull/8306)
- PLAT-9804: getNumberOfUsersInGroup() - reduce the number of DB queries needed (https://github.com/kaltura/server/pull/8305)
- SUP-17609: entry.php:copyInto() - catch and log exceptions when calling `setEntitledPusersEdit()` and `setEntitledPusersPublish()` (https://github.com/kaltura/server/pull/8304) 
- SUP-16950: `eSearch::searchCategory()` - allow searching for `categoryUser` based on its group association (https://github.com/kaltura/server/pull/8300)
- Esearch-Sphinx optimisations (https://github.com/kaltura/server/pull/8298)
- SUP-17626: Comments and Sub-commnets are deleted when trimming (https://github.com/kaltura/server/pull/8294)
- PLAT-9748: Prevent potential SVG thumb asset XSS (https://github.com/kaltura/server/pull/8291)
- REACH2-547: Support removal of all automatic rules (https://github.com/kaltura/server/pull/8290)
- Handle reach notices when catalog item fields are unavailable (https://github.com/kaltura/server/pull/8289)
- SUP-17627: Prevent email notification for temp entry annotation creation (https://github.com/kaltura/server/pull/8288)
- PLAT-9770: Purify URL `flashvars` in `previewAction()` (https://github.com/kaltura/server/pull/8285)
- Event notifications with group ID: Incorrect concatenation when running with PHP 5.3 (https://github.com/kaltura/server/pull/8284)
- PLAT-9707: add `idGreaterThan` and `createdAtGreaterThanOrEqual` to partner filter (https://github.com/kaltura/server/pull/8281)
- REACH2-545: Add support for new languages in Reach (https://github.com/kaltura/server/pull/8280)
- PLAT-9797: When trimming multi video source , focus only on the first … (https://github.com/kaltura/server/pull/8279)
- SUP-17626: Handle annotation and sub-annotation cloning when clipping and trimming (https://github.com/kaltura/server/pull/8277)
- Return `REPORT_SUBMITTED` count instead of `REPORT_CLICKED` (https://github.com/kaltura/server/pull/8276)
- SUP-17800: HF for CSV-upload for End-User is not working properly (https://github.com/kaltura/server/pull/8274)
- PSVAMB-6933: Update "comment added" KMS notification body - fix the link (https://github.com/kaltura/server/pull/8271)
- REACH2-536: Add support for new catalog item type of `audio_description` (https://github.com/kaltura/server/pull/8270)
- Make `userEntry.bulkDelete()` work with bulk batch job (https://github.com/kaltura/server/pull/8267)
- SUP-17645: Handle PHP bug when returning file MIME type (https://github.com/kaltura/server/pull/8257)
* Mon Apr 8 2019 Jess Portnoy <jess.portnoy@kaltura.com> - 14.18.0-1
- Ver Bounce to 14.18.0

* Sun Mar 31 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.17.0-12
- Pass mandatory param when calling `addHeaderRowToCsv()` (https://github.com/kaltura/server/pull/8259)
- Increase elastic beacon replication factor for fallback (https://github.com/kaltura/server/pull/8258)
- PLAT-9771 - `kClipManager.php`: avoid `concat()` on single operation attribute (https://github.com/kaltura/server/pull/8254)
- PLAT-9771 - `kClipManager.php`: avoid `concat()` on single operation attribute (https://github.com/kaltura/server/pull/8253)
- AN-188: Add batch job to export `report` results to CSV (https://github.com/kaltura/server/pull/8250)
- PLAT-9766: Call `kFileUtils::dumpApiRequest()` when thumb `$srcSyncKey` only exists on the other DC (https://github.com/kaltura/server
/pull/8242)
- PLAT-9723: Add support for copying a group (https://github.com/kaltura/server/pull/8241)
- KMS-19341: When querying entries by username, entries with a group that the user is entitled to should be returned as well (https://github.com/kaltura/server/pull/8240)
- Fix `confmaps` admin console page on service forbidden (https://github.com/kaltura/server/pull/8238)
- `playlist.updateAction()` modifications (https://github.com/kaltura/server/pull/8237)
- PLAT-9746: Return `totalCount` of 0 when `KalturaUserEntryListResponse` is empty (https://github.com/kaltura/server/pull/8235)
- PLAT-9421: Save `cdnWhiteList` results in memory in order to avoid multiple invocations during list() calls (https://github.com/kaltura/server/pull/8232)
- PLAT-9760: Make `esearch.searchUser` filter by `group_ids` field to work with `puserId` (https://github.com/kaltura/server/pull/8229)
- PLAT-9736: keep user search in recent searches (https://github.com/kaltura/server/pull/8227)
- Add option to disable new analytics tab in KMC (https://github.com/kaltura/server/pull/8226)
- PLAT-9663: youtubeApi - no status when video rejected due to video length  (https://github.com/kaltura/server/pull/8225)
- PLAT-9758: Allow partial search for username (https://github.com/kaltura/server/pull/8219)
- PSVAMB-4967, PSVAMB-4944: KMS Email Notifications update (https://github.com/kaltura/server/pull/8038)

* Tue Mar 19 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.17.0-1
- Ver Bounce to 14.17.0

* Mon Mar 18 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.16.0-16
- PLAT-9742: Added `ESearchGroupOrderByItem.php` (https://github.com/kaltura/server/pull/8217)
- PLAT-9742: Move group related `eSearch` code to the `Group` plugin (https://github.com/kaltura/server/pull/8213)
- PLAT-9742: fix param types in `validateUserNames()` and `addUserImpl()` (https://github.com/kaltura/server/pull/8212)
- Add `PushNotification` and `BooleanNotification` to `plugins.template.ini` (https://github.com/kaltura/server/pull/8210)
- PLAT-9742: Add the `Group` plugin to plugins.ini (https://github.com/kaltura/server/pull/8208)
- `KMediaFileComplexity::EvaluateSampled()`: Return null if sampling data is missing (https://github.com/kaltura/server/pull/8202)
- PLAT-9742: Upon `groupUser` delete() or add(), update the counter on group user (https://github.com/kaltura/server/pull/8198)
- Chunked encoding fixes (https://github.com/kaltura/server/pull/8195)
- PLAT-9754: Extract media fixes (https://github.com/kaltura/server/pull/8194)
- PLAT-9752: eSearch - support sorting by user ID and screen name (https://github.com/kaltura/server/pull/8193)
- PLAT-9701: Entry investigation - track template entry (https://github.com/kaltura/server/pull/8190)
- Update Live Params and remove ingest tag from Cloud Transcode flavors (https://github.com/kaltura/server/pull/8186)
- PLAT-9747: Upon deletion of `QuizUserEntry`, delete all its answer cuepoint objects (https://github.com/kaltura/server/pull/8185)
- PLAT-9648: Remove BIF thumbnail v2 flow (https://github.com/kaltura/server/pull/8184)
- PLAT-9745: Change the name of the retake fields and fix score type (https://github.com/kaltura/server/pull/8183)
- PLAT-9740: Media repurposing - When setting `inputUserId`, `inputEntitledUsersEdit` and `inputEntitledUsersPublish` to 'N/A' the origi
nal values will be kept (https://github.com/kaltura/server/pull/8182)
- PLAT-9738: Drop use of `json_decode()` (lead to memory exhaustion) (https://github.com/kaltura/server/pull/8180)
- PLAT-9318: Quiz retake - add score type and calculate overall score accordingly (https://github.com/kaltura/server/pull/8176)
- PLAT-9730: When importing during `clip_concat()`, skip the virus scan as it blocks the other consumers (https://github.com/kaltura/server/pull/8175)
- PLAT-9651: Handle `xsdDoc` page generation when type is invalid (https://github.com/kaltura/server/pull/8173)
- PLAT-8580: Add managers to group user (https://github.com/kaltura/server/pull/8167)
- SUP-17212: Disallow calling `add_content()` when entry is not in `no_content` state (https://github.com/kaltura/server/pull/8165)
- PLAT-9681: Quiz retake functionality (https://github.com/kaltura/server/pull/8156)
- PLAT-9648: Add BIF file generation (https://github.com/kaltura/server/pull/8139)

* Tue Mar 5 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.16.0-1
- Ver Bounce to 14.16.0

* Sun Mar 3 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.15.0-11
- PLAT-9727: Fix API annotation on `userEntryService` (https://github.com/kaltura/server/pull/8164)
- Add missing `conf_maps` table to initial DB deployment (https://github.com/kaltura/server/pull/8163)
- eSearch: Don't skip executed updates in `populateElasticFromLog` (https://github.com/kaltura/server/pull/8159)
- Added `ALIGNMENT` to `$serviceTypeEnumTranslate` (https://github.com/kaltura/server/pull/8157)
- SUP-16956: Fix missing subtitles issue (https://github.com/kaltura/server/pull/8151)
- PLAT-9683: Add support for searching entries by `owner=groupId` or owner in `groupIds` (https://github.com/kaltura/server/pull/8150)
- PLAT-9699: Fix `ClipConcatJobData` parsing (https://github.com/kaltura/server/pull/8142)
- PLAT-9699: Fix `ClipConcatJobData` parsing (https://github.com/kaltura/server/pull/8141)
- PLAT-9698: `UpdateContent()` with operation params does not trim (https://github.com/kaltura/server/pull/8140)
- PLAT-9643: Support viewing older versions of `confMaps`  (https://github.com/kaltura/server/pull/8138)
- PLAT-9656: create new boolean event notification (https://github.com/kaltura/server/pull/8137)
- SUP-17265: Eliminate a situation where a client requests non-existent flavor param ID from the server and gets empty manifest as result (https://github.com/kaltura/server/pull/8136)
- Set `UpdateAt` when deleting a cue-point (https://github.com/kaltura/server/pull/8135)
- Use a protocol agnostic URL for `embedPlaykitJs` (https://github.com/kaltura/server/pull/8134)
- Copy poll data cue point regardless of its time (https://github.com/kaltura/server/pull/8133)
- PLAT-9644: Support trimming/clipping content from remote storage or the other dc (https://github.com/kaltura/server/pull/8128)

* Thu Feb 21 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.15.0-1
- Ver Bounce to 14.15.0

* Mon Feb 18 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.14.0-13
- If `accessControlNameToId` is undefined call `initAccessControlNameToId()` (https://github.com/kaltura/server/pull/8121)
- return `calcPageSize` to `kFilterPager` (https://github.com/kaltura/server/pull/8118)
- PLAT-9653: KalturaScheduleResourceFilter.php - support filtering by `statusEqual` === DELETED (https://github.com/kaltura/server/pull/8112)
- PLAT-9680: handle languages in `contributeToPlaybackContextDataResult()` the same as in `playManifest` (https://github.com/kaltura/server/pull/8111)
- PLAT-9670: Scheduling - improve blackout conflict performance (https://github.com/kaltura/server/pull/8109)
- PLAT-9672: Fix exception in thumbnail creation (https://github.com/kaltura/server/pull/8108)
- Add `schedule_event.STATUS` to sphinx match optimization (https://github.com/kaltura/server/pull/8105)
- PLAT-9667: Adding/updating feedback when the quiz is submitted and updating answers is disallowed (https://github.com/kaltura/server/pull/8103)
- PLAT-9661: Update logic of setting `lastModified` of thumbnail (https://github.com/kaltura/server/pull/8101)
- PLAT-9666: Handle multiple permissions update with a single partner save (https://github.com/kaltura/server/pull/8099)
- Add sphinx match optimization and invalidation keys to schedule event index (https://github.com/kaltura/server/pull/8098)
- REACH2-496: Update alignment job data to include additional params (https://github.com/kaltura/server/pull/8097)
- Add validations to ICS bulk upload (https://github.com/kaltura/server/pull/8095)
- Schedule event bulk upload (https://github.com/kaltura/server/pull/8094)
- eSearch - query boolean fields only with true/false (https://github.com/kaltura/server/pull/8092)
- PLAT-9653: KalturaScheduleResourceFilter.php - support filtering by `statusEqual` === DELETED (https://github.com/kaltura/server/pull/8091)
- PSVAMB-4099: `playManifestAction` - call `setMinBitrate()` and `setMaxBitrate()` (https://github.com/kaltura/server/pull/8089)
- PLAT-9642: when updating an answer cue point, the fields should be added to the modified columns (https://github.com/kaltura/server/pull/8088)
- Fix PHP7 notices & warnings (https://github.com/kaltura/server/pull/8081)
- Ensure the asset is found before calling `shouldEncrypt()` (https://github.com/kaltura/server/pull/8080)
- PLAT-9629: Avoid copying Answer cue points to trimmed clipped entries (https://github.com/kaltura/server/pull/8078)
- PLAT-9625: Support multipart upload to S3 when file size is bigger than 5G (https://github.com/kaltura/server/pull/8067)
- eSearch - update mapping + add logstash playsviews conf (https://github.com/kaltura/server/pull/8037)

* Thu Feb 7 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.14.0-1
- Ver Bounce to 14.14.0

* Mon Feb 4 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.13.0-15
- playsviews: use entryType instead of KalturaEntryType (https://github.com/kaltura/server/pull/8074)
- PLAT-9563: Do not index captionAssetItem in Sphinx (https://github.com/kaltura/server/pull/8073)
- PLAT-9626: Make KalturaAssetFilter::getTypeListResponse look up captionAssetItem using eSearch instead of Sphinx (https://github.com/kaltura/server/pull/8070)
- SUP-16884: On flavorMediaInfo update, append new tags rather than override (https://github.com/kaltura/server/pull/8069)
- playsViews: Fix default value + add optimization to executePlaylist() (https://github.com/kaltura/server/pull/8068)
- PLAT-9596: Conf Maps - add option to view list of all maps in combo box (https://github.com/kaltura/server/pull/8064)
- PLAT-9602: Extract thumbnail stripe from a segment of a video and not the entire video (https://github.com/kaltura/server/pull/8063)
- PLAT-9622: KalturaConfMaps - Custom validateForInsert() (https://github.com/kaltura/server/pull/8060)
- PLAT-9622: KalturaConfMaps - Custom validateForInsert() (https://github.com/kaltura/server/pull/8059)
- Chunked encoding: Support fetching source from remote URLs (https://github.com/kaltura/server/pull/8058)
- PLAT-9618: Add language code to playbackCaptions (https://github.com/kaltura/server/pull/8055)
- Limit change account to partners which the MA logged in user belongs to (https://github.com/kaltura/server/pull/8053)
- PLAT-9618: getLocalThumbFilePath() - added `start_sec` and `end_sec` args/params (https://github.com/kaltura/server/pull/8050)
- SUP-16810: getPlaybackContext() caching (https://github.com/kaltura/server/pull/8048)
- Service annotations (https://github.com/kaltura/server/pull/8047)
- PLAT-9608: Support feedback on `answer` cue point (https://github.com/kaltura/server/pull/8045)
- PLAT-9607: Support feedback on the `quiz` object (https://github.com/kaltura/server/pull/8044)
- PLAT-9607: quiz - Support feedback (https://github.com/kaltura/server/pull/8041)
- PLAT-9602: extract thumbnail stripe from segment of the video (https://github.com/kaltura/server/pull/8039)
- PLAT-9614: listPartnersForUserAction() - only return partners for which the given user is set as admin (https://github.com/kaltura/server/pull/8036)
- PLAT-9606: quiz question/answer - support free text (https://github.com/kaltura/server/pull/8035)
- PLAT-9574: virus scan plugin - scan related assets as well (https://github.com/kaltura/server/pull/8033)
- AN-217: New report type - source (https://github.com/kaltura/server/pull/8031)
- PLAT-9601: Verify src asset fileSync exists on current dc before adding a conversion job (https://github.com/kaltura/server/pull/8027)
- Retrieve plays and views from cache (https://github.com/kaltura/server/pull/8026)
- PLAT-9539: Asset dimensions are not set when account is set with encryption + Asset size is incorrectly set with encrypted file size when account is set with encryption (https://github.com/kaltura/server/pull/8001)
- Fix typos in service documentation (https://github.com/kaltura/server/pull/7972)

* Mon Jan 21 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.13.0-1
- Ver Bounce to 14.13.0

* Mon Jan 21 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.12.0-10
- Fix Java client lib

* Thu Jan 17 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.12.0-5
- SUP-16865-HF: FFM4 audio syntax changed (https://github.com/kaltura/server/pull/8022)
- PLAT-9576: Disable cache when calling ConfMapsService::getAction() (https://github.com/kaltura/server/pull/8014)
- PLAT-9575: Added support for `write_address_list` - List of addresses allowed to set Memcached data (https://github.com/kaltura/server/pull/8012)
- PLAT-9546: Add BulkUpload Status HTTP Event Notification (https://github.com/kaltura/server/pull/8011)
- PLAT-9567: Send `serverNodeIds=internal` when we get an IP from HTTP header but no KES is configured (https://github.com/kaltura/server/pull/8008)
- Added `2019_01_10_add_media_addbulkupload_to_batch_partner.php` (https://github.com/kaltura/server/pull/8006)
- Enable ConfMaps plugin (https://github.com/kaltura/server/pull/8005)
- PLAT-9568: captionAssetItem->list() - use captionAssetItem->search() (https://github.com/kaltura/server/pull/8004)
- Force access control validation when checking partner API access control (https://github.com/kaltura/server/pull/8003)
- PLAT-9491: Server Configuration Maps management  (https://github.com/kaltura/server/pull/8000)
- SUP-16550: Event notifications - allow setting HTTPS as the default protocol (https://github.com/kaltura/server/pull/7999)
- KalturaJsonSerializer.php: handle invalid UTF8 character (https://github.com/kaltura/server/pull/7997)
- PSVAMB-5604: Allow bulk updates through the regular XML on multiple entries retrieved according to a filter (https://github.com/kaltura/server/pull/7994)
- Handle too short chunk files (https://github.com/kaltura/server/pull/7993)
- PLAT-9545: Resizing all the frames in the stripe to the same dimensions (https://github.com/kaltura/server/pull/7981)
- SUP-16700: Add version to thumbnail URL on MRSS (https://github.com/kaltura/server/pull/7980)

* Sun Jan 13 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.12.0-1
- Ver Bounce to 14.12.0

* Fri Jan 4 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.11.0-25
- SUP-16649: Quiz - exclude questions from report when answers are not included in the score (https://github.com/kaltura/server/pull/798
- serveFlavor: set JSON_UNESCAPED_UNICODE when calling json_encode() (https://github.com/kaltura/server/pull/7982)
- SUP-16649: Quiz - exclude questions from report when answers are not included in the score (https://github.com/kaltura/server/pull/797
- PLAT-9543: Supply URL for entire webVtt download (https://github.com/kaltura/server/pull/7970)
- PLAT-9543: add parsing entry_id with regex on thumbnailAction to reduce dumpiApi to other DC (https://github.com/kaltura/server/pull/7
- PLAT-9447: thumbnail strips with stitched playlist (https://github.com/kaltura/server/pull/7965)
- PLAT-9542: retrieve categories from db in one query (https://github.com/kaltura/server/pull/7961)
- PLAT-9543: add captions info to playbackContext result (https://github.com/kaltura/server/pull/7960)
- Apache config changes (https://github.com/kaltura/server/pull/7957)
- KMCng analytics integration (https://github.com/kaltura/server/pull/7956)
- Optimize file sync queries (https://github.com/kaltura/server/pull/7952)
- Handle cases where getRequestParameter get name param with no value (https://github.com/kaltura/server/pull/7948)
- Handle cases where config key is passed but has no value (https://github.com/kaltura/server/pull/7947)
- SUP-16113: add broadcasting URLs when KS user in member of a kuserEdit entitled group (https://github.com/kaltura/server/pull/7940)
- PLAT-9517: setting source when attaching a URL resource (https://github.com/kaltura/server/pull/7936)
- Add missing reach_profile table (https://github.com/kaltura/server/pull/7934)
- sup-16136: KalturaLiveEntryService::registerMediaServerAction() - avoid race condition (https://github.com/kaltura/server/pull/7929)
- PLAT-9529: add IPs from custom HTTP header (https://github.com/kaltura/server/pull/7926)
- PLAT-8192: use eSearch instead of Sphinx for caption search services (https://github.com/kaltura/server/pull/7917)
- Fix documentation typos (https://github.com/kaltura/server/pull/7900)


* Mon Dec 17 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.10.0-8
- REACH2-483: Support defining specific flavor param ids for the vendor to fetch (https://github.com/kaltura/server/pull/7922)
- PLAT-9396: Beacon search fixing fields name for new schema (https://github.com/kaltura/server/pull/7920)
- PLAT-9396: Beacon searchScheduledResource mapping (https://github.com/kaltura/server/pull/7918)
- REACH: Clone profile and partner catalog items (https://github.com/kaltura/server/pull/7915)
- Support latest apache versions strict standards (https://github.com/kaltura/server/pull/7914)
- AN-192: add `avg_drop_off` metric to syndication report (https://github.com/kaltura/server/pull/7913)
- AN-182: add fields to report input filter (https://github.com/kaltura/server/pull/7912)
- Support several chunk schedulers per node (https://github.com/kaltura/server/pull/7910)
- PLAT-9384: Beacon search - rename classes (https://github.com/kaltura/server/pull/7909)
- PLAT-9505: Fix WebM metadata extraction (https://github.com/kaltura/server/pull/7908)
- Check for `tags` in copyCuePoints/Engine (https://github.com/kaltura/server/pull/7907)
- PLAT-9504: Handle serialization of data entry with invalid chars (https://github.com/kaltura/server/pull/7905)
- REACH: Clone profile and partner catalog items (https://github.com/kaltura/server/pull/7903)
- SUP-16392: Order delivery profiles based on user defined criteria (https://github.com/kaltura/server/pull/7899)
- PLAT-9384: Beacon search (https://github.com/kaltura/server/pull/7897)
- If destFile provided and we failed to open it return false (https://github.com/kaltura/server/pull/7895)
- SUP-16219: Copy startDate and endDate from template entry (https://github.com/kaltura/server/pull/7894)
- Report filter - add missing categories mapping (https://github.com/kaltura/server/pull/7893)
- Change combined metrics to match graph format (for totals) (https://github.com/kaltura/server/pull/7892)
- Handle case where `getRemoteDeliveryByStorageId()` returned null (https://github.com/kaltura/server/pull/7890)
- PHP7 (strict standards): Handle PHP Fatal error: Only variables can be passed by reference (https://github.com/kaltura/server/pull/7884)
- AN-155: add unique users metric to reports (https://github.com/kaltura/server/pull/7883)

* Wed Dec 5 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.10.0-1
- Ver Bounce to 14.10.0

* Mon Dec 3 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.9.0-14
- crypto wrapper/openssl support additional methods (https://github.com/kaltura/server/pull/7885)
- PLAT-9399: CamelCase categoryEntry.updateStatusFromBulk action alias (https://github.com/kaltura/server/pull/7882)
- PLAT-9410: KalturaConversionProfile.php - Prevent type mismatch during validateForUpdate() (https://github.com/kaltura/server/pull/7881)
- playManifest - support captions in media playlist (https://github.com/kaltura/server/pull/7880)
- SUP-15844: KAsyncConvert.class.php - retry move operation in the event of failure (https://github.com/kaltura/server/pull/7878)
- playManifest - add track selection support (https://github.com/kaltura/server/pull/7875)
- PLAT-9467: kUploadTokenMgr.php - verify that the source file exists (https://github.com/kaltura/server/pull/7871)
- TR-2167: Allow MRSS's + Drop Folder + Bulk XML conversion profiles to use the 'CategoryID' as reference (https://github.com/kaltura/server/pull/7865)
- PLAT-9460: Chunked Encoding - support EaR sources (https://github.com/kaltura/server/pull/7863)
- Fix missing search ACL and change default dropfolder configuration (https://github.com/kaltura/server/pull/7862)
- SUP-15957: Handle source flavor fileExt on clipping and trimming (https://github.com/kaltura/server/pull/7861)
- Analytics: add properties mapping for filter objects (https://github.com/kaltura/server/pull/7860)
- PLAT-9303: Enable event notification templates for all partners (https://github.com/kaltura/server/pull/7859)
- Fix PHP Warnings (https://github.com/kaltura/server/pull/7857)
- PLAT-9429: EaR - content shorter than 10s is not encrypted (https://github.com/kaltura/server/pull/7855)
- PLAT-9406: eSearch - add entitled_kusers_view to entry index (https://github.com/kaltura/server/pull/7848)
- PLAT-9381: build thumb url for playlists (https://github.com/kaltura/server/pull/7847)
- PLAT-9441: validate the entry exist before embarking on clipping flow (https://github.com/kaltura/server/pull/7846)
- PLAT-9440: Conversion - Handle cases where source flavor was deleted (https://github.com/kaltura/server/pull/7845)
- PSVAMB-5293: Email notifications - support PHP 5.3 (https://github.com/kaltura/server/pull/7842)
- SUP-15957 - Fix missing fileExt on source flavor asset after clipping (https://github.com/kaltura/server/pull/7838)
- PLAT-9410: Prevent the addition of conversion profiles in the event their type and the type of the flavor params assigned to them do not match (https://github.com/kaltura/server/pull/7829)
- PLAT-9399: allow bulk activate/reject for category entries (https://github.com/kaltura/server/pull/7824)

* Wed Nov 21 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.9.0-1
- Ver Bounce to 14.9.0

* Mon Nov 19 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.8.0-23
- Handle cases where access_control_id doesn't exist on the entry object

* Mon Nov 19 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.8.0-22
- Fix secureEntryHelperExits condition (https://github.com/kaltura/server/pull/7833)
- PLAT-9424: Bulk upload fails due to PHP parse error (https://github.com/kaltura/server/pull/7834)

* Thu Nov 15 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.8.0-17
- PLAT-9419: DRM (WV,ISM,AtRest) conversion status is not updated once done (https://github.com/kaltura/server/pull/7825)
- PLAT-9315: DocumentsService::addFromUploadedFileAction() - Set fileSize when adding content (https://github.com/kaltura/server/pull/7823)
- PLAT-9241: playManifestAction() - handle watermark flavors (https://github.com/kaltura/server/pull/7821)
- isInternalIp(): Support CIDR range of 0.0.0.0 (https://github.com/kaltura/server/pull/7817)
- PLAT-9315: File size of DocumentEntry is always 0 (https://github.com/kaltura/server/pull/7816)
- PLAT-9414: If a 'security map is not defined, allow all internal IPs (https://github.com/kaltura/server/pull/7814)
- PLAT-9411: Reduce number of writes to kConf key in APC (https://github.com/kaltura/server/pull/7807)
- PLAT-9408: Check whether getAudioLanguage() and getAudioCodec() exist for the object before attempting to call them (https://github.com/kaltura/server/pull/7806)
- PLAT-9404: createRecordedEntry() - check if lock exists before calling unlock() (https://github.com/kaltura/server/pull/7805)
- sup-15616: addClipJobs() - skip flavour creation if duration is not set to a positive value (https://github.com/kaltura/server/pull/7803)
- PLAT-9393: Add the BASE_UPLOAD_PERMISSION permission to media:addFromUplodedFile (https://github.com/kaltura/server/pull/7800)
- PLAT-9381: Handle encrypted thumbs serving (https://github.com/kaltura/server/pull/7786)
- Catch couchbase exception and return empty list as a response (https://github.com/kaltura/server/pull/7785)
- PSVAMB-4443: Allow global access to entries from partner 0 (https://github.com/kaltura/server/pull/7781)
- SUP-15841: kFlowHelper - added validateSourceFileSync() (https://github.com/kaltura/server/pull/7780)
- PLAT-9230: Playlist service - allow user level access (add/update operations) (https://github.com/kaltura/server/pull/7778)
- Update default flavour set (https://github.com/kaltura/server/pull/7772)
- SUP-15174: Handle BOM in CSV bulk upload (https://github.com/kaltura/server/pull/7770)
- Chunked encoding: compress data when storing in Memcache (https://github.com/kaltura/server/pull/7765)

* Mon Oct 29 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.7.0-15
- thumbnail action - block inactive partners (https://github.com/kaltura/server/pull/7744)
- Reduce access to APC (https://github.com/kaltura/server/pull/7743)
- kApcConf.php: Add map prefix (https://github.com/kaltura/server/pull/7742)
- KalturaLiveEntry: when checking hasPropertyChanged, if `sourceObject` is null and value is set return true (https://github.com/kaltura/server/pull/7739)
- PLAT-9352: kRemoteMemCacheConf.php - fix hostname regex pattern (https://github.com/kaltura/server/pull/7738)
- When entryVendorTask is auto generated assign the entry userId as the entry owner, if requester partnerId is one of the system partners (https://github.com/kaltura/server/pull/7737)
- Added script to sync DB conf maps to multiple cache (https://github.com/kaltura/server/pull/7736)
- Block deleted (status 0) partners (https://github.com/kaltura/server/pull/7735)
- PLAT-9349: Fix inconsistent behavior between kConf::getMap() and kConf::hasMap() (https://github.com/kaltura/server/pull/7734)
- PLAT-9349: Fix inconsistent behavior between kConf::getMap() and kConf::hasMap()(https://github.com/kaltura/server/pull/7732)
- PLAT-9348: Indexes with underscore in names aren't added to memcache (https://github.com/kaltura/server/pull/7731)
- PLAT-9347: Reload content from file system if the base.reload file exist (https://github.com/kaltura/server/pull/7730)
- PLAT-9345: Handle caching of unkown types (https://github.com/kaltura/server/pull/7726)
- PLAT-9309: Admin Console DRM config - expose `fps_default_persistence_duration` (https://github.com/kaltura/server/pull/7725)
- PLAT-9344: Rename kBaseCacheWrapper to kInfraMemcacheCacheWrapper (https://github.com/kaltura/server/pull/7722)
- Split firebase IOS and Android notifications (https://github.com/kaltura/server/pull/7720)
- PLAT-9344: Avoid duplicate cache class names (https://github.com/kaltura/server/pull/7718)
- PLAT-9340: Preload configuration of kRemoteMemCache and kLocalMemCache (https://github.com/kaltura/server/pull/7712)
- PLAT-9343 eSearch: searchHistory - limit the length of searchTermStartsWith to 64 (https://github.com/kaltura/server/pull/7711)
- PLAT-9342: Avoid map merging if only one file is found (https://github.com/kaltura/server/pull/7710)
- eSearch: Fix field validation in searchUser() action (https://github.com/kaltura/server/pull/7707)
- PLAT-9142: Add `privacy_by_contexts` field to entry index (https://github.com/kaltura/server/pull/7706)
- PLAT-9266: Fix param parsing in dumpApiRequest() (https://github.com/kaltura/server/pull/7703)
- SUP-15772: retrieveActiveAndPendingByEntryIdAndPrivacyContext() - search through all categoryEntryObjects with privacyContext (https://github.com/kaltura/server/pull/7702)
- PLAT-9340: Fix wrong handling of wildcard in kConf (https://github.com/kaltura/server/pull/7700)
- SUP-15746: apply approve/cancel replacement flow for child media entries (https://github.com/kaltura/server/pull/7699)
- PLAT-9336: Support multi-request with a dependent request that extracts results from objects array (https://github.com/kaltura/server/pull/7698)
- PLAT-9331: Fix merging of associative array configuration files with numeric keys (https://github.com/kaltura/server/pull/7695)
- PHP7: get_class() no longer supports explicitly passing NULL in the object param (https://github.com/kaltura/server/pull/7694)
- PSVAMB-4593: New Email notifications (https://github.com/kaltura/server/pull/7692)
- PLAT-8932: Fix "do not implement countable()" errors (https://github.com/kaltura/server/pull/7691)
- PLAT-9183: kBulkUploadJob() - apply moderation  (https://github.com/kaltura/server/pull/7690)
- PLAT-8932: Avoid recursive calling kConf::load() (https://github.com/kaltura/server/pull/7688)

* Tue Oct 16 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.7.0-1
- Ver Bounce to 14.7.0

* Mon Oct 15 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.6.0-43
- SUP-15684: TranscriptPlugin.php - handle plain text files as well (not just JSON) (https://github.com/kaltura/server/pull/7677)
- getPlaybackContext - include dash flavors in hls (https://github.com/kaltura/server/pull/7674)
- PHP7: Follow PHP strict standards. serverFile() expects 3 parameters while only 2 are being sent (https://github.com/kaltura/server/pull/7670)
- PHP7: Add php7.2 Support for checking if session is active to avoid exception when distributing to Facebook (https://github.com/kaltura/server/pull/7666)
- Fix live reports notice on empty result set (https://github.com/kaltura/server/pull/7664)
- Skip analytics log print on cached multi-request part (https://github.com/kaltura/server/pull/7663)
- PLAT-9190: Zoom-Kaltura integration (https://github.com/kaltura/server/pull/7662)
- Drop Object.assign() call (https://github.com/kaltura/server/pull/7661)
- PLAT-9305: Facebook auth request - use HTTPs endpoint (https://github.com/kaltura/server/pull/7660)
- KMC player preview: fix ie11 issue (https://github.com/kaltura/server/pull/7659)
- PHP7: Explicitly passing NULL as the object when calling get_class() is no longer allowed (https://github.com/kaltura/server/pull/7658)
- SUP-15684: TranscriptPlugin.php - added getValues() method (https://github.com/kaltura/server/pull/7656)
- PLAT-9237: Added 2018_10_09_update_bulk_sync_group_users_permissions.php (https://github.com/kaltura/server/pull/7655)
- PLAT-9299: Add 'filter_units' to ffmpeg cmd-lines (https://github.com/kaltura/server/pull/7649)
- PLAT-9256: Cache thumbnail for non block and limit thumbnail capture access control actions (https://github.com/kaltura/server/pull/7646)
- PLAT-9286: eSearch - save search terms even if no results were returned (https://github.com/kaltura/server/pull/7637)
- KMS-18522: entryVendorTaskPeer.php - Don't return aborted tasks (https://github.com/kaltura/server/pull/7636)
- PLAT-8950: REACH - Add support for filtering entry vendor tasks based on target language (https://github.com/kaltura/server/pull/7634)
- SUP-15727-fix-NGS-cmdLine (https://github.com/kaltura/server/pull/7633)
- PHP7: Ensure getStreamInfo() always returns an array object to avoid PHP Warning when calling count on it (https://github.com/kaltura/server/pull/7628)
- PLAT-9255 + PLAT-6772: handle enc_at_rest flavor conversion and thumb generation (https://github.com/kaltura/server/pull/7626)
- PLAT-9262: handle thumb and volume mapped with encryption (https://github.com/kaltura/server/pull/7625)
- PHP7.2: Avoid PHP Fatal error caused by passing too few arguments to function KalturaException::__construct(), 2 passed instead of 3 (https://github.com/kaltura/server/pull/7624)
- PLAT-9237: groupuser->sync does not handle special characters (https://github.com/kaltura/server/pull/7623)
- PHP7.2: to, cc and bcc do not implement countable() (https://github.com/kaltura/server/pull/7621)
- PLAT-7848: override __call function to restore http/s wrappers (https://github.com/kaltura/server/pull/7620)
- PLAT-8342: limit reset password per email and IP to avoid flooding (https://github.com/kaltura/server/pull/7619)

* Mon Aug 27 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.5.0-16
- PLAT-9163: Handle ingested flavors with 639-2B and 639-3 language codes (https://github.com/kaltura/server/pull/7533)
- PLAT-9163: Handle ingested flavors with 639-2B and 639-3 language codes (https://github.com/kaltura/server/pull/7527)
- SUP_15188: Align UTF8 string when adding or updating kuser name fields (https://github.com/kaltura/server/pull/7531)
- SUP-15188: Align UTF8 string kuser name fields (https://github.com/kaltura/server/pull/7523)
- PLAT-9037: Increase max number of groups per user (https://github.com/kaltura/server/pull/7529)
- PLAT-9181: Add option to avoid invalidation in CouchBase for specific partners (https://github.com/kaltura/server/pull/7526)
- Add priority to isSubstitute() check (https://github.com/kaltura/server/pull/7520)
- Apply CDN switching only to DP with the same attributes (https://github.com/kaltura/server/pull/7519)
- Apply CDN switching only to DP with the same path (https://github.com/kaltura/server/pull/7518)
- Cost base multi CDN support (https://github.com/kaltura/server/pull/7517)
- Limit bulk service `list` action to use only last 300K records when filtering events (https://github.com/kaltura/server/pull/7516)
- When using dynamic response profiles calculate the hasKey by serializing the response profile object (https://github.com/kaltura/server/pull/7515)
- PLAT 9130: thumbnail `execute` action - added validations (https://github.com/kaltura/server/pull/7514)
- PLAT-8904: Sphinx load balancing phase 1 (https://github.com/kaltura/server/pull/7485)

* Mon Aug 13 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.5.0-1
- Ver Bounce to 14.5.0

* Fri Aug 10 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.4.0-4
- addFromUrl(): Throw exception in case the result is empty (https://github.com/kaltura/server/pull/7505)
- KMS-18227: Add custom role for Kaltura's caption editor application (https://github.com/kaltura/server/pull/7500)
- PLAT-9121: DeliveryProfileLive.php - reverse sorting order (https://github.com/kaltura/server/pull/7499)
- quiz: Avoid calling UserEntryPeer::retrieveByPK() per answer (https://github.com/kaltura/server/pull/7498)
- Add the `X-XSS-Protection` header to KMCng (https://github.com/kaltura/server/pull/7491)
- PLAT-9126: Add monitoring to Couchbase calls (https://github.com/kaltura/server/pull/7488)
- Adjust auto inc for `dynamic_enums` and `partner` tables (https://github.com/kaltura/server/pull/7487)
- bulk->listAction(): limit to the last 100K records in order to constrain query performance (https://github.com/kaltura/server/pull/7483)
- PLAT-9124: Validate response profile before generating Couchbase key (https://github.com/kaltura/server/pull/7477)
- PLAT-9122: Allow returning indexed array with Couchbase extracted values (https://github.com/kaltura/server/pull/7473)
- sup-14543: Quiz - Non-Latin chars turn to gibberish when downloading PDF (https://github.com/kaltura/server/pull/7470)
- PLAT-9067: KMC partner creation - new email template (https://github.com/kaltura/server/pull/7465)

* Tue Jul 31 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.4.0-1
- Ver Bounce to 14.4.0

* Mon Jul 30 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.3.0-8
- PLAT-9138: Add missing privileges to allow entry view & download (https://github.com/kaltura/server/pull/7474)
- in case KalturaServiceClassToId cache file does not exist (https://github.com/kaltura/server/pull/7472)
- PLAT-9135: Added reach profile max chars per line default value (https://github.com/kaltura/server/pull/7471)
- PLAT-9127: Allow vendors to impersonate operating task account (https://github.com/kaltura/server/pull/7469)
- PLAT-9032: lowercase additional params before checking for account type (https://github.com/kaltura/server/pull/7468)
- SUP-14981: due to Itunes limitations, removing unnecessary fields (https://github.com/kaltura/server/pull/7467)
- Ignore related service validation for reachProfile (https://github.com/kaltura/server/pull/7461)
- ThumbnailDescriptor: prevent division by zero. (https://github.com/kaltura/server/pull/7460)
- PLAT-9120: Add -5 partner permission to the report service (https://github.com/kaltura/server/pull/7459)
- kava - retry on channel disconnected druid error (https://github.com/kaltura/server/pull/7455)
- Do not override metadata profile field settings if the field was not specified in the schema (https://github.com/kaltura/server/pull/7453)
- PLAT-9115: Block the option to order tasks for an entry whose status is not READY + correctly handle entry duration changes (https://github.com/kaltura/server/pull/7447)
- Align DB schema with SaaS (https://github.com/kaltura/server/pull/7429)
- Naos 14.3.0-SUP-14718 filtering whitelisted delivery profiles when retrieving default delivery profiles (https://github.com/kaltura/server/pull/7426)
- KMCng: Do not force redirect to HTTP and login process modifications (https://github.com/kaltura/server/pull/7423)
- PSVAMB-3750: Add subtitle track name to data search (https://github.com/kaltura/server/pull/7420)
- PLAT-9101 MR dry run list to all types extending baseEntry (https://github.com/kaltura/server/pull/7418)
- PLAT-8248: Added getClipData() (https://github.com/kaltura/server/pull/7411)
- PLAT-8908: Multi DC configuration - do not check costume data on the other DC (https://github.com/kaltura/server/pull/7410)

* Tue Jul 24 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.3.0-1
- Ver Bounce to 14.3.0

* Mon Jul 23 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.2.0-14
- SUP-14941: Fix multi account login (https://github.com/kaltura/server/pull/7421)
- PLAT-9100: Hotfix for Response Profile (https://github.com/kaltura/server/pull/7414)
- Fix link from legacy KMC to KMCng, providing KS of logged-in user (https://github.com/kaltura/server/pull/7409)
- PLAT-9091: Adjust Facebook auth request permissions (https://github.com/kaltura/server/pull/7399)
- PLAT-9062: Return value from soapCall() (https://github.com/kaltura/server/pull/7391)
- Fix Media repurposing admin console listing and dry runner log to support REACH (https://github.com/kaltura/server/pull/7390)
- PLAT-9064: filter scheduledTasks that were not handled the current day (https://github.com/kaltura/server/pull/7388)
- PLAT-9062: kSoapClient - override  __soapCall (https://github.com/kaltura/server/pull/7387)
- PLAT-8941: move the config json string up to Delivery Server Node (https://github.com/kaltura/server/pull/7386)
- PLAT-9019: YouTube distributor - custom match and usage policy (https://github.com/kaltura/server/pull/7381)
- Fix Curl Wrapper response for Http notification (https://github.com/kaltura/server/pull/7378)
- PLAT-8903: Optimise kContentDistribution (https://github.com/kaltura/server/pull/7374)
- KMCNG-1941: Add link to the html based kmc from the flash based kmc (https://github.com/kaltura/server/pull/7373)
- PLAT-9075: handle filter generation for abstract class (https://github.com/kaltura/server/pull/7370)
- Handle filtering 0 enum value (https://github.com/kaltura/server/pull/7369)
- Use smaller chunk size for delayed file sync pull (https://github.com/kaltura/server/pull/7366)
- Ensure the serviceClassToIdAndName array is populated when service item is being fetched from cache (https://github.com/kaltura/server/pull/7365)
- admin_console/configs/lang/en.php - Added Thai (https://github.com/kaltura/server/pull/7364)
- PLAT-8915: Response profile access validation (https://github.com/kaltura/server/pull/7363)
- Add missing relatedService annotations (https://github.com/kaltura/server/pull/7361)
- Add missing class annotation to avoid error when using reach objects as a part of a response profile (https://github.com/kaltura/server/pull/7360)
- PLAT-9044: Cue point merging  (https://github.com/kaltura/server/pull/7357)
- PLAT-9062: SoapServer - allow remote access (https://github.com/kaltura/server/pull/7355)
- limit the number of last_login_pid updates (https://github.com/kaltura/server/pull/7351)
- PLAT-8484: add -5 permission to liveConversionProfile (https://github.com/kaltura/server/pull/7349)
- add kmcng_version to local.ini (https://github.com/kaltura/server/pull/7340)
- PLAT-8915: Response profile access validation (https://github.com/kaltura/server/pull/7313)
- Avoid fetching none default delivery profiles (https://github.com/kaltura/server/pull/7161)


* Tue Jul 3 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.1.0-18
- Depend on php-mysqli and php-pdo_mysql rather than on php-mysql

* Mon Jul 2 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.1.0-16
- verifyObjectDeletion - increase chunk size (https://github.com/kaltura/server/pull/7337)
- PLAT-8581: ValidateMetadataObjectAccess should not return false if session is of admin type (https://github.com/kaltura/server/pull/7336)
- PLAT-9034 Upgrade facebook distributor to graph API v3.0 (https://github.com/kaltura/server/pull/7331)
- PLAT-8940 facebook new auth logic (https://github.com/kaltura/server/pull/7330)
- SUP-14624: Support of Mac/Win EOL in serveWebVTTAction (https://github.com/kaltura/server/pull/7329)
- getIpFromHttpHeader(): support IPv6 addresses (https://github.com/kaltura/server/pull/7325)
- ip2location - support single file with IPv4 & 6 (https://github.com/kaltura/server/pull/7324)
- SUP-14753: Perform clip action on source DC if the file is not accesible from the current DC (https://github.com/kaltura/server/pull/7320)
- PLAT-8507: Return empty KalturaMetadataArray if object ID is not found (https://github.com/kaltura/server/pull/7317)
- Fix eventConditions for SLIDE_VIEW_CHANGE_CODE_CUE_POINT notification (https://github.com/kaltura/server/pull/7314)
- PLAT-9002: playManifest fix (https://github.com/kaltura/server/pull/7309)
- KMS-17960: Set status to pending and do not set duration if no flavours exist (https://github.com/kaltura/server/pull/7306)
- PLAT-9025: updateContent action - abort replacement process if an exception was raised (https://github.com/kaltura/server/pull/7304)
- SUP-14641: set thumb URL to the correct version (https://github.com/kaltura/server/pull/7300)
- PLAT-8952: Live clipping engine - handle cue points (https://github.com/kaltura/server/pull/7299)
- Correct action annotations (https://github.com/kaltura/server/pull/7210)
* Mon Jun 18 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.1.0-1
- Ver Bounce to 14.1.0

* Mon Jun 18 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.0.0-15
- Redirect the live thumb when stream to other DC (https://github.com/kaltura/server/pull/7289)
- Fix package annotations on reach related list objects (https://github.com/kaltura/server/pull/7286)
- PLAT-8973: allow force stream type (https://github.com/kaltura/server/pull/7284)
- Fix fatal when checking live entry (https://github.com/kaltura/server/pull/7283)
- PLAT-9001: fix serveMultiFileAction to handle encrypted filesyncs (https://github.com/kaltura/server/pull/7279)
- Fade in/out for single clip (https://github.com/kaltura/server/pull/7278)
- KalturaBatchJobStatus.php: add suspension statuses (https://github.com/kaltura/server/pull/7277)
- PLAT-8998: decrease index when removing a node from the xml object (https://github.com/kaltura/server/pull/7276)
- PLAT-8985: Define live concurrency limits for new accounts (https://github.com/kaltura/server/pull/7273)
- PLAT-8985: Define live concurrency limits for new accounts (https://github.com/kaltura/server/pull/7272)
- KLiveToVodCopyCuePointEngine.php: reduce segment time to 6 sec (https://github.com/kaltura/server/pull/7267)
- Admin Console HLS delivery profile: merge advanced and parent settings (https://github.com/kaltura/server/pull/7265)
- Plat-8995: Make bulk upload CSV work in multi request (https://github.com/kaltura/server/pull/7264)
- PLAT-8985: Define live stream limits (https://github.com/kaltura/server/pull/7263)
- Change CATEGORY_ID_THAT_DOES_NOT_EXIST value to avoid slow sphinx query (https://github.com/kaltura/server/pull/7262)
- PLAT-8952: Live Clipping engine: check cue point times before copying (https://github.com/kaltura/server/pull/7258)
- PLAT-8974: Allow setting LivePackagerSigningDomain from admin console (https://github.com/kaltura/server/pull/7255)
- PLAT-8980: Update firebase notification (https://github.com/kaltura/server/pull/7253)
- Increase MaxDimensions to support VR360 w/4K (https://github.com/kaltura/server/pull/7251)
- Use unique string for none existing entry ID const to avoid long query time when value is added to sphinx match optimization (https://github.com/kaltura/server/pull/7248)
- PLAT-8583: YouTube is switching to a new CSV based feed (https://github.com/kaltura/server/pull/7243)
- Plat-8829: Validate config INIs (https://github.com/kaltura/server/pull/7242)
- PLAT-8967: Optimize bulk upload closing time for short tasks (https://github.com/kaltura/server/pull/7238)
- WEBC-1188: Enable RTC tokenization (https://github.com/kaltura/server/pull/7237)
- PLAT-8952: Set lastSyncTime for live clipping to the created time of the live entry (https://github.com/kaltura/server/pull/7236)
- PLAT-8583: youtube sftp distribution (https://github.com/kaltura/server/pull/7235)
- SUP-14595: Chunked Encoding - prevent unintentional lang setting (https://github.com/kaltura/server/pull/7231)
- SUP-14517: Chunked Encoding - fix inaccurate FPS (https://github.com/kaltura/server/pull/7229)


* Tue Jun 5 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.0.0-1
- Ver Bounce to 14.0.0

* Tue Jun 5 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.20.0-31
- PLAT-7514-PHP-5.3 bug (https://github.com/kaltura/server-saas-config/pull/1412)

* Mon Jun 4 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.20.0-30
- PLAT-8583: YouTube SFTP Connector Migration to CSV (https://github.com/kaltura/server/pull/7217)
- plat-8583: YouTube SFTP Connector Migration to CSV (https://github.com/kaltura/server/pull/7211)
- PLAT-8966: Set property isMomentary to read only (https://github.com/kaltura/server/pull/7213)
- Fix insertPermissions script for groupUser service (https://github.com/kaltura/server/pull/7206)
- KMS-17587: Added momentary cue flag for clipping  (https://github.com/kaltura/server/pull/7203)
- KMS-17656: If parent id is null, set to 0 to maintain compatiblity (https://github.com/kaltura/server/pull/7198)
- SUP-14520 chunks with faststart (https://github.com/kaltura/server/pull/7195)
- Allow change account for users with KMC_ACCESS permission (https://github.com/kaltura/server/pull/7194)
- Add notification for slides view change (https://github.com/kaltura/server/pull/7188)
- PLAT-8531: must call postUpdate of parent (https://github.com/kaltura/server/pull/7183)
- Use the version uiconf instead of the latest.json and beta.json files (https://github.com/kaltura/server/pull/7182)
- PLAT-8901: KalturaSyndicationFeedRenderer.php - only return entryStatus::READY (https://github.com/kaltura/server/pull/7181)
- FEV-186: Support sending push notification when thumb cue point becomes ready (https://github.com/kaltura/server/pull/7177)
- Allow order by status on entry vendor task (https://github.com/kaltura/server/pull/7176)
- PLAT-8867: Get live thumb by positive offset (https://github.com/kaltura/server/pull/7174)
- PLAT-8939: Before adding a task for catalog item defined on the action validate that it is allowed for partner (https://github.com/kaltura/server/pull/7172)
- SUP-14485: Use job createdAt instead of queued_time to determine timeout (https://github.com/kaltura/server/pull/7169)
- PLAT-8935: Move synonyms to use contraction (https://github.com/kaltura/server/pull/7168)
- PLAT-8870: Remove the use of increaseEntriesChangedNum (https://github.com/kaltura/server/pull/7166)
- PLAT-8770: Media Repurposing private content bug (https://github.com/kaltura/server/pull/7162)
- PLAT-8926: Add remove/create flags to groupUser sync action (https://github.com/kaltura/server/pull/7157)
- PLAT-8458: KCopyCuePointEngine.php refactoring (https://github.com/kaltura/server/pull/7155)
- If entryId is available on the object use it when building the cacheKey (https://github.com/kaltura/server/pull/7153)

* Tue May 8 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.20.0-1
- Ver Bounce to 13.20.0

* Tue May 8 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.19.0-14
- PLAT-8878: Importing file_sync objects between DCs fails in case the file points to a directory (https://github.com/kaltura/server/pull/7070)
- PLAT-8827: change serveWebVTT to use delivery profile hostname (https://github.com/kaltura/server/pull/7069)
- PLAT-8844: KMC-NG configurations (https://github.com/kaltura/server/pull/7066)
- Remove update status from the add template request and add explicit-live to init.content (https://github.com/kaltura/server/pull/7064)
- SUP-14278: WebEx dropfoler - fix delete by name (https://github.com/kaltura/server/pull/7063)
- Don't set duration if flow type is EntryFlowType::LIVE_CLIPPING (https://github.com/kaltura/server/pull/7062)
- FEC-8162: Player: add a wildcard to the Policy Controlled Features (https://github.com/kaltura/server/pull/7060)
- Dynamically adjust max concurrency of chunked asset session (https://github.com/kaltura/server/pull/7058)
- PLAT-7832: support live clipping (https://github.com/kaltura/server/pull/7057)
- PLAT-7832: Support live clipping (https://github.com/kaltura/server/pull/7052)
- Transcript plugin: only index text assets (https://github.com/kaltura/server/pull/7056)
- PLAT-8543: syndication feed fix (https://github.com/kaltura/server/pull/7055)
- SUP-14231: Verify HTTP RC is not erroneous (https://github.com/kaltura/server/pull/7054)
- Disable Encoding.com transcoder (https://github.com/kaltura/server/pull/7053)
- Assign default values to metadataProfileField matchType & trimChars (https://github.com/kaltura/server/pull/7048)
- PLAT-8543: itunes syndication feed (https://github.com/kaltura/server/pull/7045)
- PLAT-8827: change serveWebVTT to use delivery profile hostname (https://github.com/kaltura/server/pull/7039)
- PLAT-8820: add segment duration to serveWebVTT url (https://github.com/kaltura/server/pull/7038)
- SUP-14151: fix retry on Widevine packager failure (https://github.com/kaltura/server/pull/7037)
- PLAT-8792: firebase event notification template update (https://github.com/kaltura/server/pull/7036)
- PLAT-8832: Add missing LANGUAGE field to HLS Master playlist manifest (https://github.com/kaltura/server/pull/7035)
- PSVAMB-3002: Add option for ip tokenization to the Akamai Tokenizer (https://github.com/kaltura/server/pull/7032)
- SUP-13559:  privacyContext Fix (https://github.com/kaltura/server/pull/7031)
- PLAT-8701: Support COPY operation for MP3 sources (https://github.com/kaltura/server/pull/7025)
- PLAT-8651: Chop and slice (https://github.com/kaltura/server/pull/7022)
- SUP-13826: Add ogg file extension to supported types (https://github.com/kaltura/server/pull/7021)
- PLAT-8543: Episode Author Field in iTunes Syndication (https://github.com/kaltura/server/pull/7020)
- Improve sphinx query time for metadata match by adding support for defining matchType and providing split & explode chars (https://github.com/kaltura/server/pull/6984)
* Mon Apr 23 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.19.0-1
- Ver Bounce to 13.19.0

* Mon Apr 23 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.18.0-16
- PLAT-8311: remove partner_in for partner 0 when running sphinx entry queries (https://github.com/kaltura/server/pull/6962)
- PLAT-8552: youtubeApi encryption support (https://github.com/kaltura/server/pull/6955)
- PLAT-8651: Chop and Slice (https://github.com/kaltura/server/pull/6963)
- plat 8651: Chop and slice: multi audio fix (https://github.com/kaltura/server/pull/6978)
- PLAT-8651: Chop and Slice refactoring (https://github.com/kaltura/server/pull/6968)
- Plat 8651: kClipManager.php: optimise batch jobs retrieval (https://github.com/kaltura/server/pull/6990)
- PLAT-8738: Only create a user_add_ lock in the event the kuser does not exist (https://github.com/kaltura/server/pull/6970)
- PLAT-8755: Add support for multiple IP values in a single range (https://github.com/kaltura/server/pull/6976)
- PLAT-8785: Add categoryUserItem to categorySearch (https://github.com/kaltura/server/pull/6995)
- PLAT-8785: Return kuserId as string (https://github.com/kaltura/server/pull/6999)
- PSVAMB-2895: Fix delivery profile lookup (https://github.com/kaltura/server/pull/6985)
- SUP-13925: Update child categories based on the parent's status (https://github.com/kaltura/server/pull/6972)
- SUP-13945: DeliveryProfileAkamaiHttp.php: get file extension from container format element (https://github.com/kaltura/server/pull/6989)
- SUP-14139: Fix FtpDistributionEngine (https://github.com/kaltura/server/pull/7006)
- SUP-14195: Attr name in map should match its definition to avoid the data stored on it to be lost when fetching the object (https://github.com/kaltura/server/pull/7015)

* Mon Apr 9 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.18.0-1
- Ver Bounce to 13.18.0

* Mon Apr 9 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.17.0-17
- apimon - log conditional cache sql validations (https://github.com/kaltura/server/pull/6957)
- PLAT-8768: Invalidate cache when updating answer cuepoint (https://github.com/kaltura/server/pull/6951)
- Fix plugins dependency, required for Swift client lib (https://github.com/kaltura/server/pull/6948)
- PLAT-8708: add `ASE_USER_SESSION_PERMISSION` permission to fileAsset service (https://github.com/kaltura/server/pull/6946)
- SUP-13191: KAsyncLiveToVod - in the event `cuePoint->listAction()` failed, retry (https://github.com/kaltura/server/pull/6944)
- Plat 8651: kClipManager - set partner Id on the BatchJob object (clip concat) (https://github.com/kaltura/server/pull/6943)
- SUP-13990: Fix seek issues with large GOPs (https://github.com/kaltura/server/pull/6939)
- plat 8651: chop and slice (https://github.com/kaltura/server/pull/6938)
- WEBC-1162: add lastBroadcastEndTime to KalturaLiveEntry (https://github.com/kaltura/server/pull/6936)
- PLAT-8735: Skip Sphinx query for specific partners and actions (https://github.com/kaltura/server/pull/6929)
- SUP-13708: Update embedCodeGenerator (https://github.com/kaltura/server/pull/6927)
- SUP-13708: Add allow="autoplay; fullscreen; encrypted-media" to player iframe (https://github.com/kaltura/server/pull/6925)
- KalturaDocCommentParser: add the ability to annotate services and actions as beta (https://github.com/kaltura/server/pull/6923)
- PLAT-8551: Distribution - correctly handle encrypted files (https://github.com/kaltura/server/pull/6921)
- SUP-13039: Playing apple http with non kaltura live (https://github.com/kaltura/server/pull/6920)
- SUP-13614 - Include entry flavor version when requesting playManifest (https://github.com/kaltura/server/pull/6913)
- PLAT-8311 - Fetch partner ID 0's static playlists from the DB rather than Sphinx (https://github.com/kaltura/server/pull/6903)
- exportToCsvAction(): KalturaUserFilter $filter can be null (https://github.com/kaltura/server/pull/6902)

* Mon Mar 26 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.17.0-1
- Ver Bounce to 13.17.0

* Mon Mar 26 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-16
- SUP-13320: data::serveAction() - pass key and IV to dumpFile() (https://github.com/kaltura/server/pull/6901)
- webrtc/AVC recordings: if FR==0, set FR to 30 (https://github.com/kaltura/server/pull/6890)
- SUP-13904: Handle chunk split edge conditions (https://github.com/kaltura/server/pull/6887)
- Handle cases where LastLoginTime is empty (https://github.com/kaltura/server/pull/6886)
- Only update LastLoginTime if more than 600 seconds passed since the last update (https://github.com/kaltura/server/pull/6885)
- PLAT-8695: Quiz mechanism - allow excluding questions from score (https://github.com/kaltura/server/pull/6874)
- Added missing params.ffmpegCmd directive (https://github.com/kaltura/server/pull/6866)
- Chunked Encoding: for the last chunk, make sure that the loop/t period does not overflow the end of the file (https://github.com/kaltu
- SUP-13373: Support setting the default audio track in the manifest (https://github.com/kaltura/server/pull/6862)
- PLAT-8697: Extend FileAsset so it can handle objectType of type entry (https://github.com/kaltura/server/pull/6861)
- It is not possible to unset $this inside an object method (https://github.com/kaltura/server/pull/6858)
- Align the declaration of entry::save() with that of Baseentry::save() (https://github.com/kaltura/server/pull/6847)
- Use OpenSSL functions if mcrypt is not available (https://github.com/kaltura/server/pull/6826)
- SUP-13039: Live streaming: protocol selection improvements (https://github.com/kaltura/server/pull/6783)
- PLAT-8723: User Id should always be lowercase when testing match (https://github.com/kaltura/server/pull/6907)

* Sun Mar 25 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-15
- Nightly build.

* Sat Mar 24 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-14
- Nightly build.

* Fri Mar 23 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-13
- Nightly build.

* Thu Mar 22 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-12
- Nightly build.

* Wed Mar 21 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-11
- Nightly build.

* Tue Mar 20 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-10
- Nightly build.

* Mon Mar 19 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-9
- Nightly build.

* Sun Mar 18 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-8
- Nightly build.

* Sat Mar 17 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-7
- Nightly build.

* Fri Mar 16 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-6
- Nightly build.

* Thu Mar 15 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-5
- Nightly build.

* Wed Mar 14 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-4
- Nightly build.

* Tue Mar 13 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-3
- Nightly build.

* Mon Mar 12 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-2
- Nightly build.

* Mon Mar 12 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-1
- Ver Bounce to 13.16.0

* Fri Mar 9 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.15.0-13
- PLAT-8685: Get thumb file only if exists (https://github.com/kaltura/server/pull/6849)
- Fix first time input for field array configuration of type select (https://github.com/kaltura/server/pull/6844)
- PLAT-8645: Event notification: entry added to category fire base template (https://github.com/kaltura/server/pull/6843)
- Media Repurposing: added max entries limitation to dry run (https://github.com/kaltura/server/pull/6842)
- KMS-17162: Add ability to disallow live explicitly (https://github.com/kaltura/server/pull/6840)
- PLAT-8550: Add support for encrypted thumbnail - Facebook (https://github.com/kaltura/server/pull/6838)
- PLAT-8499: Add presentation order field to question cue point (https://github.com/kaltura/server/pull/6835)
- PLAT-8619: Order cue point items by start time (https://github.com/kaltura/server/pull/6834)
- PLAT-8645: New categoryEntry firebase http notification template (https://github.com/kaltura/server/pull/6832)
- PLAT-8550: Enable Facebook caption distribution for encrypted content (https://github.com/kaltura/server/pull/6827)
- PLAT-8492: Allow the editing of admin tags based on KS privilege (https://github.com/kaltura/server/pull/6823)
- PLAT-8633: Update viewMode and recordingStatus when live entry is no longer in broadcasting mode (https://github.com/kaltura/server/pull/6821)
- uiconf->get() requires a KS (https://github.com/kaltura/server/pull/6761)


* Mon Feb 26 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.15.0-1
- Ver Bounce to 13.15.0

* Mon Feb 26 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.14.0-12
- fix AddMediaEntryReady email template (https://github.com/kaltura/server/pull/6800)
- PLAT-8620: uDRM - clean up mpeg-ts leftovers from remuxed mp4 files (https://github.com/kaltura/server/pull/6799)
- PLAT-8611: disable criteria filter only for batch in cloneEntryAction (https://github.com/kaltura/server/pull/6796)
- PLAT-8584: remove duplicate records creation on csv and handle api exception (https://github.com/kaltura/server/pull/6778)
- Drop unused indexes (https://github.com/kaltura/server/pull/6771)
- PLAT-8526: New Free Trial - Modification of Additional Flow behavior (https://github.com/kaltura/server/pull/6763)

* Mon Feb 12 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.14.0-1
- Ver Bounce to 13.14.0

* Mon Feb 12 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.13.0-14
- Add cue_point.ENTRY_ID to getSphinxConditionsToKeep in order to use the ENTRY_ID query invalidation key (https://github.com/kaltura/server/pull/6774)

* Thu Feb 8 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.13.0-13
- kAsyncUsersCsv: Fix memory and scale issues (https://github.com/kaltura/server/pull/6772)

* Thu Feb 8 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.13.0-12
- kms-16965: add BASE_UPLOAD_PERMISSION to media->addfromrecordedwebcam() (https://github.com/kaltura/server/pull/6768)
- PLAT-8450: additional Chinese dialects (https://github.com/kaltura/server/pull/6760)
- SUP-13366: set the correct conversion profile ID when clipping a recorded entry (https://github.com/kaltura/server/pull/6758)
- Drop unused indexes from caption_asset_item and entry (https://github.com/kaltura/server/pull/6754)
- PLAT-8557: fix ordering on DFP feed advanced pages (https://github.com/kaltura/server/pull/6752)
- Remove setLimit(40) and fetch by version to better use the file_sync index (https://github.com/kaltura/server/pull/6751)
- Change file sync version column from varchar to int in order to optimise the query used to delete old file_sync versions (https://github.com/kaltura/server/pull/6748)
- Don't save SchedulerStatus to prevent unneeded DB insertion load (https://github.com/kaltura/server/pull/6745)
- PLAT-8325: Enable file encryption for KAsyncTransformMetadata (https://github.com/kaltura/server/pull/6744)
- PLAT-8556: set frameRate to 30 if missing from the source video and the codec is vp8 or vp9 (https://github.com/kaltura/server/pull/6741)
- Avoid chunked processing for very short sources (https://github.com/kaltura/server/pull/6739)
- PLAT-8403: CaptionBulkUploadXmlPlugin - enable label value addition (https://github.com/kaltura/server/pull/6737)
- PLAT-8446: get kusers list as CSV (https://github.com/kaltura/server/pull/6733)
- PLAT-8520: Media Repurposing profile is not updated after an entry is deleted (https://github.com/kaltura/server/pull/6732)
- Avoid connecting to both slaves in a single session (https://github.com/kaltura/server/pull/6731)
- PLAT-8538: if the creator and co-publisher are the same user, no need to index them twice (https://github.com/kaltura/server/pull/6729)
- PLAT-8532: add caption label to itemdata result + change caption object nesting level (https://github.com/kaltura/server/pull/6728)
- PLAT-8544: fix flavorParamsOutput->list() returning wrong objects (https://github.com/kaltura/server/pull/6727)
- PSVAMB-419: add -1>PARTNER_-1_GROUP_*_PERMISSION to metadata->delete() (https://github.com/kaltura/server/pull/6725)
- PLAT-8530: only sync relevant file sync objects between DCs (https://github.com/kaltura/server/pull/6722)
- Add query cache rules (https://github.com/kaltura/server/pull/6719)
- set Sphinx cacheExpiry to 30 seconds (instead of 300) (https://github.com/kaltura/server/pull/6718)
- PLAT-8456: Add questionType to the KalturaQuestionCuePoint class (https://github.com/kaltura/server/pull/6717)
- PLAT-8435: Base Upload Permission and User-role (https://github.com/kaltura/server/pull/6714)
- PLAT-8519: only call kEncryptFileUtils::fileSize() if fileSize > 0 (https://github.com/kaltura/server/pull/6709)
- Remove addTrackEntry() (https://github.com/kaltura/server/pull/6708)

* Mon Jan 29 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.13.0-1
- Ver Bounce to 13.13.0

* Mon Jan 29 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.12.0-17
- PLAT-8513: downloadAction() - set $fileSize to null if $filePath is a directory (https://github.com/kaltura/server/pull/6697)
- Chunked Encoding: enforce provided vsync setting (https://github.com/kaltura/server/pull/6686)
- change invalid_session.id to bigint (https://github.com/kaltura/server/pull/6683)
- Support setting partner and allowed types in metadata_list_without_object_filtering_partners (https://github.com/kaltura/server/pull/6679)
- New notification dispatched to channel subscribers when an entry is approved (https://github.com/kaltura/server/pull/6677)
- PLAT-8468: add new permission to create VAST cue point without URL (https://github.com/kaltura/server/pull/6665)
- Improved Chunked Encode compliance verification (https://github.com/kaltura/server/pull/6660)
- Improved Chunked Encode compliance verification (https://github.com/kaltura/server/pull/6659)
- TR-2068: Transcript Processing breaks when ACLs are in use (https://github.com/kaltura/server/pull/6658)
- PSVAMB-1496: bpm notification - send also on metadata creation (https://github.com/kaltura/server/pull/6655)
- PLAT-8465: KalturaRequestDeserializer - if params is not an array - throw API exception (https://github.com/kaltura/server/pull/6653)
- PLAT-8469: change encryption method and support encrypt of large files (https://github.com/kaltura/server/pull/6652)
- SUP-13175: New VOD content replacement notifications (https://github.com/kaltura/server/pull/6649)
- PLAT-8470 encrypt based on media type (https://github.com/kaltura/server/pull/6645)
- SUP-13353: Assign default frame rate when no encoder information is provided

* Mon Jan 15 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.12.0-1
- Ver Bounce to 13.12.0

* Mon Jan 15 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.11.0-12
- Increase the Encrypted file max size to 25 MB (https://github.com/kaltura/server/pull/6638)
- Add delete verification script (https://github.com/kaltura/server/pull/6637)
- TR-1682: Better Error Handling for VoiceBase (https://github.com/kaltura/server/pull/6632)
- PLAT-8404: Enable captions when blocking high bitrate flavors (https://github.com/kaltura/server/pull/6629)
- PLAT-8453: Storage: preserve original file permissions when copying (https://github.com/kaltura/server/pull/6626)
- KMS-16337: fix cue point sub type query with OR operator (https://github.com/kaltura/server/pull/6625)
- PLAT-8449: fix field name in decorator + change shouldEnforceEntitlement to use kEntitlementUtils (https://github.com/kaltura/server/pull/6624)
- Improved memcache error handling (https://github.com/kaltura/server/pull/6622)
- Improved memcache error handling (https://github.com/kaltura/server/pull/6621)
- PLAT-8343: support hevc (h265) flavors in getPlaybackContext (https://github.com/kaltura/server/pull/6619)
- PLAT-8442: Media Re-purposing email notification bug (https://github.com/kaltura/server/pull/6614)
- SUP-12639: throw api error on replacement when source flavor not found (https://github.com/kaltura/server/pull/6610)
- SUP-11664: get live default thumbnail in case the recorded entry is not ready yet (https://github.com/kaltura/server/pull/6606)
- PLAT8405: use a 2 letter language code in HLS manifest (instead of a 3 letter code) (https://github.com/kaltura/server/pull/6594)
- SUP-12956: avoid simultaneous updates to the same Live Entry object when running in multi DC mode (https://github.com/kaltura/server/pull/6540)

* Wed Jan 3 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.11.0-1
- Ver Bounce to 13.11.0

* Wed Jan 3 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.10.0-16
- MR email bug (https://github.com/kaltura/server/pull/6613)

* Fri Dec 29 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.10.0-13
- Increase memory limit for CSV report action to 512M (https://github.com/kaltura/server/pull/6597)
- SUP-12871: Adjust bitrate threshold for CODECS="mp4a.40.2" (https://github.com/kaltura/server/pull/6593)
- SUP-12853: Added reSetMembersCount() to categoryCount script (https://github.com/kaltura/server/pull/6590)
- PLAT-8307: Limit max time for stalled file import (https://github.com/kaltura/server/pull/6586)
- PLAT-8430: Update inner hits size for caption and cue points (https://github.com/kaltura/server/pull/6585)
- addBulkUploadResult(): set bulk job ID only when its null (https://github.com/kaltura/server/pull/6582)
- SUP-12715: substring of tag with utf8 encoding (https://github.com/kaltura/server/pull/6579)
- call dieError() in case bundleConfig does not exist (https://github.com/kaltura/server/pull/6578)
- Fix deletion of caption file syncs (https://github.com/kaltura/server/pull/6577)
- SUP-12871: change the bitrate HLS calculation (https://github.com/kaltura/server/pull/6576)
- Remove protocol from DeliveryProfile url (https://github.com/kaltura/server/pull/6573)
- KMS-16413: store questionCuePoint name in the cue_point_question element (https://github.com/kaltura/server/pull/6572)
- Fix JSON serializer (https://github.com/kaltura/server/pull/6571)
- PLAT-8274: Disable XsendFile for encrypted file (https://github.com/kaltura/server/pull/6570)
- Fix filter issues (https://github.com/kaltura/server/pull/6568)
- PLAT-8332: Check ingestFramerate before setting skipCount for Wowza (https://github.com/kaltura/server/pull/6565)
- PLAT-8294: Support Finnish and Swedish multi audio live flavor params (https://github.com/kaltura/server/pull/6561)
- PLAT-8408: Encrypted folders - set user and group permissions according to the source's (https://github.com/kaltura/server/pull/6560)
- PLAT-8354: Avoid warning when missing label from caption (https://github.com/kaltura/server/pull/6559)
- PLAT-8408: Decrypt the image list xml file (https://github.com/kaltura/server/pull/6556)
- SUP-13055: Add Entry replaced HTTP notification template that excludes kaltura VOD entries (https://github.com/kaltura/server/pull/6555)
- SUP-12938: New Media Repurposing email address selection logic (https://github.com/kaltura/server/pull/6554)
- SUP-13043: KalturaMetadataFilter::validateObjectIdFiltered() - call strtolower() on $objectIds (https://github.com/kaltura/server/pull/6552)
- PLAT-8420: fix php error (https://github.com/kaltura/server/pull/6551)
- PLAT-8408: Enable recursive directory encryption (https://github.com/kaltura/server/pull/6547)
- PLAT-8414: handleConvertFinished() - only iterate over jobs with these statuses: BatchJobType::CONVERT, BatchJobType::CONVERT_COLLECTION, BatchJobType::POSTCONVERT (https://github.com/kaltura/server/pull/6545)

* Tue Dec 19 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.10.0-1
- Ver Bounce to 13.10.0

* Mon Dec 18 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.9.0-16
- PLAT-8409: allow webcast producer to update cue point status (https://github.com/kaltura/server/pull/6533)
- PLAT-8398: add partner -5 to allowed viewers of preview stream in explicit live (https://github.com/kaltura/server/pull/6524)
- PLAT-8396: If no delivery format is supplied, sort all the list (https://github.com/kaltura/server/pull/6522)
- check if bundleConfig exists (https://github.com/kaltura/server/pull/6515)
- SUP-12843: increase entry cache version if isDefault is set on flavor (https://github.com/kaltura/server/pull/6512)
- PLAT-8032: if no push publish is set return null (https://github.com/kaltura/server/pull/6509)
- PLAT-7961: Enable file encryption for the ISMC engine (https://github.com/kaltura/server/pull/6505)
- PLAT-8277: KS v2 multiple values support for disableentitlementforentry privilege (https://github.com/kaltura/server/pull/6500)
- SUP-12993: Fix HTTP error condition (https://github.com/kaltura/server/pull/6496)
- Fix conditional-conv-prof crashes (https://github.com/kaltura/server/pull/6495)
- SUPPS-1311: Raise the limit of email notification recipients (https://github.com/kaltura/server/pull/6488)
- Fix failure on video-only sources (https://github.com/kaltura/server/pull/6487)
- PLAT-8370: Block ingest of m3u8 and MPD files (https://github.com/kaltura/server/pull/6486)
- PLAT-8366: alert when asking for unsupported format in storage delivery profile (https://github.com/kaltura/server/pull/6485)
- Fix fatal error in kFlowHelper when trying to get replacing entry for recorded live (https://github.com/kaltura/server/pull/6484)
- SUP-12715: substring of tag with utf8 encoding (https://github.com/kaltura/server/pull/6480)
- plat-8233: Add "name" to Media Entry Filter (https://github.com/kaltura/server/pull/6476)
- PLAT-8354: grab the label and id from entry that has captions for a given lang (https://github.com/kaltura/server/pull/6473)
- PLAT-8273: Thumbnail resize action should use the packager rather than image magic (https://github.com/kaltura/server/pull/6472)
- PLAT-8315: Check isFileText for encrypted files as well (https://github.com/kaltura/server/pull/6469)
- SUP-11979: Deinterlace thumbs (https://github.com/kaltura/server/pull/6467)
- SUP-11979: Deinterlace thumbs (https://github.com/kaltura/server/pull/6463)
- SUP-11797: Add mediaInfoScanType to the captureThumb (https://github.com/kaltura/server/pull/6464)
- PLAT-8323: Enable file encryption in the post convert batch job (https://github.com/kaltura/server/pull/6456)

* Thu Nov 30 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.8.0-13
- PLAT-8349: app token list filter fix (https://github.com/kaltura/server/pull/6448)
- PLAT-8273: fix Code review comments for croping in the packager (https://github.com/kaltura/server/pull/6441)
- SUP-12533: Add http notification to be triggered when recorded entry was replaced (https://github.com/kaltura/server/pull/6432)
- PLAT-8249: Adding deliveryProfileIds to playManifestAction (https://github.com/kaltura/server/pull/6431)
- PLAT-8273: move deletion of temp encrypted file after combine pictures (https://github.com/kaltura/server/pull/6430)
- Don't create copyCpations job if no captions found on source entry (https://github.com/kaltura/server/pull/6429)
- Fix mediaInfo missing duration info with some MP3 cases (https://github.com/kaltura/server/pull/6423)
- PLAT-8273: Use VOD packager for cropping rather than imageMagick (https://github.com/kaltura/server/pull/6417)
- PLAT-8281: Support sorting flavors order when serving mpegdash (https://github.com/kaltura/server/pull/6413)
- PLAT-7977: Added pushnotificationtemplate-register() permission (https://github.com/kaltura/server/pull/6409)
- PLAT-7387: Media Repurposing UI fix (https://github.com/kaltura/server/pull/6408)
- TR-1693: Email Notification - dispatch to multiple category subscribers (https://github.com/kaltura/server/pull/6407)
- Chunked Encoding: several fixes and additions (https://github.com/kaltura/server/pull/6399)
- Mercury 13.8.0 psvamb321 (https://github.com/kaltura/server/pull/6395)
- PLAT-8282: enable the file encryption on CaptureThumb batch job (https://github.com/kaltura/server/pull/6389)
- TR-2020: Allow partners to set VoiceBase speaker delimiter (https://github.com/kaltura/server/pull/6388)
- PLAT-8285: Add partner id to categoryUser default criteria (https://github.com/kaltura/server/pull/6387)



* Tue Nov 21 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.8.0-1
- Ver Bounce to 13.8.0

* Mon Nov 20 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.7.0-8
- PLAT-7977: minor fix so that redirectEntryId will behave the same way as it used to (https://github.com/kaltura/server/pull/6358)
- Fix getting file with dump renderer (https://github.com/kaltura/server/pull/6356)
- PLAT-8242: When setting Label or Language on Flavor - increase cache version of entry (https://github.com/kaltura/server/pull/6350)
- Run convert processes check before vidslice loop (https://github.com/kaltura/server/pull/6345)
- Improve log of failed chunk job (https://github.com/kaltura/server/pull/6342)
- KMS-14875: fix regex for finding alphanumeric in all languages (https://github.com/kaltura/server/pull/6340)
- PLAT-8120: add exists query to reference id (https://github.com/kaltura/server/pull/6338)
- Chunked Encoding - improved FetchNextJob (https://github.com/kaltura/server/pull/6337)
- Chunked Encoding - Improved 'job-skip' detection (https://github.com/kaltura/server/pull/6336)
- Chunked Encoding - fixes and updates (https://github.com/kaltura/server/pull/6335)
- Chunked Encoding - concurrency reports (https://github.com/kaltura/server/pull/6334)
- PLAT-8240: Duplicate entries in MR notification mail (https://github.com/kaltura/server/pull/6332)
- When serving live order by primary DC first (https://github.com/kaltura/server/pull/6331)
- PLAT-8236: set loginEnabled to @insertonly (https://github.com/kaltura/server/pull/6330)
- PLAT-7961: added max_file_size_for_encryption directive (https://github.com/kaltura/server/pull/6328)
- Fix category privacy + return only category id in entitlement query (https://github.com/kaltura/server/pull/6327)
- PLAT-7961: add file size check before encrypting/decrypting (https://github.com/kaltura/server/pull/6323)
- Update bpmNotificationsTemplates.xml (https://github.com/kaltura/server/pull/6322)
- PLAT-8219: add projected audience parameter to live schedule event (https://github.com/kaltura/server/pull/6321)
- SUP-12622: KWebexDropFolderEngine.php: validate startTime (https://github.com/kaltura/server/pull/6318)
- SUP-12622: Obey new webex limitation LstRecording SQL default time range of 4 weeks (https://github.com/kaltura/server/pull/6315)
- PLAT-8207: fix group_ids indexing on kuser (https://github.com/kaltura/server/pull/6311)
- KMS-14857: add language support to name and description in partial search (https://github.com/kaltura/server/pull/6309)
- PLAT-7961: when using encryption flow do not save the single vid slice after concating (https://github.com/kaltura/server/pull/6307)
- PLAT-8230: user->add action should call toInsertable() for htmlPurify validation (https://github.com/kaltura/server/pull/6306)
- PLAT-8097: Add new logic to matching flavors on playlist (https://github.com/kaltura/server/pull/6305)
- plat 8204: MR - add footer to email notification (https://github.com/kaltura/server/pull/6303)
- Support api rate limiting (https://github.com/kaltura/server/pull/6300)
- SUP-12423: Support passing defaultAudioLang param on the playManifest request to determine which audio flavor will be marked with default & autoSelect = YES + support defining default audio flavor on flavorAsset object (https://github.com/kaltura/server/pull/6297)
- Set the filter *before* getDisableEntitlementForEntry since otherwise the partner criteria will not be added to $c (https://github.com/kaltura/server/pull/6295)
- Move object id filtering validation into filter to support responseProfile flow (https://github.com/kaltura/server/pull/6292)
- PLAT-8205: Add media name in notification email (https://github.com/kaltura/server/pull/6290)
- SUP-12546: Add retry when regisering WV asset (https://github.com/kaltura/server/pull/6289)

* Fri Nov 10 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.7.0-1
- Ver Bounce to 13.7.0

* Mon Nov 6 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.6.0-16
- Update KalturaLiveEntryService.php (https://github.com/kaltura/server/pull/6274)
- Avoid returning empty results when passing DYNAMIC_OBJECT metadata object type (https://github.com/kaltura/server/pull/6273)
- Correctly validate objectId is filtered when calling metadata list (https://github.com/kaltura/server/pull/6269)
- Add query cache rules (https://github.com/kaltura/server/pull/6264)
- PLAT-8134: added KalturaESearchQuery obejct (https://github.com/kaltura/server/pull/6263)
- PLAT-8134: added KalturaESearchObject (https://github.com/kaltura/server/pull/6262)
- SUP-11691: Added ra extension into audio_file_ext[] (https://github.com/kaltura/server/pull/6260)
- PSVAMB-459: New email notification template - current session user (https://github.com/kaltura/server/pull/6259)
- Handle 'skip-chunk-job' cases (https://github.com/kaltura/server/pull/6255)
- Increase allowed max retried chunk jobs to 5 (https://github.com/kaltura/server/pull/6250)
- Call realpath() on secondary sources (WM's) (https://github.com/kaltura/server/pull/6245)
- PlaykitJX: fix last modified date (https://github.com/kaltura/server/pull/6242)
- KMS15714: retreive child entries without entitlements if user is entitled to the parent entry (https://github.com/kaltura/server/pull/6241)
- Remove defKeditorservicesSuccess.php  (https://github.com/kaltura/server/pull/6238)
- PLAT-8133: Changing pubdate date/time format to ISO (https://github.com/kaltura/server/pull/6237)
- playkitjs action validations (https://github.com/kaltura/server/pull/6236)
- embedPlaykitJsAction.class.php: Return correct lastModified value (https://github.com/kaltura/server/pull/6235)
- PLAT-8174: add permission to v3 studio (https://github.com/kaltura/server/pull/6233)
- PLAT-8174: add V3 studio permission and feature flip (https://github.com/kaltura/server/pull/6232)
- ChunkedEncode support for x265 (https://github.com/kaltura/server/pull/6231)
- Raise urgency/priority of copy jobs (https://github.com/kaltura/server/pull/6229)
- PLAT-8150: fix searchCategory + searchUser allowed fields (https://github.com/kaltura/server/pull/6228)
- PLAT-8195: chunked encoding (https://github.com/kaltura/server/pull/6223)
- KMS-15806: allow anonymous user in KalturaQuizUserEntry (https://github.com/kaltura/server/pull/6221)
- PLAT-8122: add partial search on cue point tags (https://github.com/kaltura/server/pull/6218)
- PLAT-8121: add missing cue point question to cue point item result (https://github.com/kaltura/server/pull/6217)
- PLAT-8190: fix partial metadata query (https://github.com/kaltura/server/pull/6216)
- PLAT-8164: change access_control rules column to mediumtext to allow saving ACL's with large amount of rules (https://github.com/kaltura/server/pull/6215)
- PLAT-8142: don't check entitlement when using an ADMIN KS (https://github.com/kaltura/server/pull/6214)
- PLAT-7768: fix privacy context search (https://github.com/kaltura/server/pull/6212)
- Fix conditional-conv-prof crashes (https://github.com/kaltura/server/pull/6211)
- PLAT-8179: move kExtwidgetUtils to lib directory (https://github.com/kaltura/server/pull/6210)
- PLAT-8169: Add support in new languages hkk teo hak hnn (https://github.com/kaltura/server/pull/6209)
- SUP-11802: Properly handle multi deferred events raising a deferred event (https://github.com/kaltura/server/pull/6207)

* Mon Oct 23 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.6.0-1
- Ver Bounce to 13.6.0

* Sun Oct 22 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.5.0-14
- Nightly build.

* Sun Oct 22 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.5.0-13
- KMS-15658: Handle Complex Entry clipping of clip (https://github.com/kaltura/server/pull/6194)
- apiGrep bug fix - case insensitive with match any (https://github.com/kaltura/server/pull/6193)

* Thu Oct 19 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.5.0-9
- KMS-15676: Clone quiz data in baseEntry->clone (https://github.com/kaltura/server/pull/6190)
- KMS-15632: Override source type in cloning (https://github.com/kaltura/server/pull/6188)
- PLAT-8100: Support chunked uploading with autoFinalize flag (https://github.com/kaltura/server/pull/6184)
- PLAT-8138: When serving multi audio entry, audio flavors should be first in the list (https://github.com/kaltura/server/pull/6183)
- PLAT-8129: Don't set sourceType to the original type when clonning (https://github.com/kaltura/server/pull/6180)
- PLAT-8040: Update google API client to 1.1.2 (https://github.com/kaltura/server/pull/6176)
- SUP-12232: Due to Apple bug: add new lines at the end of WebVTT segment to make it at least 10 bytes long (https://github.com/kaltura/server/pull/6175)
- Set plugins in player config object from uiConfig data (https://github.com/kaltura/server/pull/6171)
- PLAT-8132: Fix facebook connector when tags are empty (https://github.com/kaltura/server/pull/6167)
- PLAT-8130: Limit cue point indexing (https://github.com/kaltura/server/pull/6166)
- ChunkedEncoding: Require minimal duration of 3 min (https://github.com/kaltura/server/pull/6164)
- PLAT-8127: Add clone option for caption assets (https://github.com/kaltura/server/pull/6162)
- ChunkedEncoding: Fix aud/vid filters processing (https://github.com/kaltura/server/pull/6160)
- PLAT-8113: Add getVolumeMap action to flavorAsset service (https://github.com/kaltura/server/pull/6156)
- changing enum to core value in drmPlugin (https://github.com/kaltura/server/pull/6155)
- PLAT-8089: facebook 'place' metadata is deprecated and added updateTags() method (https://github.com/kaltura/server/pull/6153)
- PLAT-8100: Support chunked uploading autoFinalize to support file upload without stating which chunk is the last one (https://github.com/kaltura/server/pull/6148)
- PLAT-8084: Dolby audio improvements (https://github.com/kaltura/server/pull/6147)
- Allow single KChunkedEncodeJobScheduler process (https://github.com/kaltura/server/pull/6146)
- PLAT-7886: add optional param of flavorId to getVolumeMap action (https://github.com/kaltura/server/pull/6144)
- x265 frame size should be mod 2 (https://github.com/kaltura/server/pull/6143)
- PLAT-7979: Adding Multi Captions Support connector (https://github.com/kaltura/server/pull/6140)
- PLAT-7961: Adopt YouTube distribution engine (https://github.com/kaltura/server/pull/6138)
- PLAT-8048: Fix distributionProfile and distributionProvider fields on… (https://github.com/kaltura/server/pull/6136)
- Avoid error Response header name 'KalturaBaseEntry-description error' contains invalid characters, aborting request (https://github.com/kaltura/server/pull/6126)

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

