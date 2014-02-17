# this sucks but base.ini needs to know the KMC version and it needs to be known cross cluster because, it is needed to generate the UI confs, which is done by the db-config postinst script which can run from every cluster node.
%define kmc_version v5.37.10
%define clipapp_version v1.0.7
%define html5_version v2.1.1
%define kdp3_wrapper_version v37.0
%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define apache_user	apache
%define apache_group	apache
%define prefix /opt/kaltura
%define confdir %{prefix}/app/configurations
%define logdir %{prefix}/log
%define webdir %{prefix}/web

Summary: Kaltura Open Source Video Platform 
Name: kaltura-base
Version: 9.9.0
Release: 48
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/server/archive/IX-%{version}.zip 
Source1: kaltura.apache.ssl.conf.template 
# 22/01/14 due to a bug, can be removed in the next version:
Source2: 01.conversionProfile.99.template.xml
Source3: kaltura.apache.conf.template 
Source4: emails_en.template.ini
Source5: 01.Partner.template.ini
Source6: 02.Permission.ini
Source7: dwh.template
Source8: 01.uiConf.99.template.xml
Source9: plugins.template.ini
Source10: entry_and_uiconf_templates.tar.gz
# fixes https://github.com/kaltura/platform-install-packages/issues/37
Source11: clear_cache.sh
# monit templates
Source12: mysqld.template.rc
Source13: sphinx.template.rc 
Source14: httpd.template.rc 
Source15: batch.template.rc 
Source16: memcached.template.rc
Source17: navigation.xml 
Source18: monit.phtml 
Source19: IndexController.php
Source20: sphinx.populate.template.rc

#Source10: 01.UserRole.99.template.xml
#Source9: 01.conversionProfile.99.template.xml
URL: https://github.com/kaltura/server/tree/IX-%{version}
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: rsync,mail,mysql,kaltura-monit,kaltura-postinst,cronie, php-cli, php-xml, php-curl, php-mysql,php-gd,php-gmp, php-imap, php-ldap,ntp,mailx

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
%setup -qn server-IX-%{version}


%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/app
mkdir -p $RPM_BUILD_ROOT%{prefix}/log
mkdir -p $RPM_BUILD_ROOT%{prefix}/tmp
mkdir -p $RPM_BUILD_ROOT%{prefix}/web
mkdir -p $RPM_BUILD_ROOT%{prefix}/app/cache
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
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content/webcam 
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

for i in admin_console alpha api_v3 batch configurations deployment generator infra plugins start tests ui_infra var_console vendor;do 
	mv  %{_builddir}/server-IX-%{version}/$i $RPM_BUILD_ROOT%{prefix}/app
done
find  $RPM_BUILD_ROOT%{prefix}/app -name "*.sh" -type f -exec chmod +x {} \;


sed -i "s@\(^kmc_version\)\s*=.*@\1=%{kmc_version}@g" $RPM_BUILD_ROOT%{prefix}/app/configurations/base.ini
sed -i "s@\(^clipapp_version\)\s*=.*@\1=%{clipapp_version}@g" $RPM_BUILD_ROOT%{prefix}/app/configurations/base.ini
sed -i "s@\(^html5_version\)\s*=.*@\1=%{html5_version}@g" $RPM_BUILD_ROOT%{prefix}/app/configurations/base.ini
sed -i "s@\(^kdp3_wrapper_version\)\s*=.*@\1=%{kdp3_wrapper_version}@g" $RPM_BUILD_ROOT%{prefix}/app/configurations/base.ini
# our Pentaho is correctly installed under its own dir and not %prefix/bin which is the known default so, adding -k path to kitchen.sh
sed -i 's#\(@DWH_DIR@\)$#\1 -k /opt/kaltura/pentaho/pdi/kitchen.sh#g' $RPM_BUILD_ROOT%{prefix}/app/configurations/cron/dwh.template
rm $RPM_BUILD_ROOT%{prefix}/app/generator/sources/android/DemoApplication/libs/libWVphoneAPI.so
rm $RPM_BUILD_ROOT%{prefix}/app/configurations/.project
# we bring our own for kaltura-front and kaltura-batch.
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/app/configurations/apache/kaltura.ssl.conf.template
cp %{SOURCE3} $RPM_BUILD_ROOT%{prefix}/app/configurations/apache/kaltura.conf.template
cp %{SOURCE4} $RPM_BUILD_ROOT%{prefix}/app/batch/batches/Mailer/emails_en.template.ini
# Add partnerParentId=0 to Mr. partner 99.
cp %{SOURCE5} $RPM_BUILD_ROOT%{prefix}/app/deployment/base/scripts/init_data/01.Partner.template.ini
cp %{SOURCE6} $RPM_BUILD_ROOT%{prefix}/app/deployment/base/scripts/init_data/02.Permission.ini
cp %{SOURCE8} $RPM_BUILD_ROOT%{prefix}/app/deployment/base/scripts/init_content/01.uiConf.99.template.xml
cp %{SOURCE7} $RPM_BUILD_ROOT%{prefix}/app/configurations/cron/dwh.template
cp %{SOURCE9} $RPM_BUILD_ROOT%{prefix}/app/configurations/plugins.template.ini
#cp %{SOURCE10} $RPM_BUILD_ROOT%{prefix}/app/deployment/base/scripts/init_content/01.UserRole.99.template.xml
cp %{SOURCE11} $RPM_BUILD_ROOT%{prefix}/app/alpha/crond/kaltura/clear_cache.sh
mkdir -p $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail
cp %{SOURCE12} $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/
cp %{SOURCE13} $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/
cp %{SOURCE20} $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/
cp %{SOURCE14} $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/
cp %{SOURCE15} $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/
cp %{SOURCE16} $RPM_BUILD_ROOT%{prefix}/app/configurations/monit/monit.avail/

# David Bezemer's Admin console and monit patches:
cp %{SOURCE17} $RPM_BUILD_ROOT%{prefix}/app/admin_console/configs/navigation.xml
cp %{SOURCE18} $RPM_BUILD_ROOT%{prefix}/app/admin_console/views/scripts/index/monit.phtml
cp %{SOURCE19} $RPM_BUILD_ROOT%{prefix}/app/admin_console/controllers/IndexController.php

# we bring another in kaltura-batch
rm $RPM_BUILD_ROOT%{prefix}/app/configurations/batch/batch.ini.template

# 22/01/14 due to a bug, can be removed in the next version:
cp %{SOURCE2} $RPM_BUILD_ROOT%{prefix}/app/deployment/base/scripts/init_content/01.conversionProfile.99.template.xml

mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content
tar zxf %{SOURCE10} -C $RPM_BUILD_ROOT%{prefix}/web/content

%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/kaltura_base.sh << EOF
PATH=\$PATH:%{prefix}/bin
export PATH
alias allkaltlog='grep --color "ERR:\|PHP\|trace\|CRIT\|\[error\]" /opt/kaltura/log/*.log /opt/kaltura/log/batch/*.log'
alias kaltlog='tail -f /opt/kaltura/log/*.log /opt/kaltura/log/batch/*.log | grep -A 1 -B 1 --color "ERR:\|PHP\|trace\|CRIT\|\[error\]"'
EOF

%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/kaltura_base.conf << EOF
%{prefix}/lib

EOF

%clean
rm -rf %{buildroot}

%pre

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
groupadd -r %{kaltura_group} -g7373 2>/dev/null || true
useradd -M -r -u7373 -d /opt/kaltura -s /bin/bash -c "Kaltura server" -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true
getent group apache >/dev/null || groupadd -g 48 -r apache
getent passwd apache >/dev/null || \
  useradd -r -u 48 -g apache -s /sbin/nologin \
    -d /var/www -c "Apache" apache
usermod -a -G %{kaltura_group} %{apache_user}

usermod -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true


%post

ln -sf %{prefix}/app/configurations/system.ini /etc/kaltura.d/system.ini
ln -sf %{prefix}/app/api_v3/web %{prefix}/app/alpha/web/api_v3
chown apache.kaltura -R /opt/kaltura/web/content/entry /opt/kaltura/web/content/uploads/ /opt/kaltura/web/content/webcam/ /opt/kaltura/web/tmp/
find /opt/kaltura/web/content/entry /opt/kaltura/web/content/uploads/ /opt/kaltura/web/content/webcam/ /opt/kaltura/web/tmp/ -type d -exec chmod 775 {} \;
/etc/init.d/ntpd start
if [ "$1" = 2 ];then
	if [ -r "%{prefix}/app/configurations/local.ini" -a -r "%{prefix}/app/configurations/base.ini" ];then
		echo "Regenarating client libs.. this will take up to 2 minutes to complete."
		rm -rf %{prefix}/app/cache/*
		php %{prefix}/app/generator/generate.php
		find %{prefix}/app/cache/ %{prefix}/log -type d -exec chmod 775 {} \;
		find %{prefix}/app/cache/ %{prefix}/log -type f -exec chmod 664 {} \;
		chown -R %{kaltura_user}.%{apache_user} %{prefix}/app/cache/ %{prefix}/log
		chmod 775 %{prefix}/web/content

		if [ -x %{_sysconfdir}/init.d/httpd ];then
			%{_sysconfdir}/init.d/httpd restart
		fi
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

%config %{prefix}/app/configurations/*
%config %{_sysconfdir}/profile.d/kaltura_base.sh
%config %{_sysconfdir}/ld.so.conf.d/kaltura_base.conf


%dir /etc/kaltura.d
%defattr(-, %{kaltura_user}, %{apache_group} , 0775)
%dir %{prefix}/log
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


%changelog
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

