# this sucks but base.ini needs to know the KMC version and it needs to be known cross cluster because, it is needed to generate the UI confs, which is done by the db-config postinst script which can run from every cluster node.
%define kmc_version v5.37.10
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
Version: 9.7.0
Release: 37
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/server/archive/IX-%{version}.zip 
Source1: kaltura.ssl.conf.template 
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: rsync,mail,mysql,kaltura-monit,kaltura-postinst,cronie, php, php-xml, php-curl, php-mysql,php-gd,php-gmp, php-imap, php-ldap

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
%setup -q

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
	mv  %{_builddir}/%{name}-%{version}/$i $RPM_BUILD_ROOT%{prefix}/app
done
mkdir -p $RPM_BUILD_ROOT%{prefix}/app/configurations/monit.d
mv $RPM_BUILD_ROOT/%{prefix}/app/configurations/monit/monit.d $RPM_BUILD_ROOT/%{prefix}/app/configurations/monit.avail
# change name from .*.template.rc to .*.rc.template so that monit.d/*.rc will work correctly.

# now replace tokens
#sed 's#@IMAGE_MAGICK_BIN_DIR@#%{_bindir}#g' $RPM_BUILD_ROOT%{prefix}/app/configurations/local.template.ini > $RPM_BUILD_ROOT/%{prefix}/app/configurations/local.ini
#sed -i 's#@CURL_BIN_DIR@#%{_bindir}#g' $RPM_BUILD_ROOT%{prefix}/app/configurations/local.ini

sed -i "s@\(^kmc_version\)\s*=.*@\1=%{kmc_version}@g" $RPM_BUILD_ROOT%{prefix}/app/configurations/base.ini
rm $RPM_BUILD_ROOT%{prefix}/app/generator/sources/android/DemoApplication/libs/libWVphoneAPI.so
rm $RPM_BUILD_ROOT%{prefix}/app/configurations/.project
# we bring our own for kaltura-front and kaltura-batch.
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/app/configurations/apache/kaltura.ssl.conf.template
# we bring another in kaltura-batch
rm $RPM_BUILD_ROOT%{prefix}/app/configurations/batch/batch.ini.template

%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/kaltura_base.sh << EOF
PATH=\$PATH:%{prefix}/bin
export PATH
EOF

%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/kaltura_base.conf << EOF
%{prefix}/lib

EOF

%clean
rm -rf %{buildroot}

%pre

# maybe one day we will support SELinux in which case this can be ommitted.
if which selinuxenabled 2>/dev/null; then
	selinuxenabled
	if [ $? -eq 0 ];then
		echo "You have SELinux enabled, please change to permissive mode with:
# setenforce permissive
and then edit /etc/selinux/config to make the change permanent."
		exit 1;
	fi
fi
%post

# create user/group, and update permissions
groupadd -r %{kaltura_group} 2>/dev/null || true
useradd -M -r -d /opt/kaltura -s /bin/bash -c "Kaltura server" -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true
usermod -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true
#chown -R %{kaltura_user}:%{kaltura_group} %{prefix}/log 
#chown -R %{kaltura_user}:%{kaltura_group} %{prefix}/tmp 
#chown -R %{kaltura_user}:%{kaltura_group} %{prefix}/app/cache 
ln -sf %{prefix}/app/configurations/system.ini /etc/kaltura.d/system.ini
ln -sf %{prefix}/app/api_v3/web %{prefix}/app/alpha/web/api_v3



%preun
if [ "$1" = 0 ] ; then
	rm -f %{_sysconfdir}/kaltura.d/system.ini
	rm -f %{prefix}/app/alpha/web/api_v3
	rm -f %{_sysconfdir}/logrotate.d/kaltura_base
	# get rid of stray symlinks.
	find %{_sysconfdir}/httpd/conf.d/ -type l -name "*kaltura*" -exec rm {} \;
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
%{prefix}/web/content
%{prefix}/web/tmp
%dir %{prefix}/web/control
%{prefix}/web/dropfolders
%defattr(-, root,root, 0755)
%dir %{prefix}/app/configurations/monit.d
%dir %{prefix}/bin
%dir %{prefix}/lib
%dir %{prefix}/include
%dir %{prefix}/share


%changelog
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

