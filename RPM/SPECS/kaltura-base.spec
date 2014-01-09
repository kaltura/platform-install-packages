%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define prefix /opt/kaltura
%define confdir %{prefix}/app/configurations
%define logdir %{prefix}/log
%define webdir %{prefix}/web

Summary: Kaltura Open Source Video Platform 
Name: kaltura-base
Version: 9.7.0
Release: 21 
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/server/archive/IX-%{version}.zip 
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: rsync,mail,mysql,kaltura-monit,kaltura-postinst,cronie

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
mkdir -p $RPM_BUILD_ROOT/etc/kaltura.d
for i in admin_console alpha api_v3 batch configurations deployment generator infra plugins start tests ui_infra var_console vendor;do 
	mv  %{_builddir}/%{name}-%{version}/$i $RPM_BUILD_ROOT/%{prefix}/app
done
# now replace tokens
sed 's#@WEB_DIR@#%{prefix}/web#g' $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.template.ini > $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini
sed 's#@IMAGE_MAGICK_BIN_DIR@#%{_bindir}#g' $RPM_BUILD_ROOT/%{prefix}/app/configurations/local.template.ini > $RPM_BUILD_ROOT/%{prefix}/app/configurations/local.ini
sed 's#@WEB_DIR@#%{prefix}/web#g' -i $RPM_BUILD_ROOT/%{prefix}/app/configurations/local.ini
sed 's#@LOG_DIR@#%{prefix}/log#g' -i  $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini  $RPM_BUILD_ROOT/%{prefix}/app/configurations/local.ini
sed 's#@TMP_DIR@#%{prefix}/tmp#g' -i  $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini  $RPM_BUILD_ROOT/%{prefix}/app/configurations/local.ini
sed 's#@APP_DIR@#%{prefix}/app#g' -i  $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini  $RPM_BUILD_ROOT/%{prefix}/app/configurations/local.ini
sed 's#@BASE_DIR@#%{prefix}#g' -i $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini  $RPM_BUILD_ROOT/%{prefix}/app/configurations/local.ini
sed 's#@BIN_DIR@#%{prefix}/bin#g' -i $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini  $RPM_BUILD_ROOT/%{prefix}/app/configurations/local.ini
sed 's#@OS_KALTURA_USER@#%{kaltura_user}#g' -i $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini $RPM_BUILD_ROOT/%{prefix}/app/configurations/local.ini
sed 's#@PHP_BIN@#%{_bindir}/php#g' -i $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini  $RPM_BUILD_ROOT/%{prefix}/app/configurations/local.ini
sed 's#@CURL_BIN_DIR@#%{_bindir}#g' -i $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini  $RPM_BUILD_ROOT/%{prefix}/app/configurations/local.ini

rm $RPM_BUILD_ROOT/%{prefix}/app/generator/sources/android/DemoApplication/libs/libWVphoneAPI.so
rm $RPM_BUILD_ROOT/%{prefix}/app/configurations/.project

%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/kaltura_base.sh << EOF
PATH=$PATH:%{prefix}/bin
export PATH
EOF

%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.conf.so.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.conf.so.d/kaltura_base.conf << EOF
%{prefix}/lib

EOF

%clean
#rm -rf %{buildroot}
%post

# create user/group, and update permissions
groupadd -r %{kaltura_group} 2>/dev/null || true
useradd -M -r -d /opt/kaltura -s /bin/bash -c "Kaltura server" -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true
usermod -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true
chown -R %{kaltura_user}:%{kaltura_group} %{prefix}/log 
chown -R %{kaltura_user}:%{kaltura_group} %{prefix}/app/cache 
ln -sf %{prefix}/app/configurations/system.ini /etc/kaltura.d/system.ini

echo "

#####################################################################################################################################
Installation of %{name} %{version} completed
Please run 
# %{prefix}/bin/%{name}-config.sh [/path/to/answer/file]
To finalize the setup.
#####################################################################################################################################

" 

%preun
if [ "$1" = 0 ] ; then
	rm /etc/kaltura.d/system.ini
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
%config %{_sysconfdir}/ld.conf.so.d/kaltura_base.conf


%dir /etc/kaltura.d
%dir %{prefix}/log
%dir %{prefix}/tmp
%dir %{prefix}/app/cache
%dir %{prefix}/bin
%dir %{prefix}/lib
%dir %{prefix}/include
%dir %{prefix}/share
%dir %{prefix}/web

#token_files[] = @APP_DIR@/configurations/logrotate/kaltura_*.template
#token_files[] = @APP_DIR@/deployment/base/scripts/init_content/*.template.xml
#token_files[] = @APP_DIR@/deployment/base/scripts/init_data/*.template.ini
#token_files[] = @APP_DIR@/plugins/sphinx_search/scripts/configs/server-sphinx.php.template
#token_files[] = dbSchema/db.template.xml


%changelog
* Thu Jan 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-16
- No need for base.ini, there are no tokens there.

* Thu Jan 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-16
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

