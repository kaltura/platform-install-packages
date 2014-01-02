%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define prefix /opt/kaltura
%define confdir %{prefix}/app/configurations
%define logdir %{prefix}/log
%define webdir %{prefix}/web

Summary: Kaltura Open Source Video Platform 
Name: kaltura-base
Version: 9.7.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/server/archive/IX-%{version}.zip 
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
# monit
Requires: rsync,mail,mysql,cronie

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
mkdir -p $RPM_BUILD_ROOT%{prefix}/log
mkdir -p $RPM_BUILD_ROOT%{prefix}/app
mkdir -p $RPM_BUILD_ROOT%{prefix}/cache
mkdir -p $RPM_BUILD_ROOT/etc/kaltura.d
for i in admin_console alpha api_v3 batch configurations deployment generator infra plugins start tests ui_infra var_console vendor;do 
	mv  %{_builddir}/%{name}-%{version}/$i $RPM_BUILD_ROOT/%{prefix}/app
done
# now replace tokens
sed 's#WEB_DIR=@WEB_DIR@#WEB_DIR=%{prefix}/web#' $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.template.ini > $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini
sed 's#LOG_DIR=@LOG_DIR@#LOG_DIR=%{prefix}/log#' $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.template.ini > $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini
sed 's#APP_DIR=@LOG_DIR@#APP_DIR=%{prefix}/app#' $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.template.ini > $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini
sed 's#BASE_DIR=@BASE_DIR@#BASE_DIR=%{prefix}#' $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.template.ini > $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini
sed 's#OS_KALTURA_USER=@OS_KALTURA_USER@#OS_KALTURA_USER=%{kaltura_user}#' $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.template.ini > $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini
sed 's#PHP_BIN=@PHP_BIN@#PHP_BIN=%{_bindir}/php#' $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.template.ini > $RPM_BUILD_ROOT/%{prefix}/app/configurations/system.ini
rm $RPM_BUILD_ROOT/%{prefix}/app/generator/sources/android/DemoApplication/libs/libWVphoneAPI.so

%clean
rm -rf %{buildroot}

%post

# create user/group, and update permissions
groupadd -r %{sphinx_group} 2>/dev/null || true
useradd -M -r -d /opt/kaltura -s /bin/bash -c "Kaltura server" -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true
usermod -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true
chown -R %{kaltura_user}:%{sphinx_group} %{prefix}-%{version}/log %{prefix}-%{version}/cache 
ln -sf %{prefix}/app/configurations/system.ini /etc/kaltura.d/system.ini

%preun

%postun
rm /etc/kaltura.d/system.ini

%files
%dir %{prefix}/app
%config %{prefix}/app/configurations/base.ini
%config %{prefix}/app/configurations/local.template.ini
%config %{prefix}/app/configurations/cron/api.template
%config %{prefix}/app/configurations/system.ini
%config %{prefix}/app/configurations/system.template.ini
%dir /etc/kaltura.d

#token_files[] = @APP_DIR@/configurations/logrotate/kaltura_*.template
#token_files[] = @APP_DIR@/deployment/base/scripts/init_content/*.template.xml
#token_files[] = @APP_DIR@/deployment/base/scripts/init_data/*.template.ini
#token_files[] = @APP_DIR@/plugins/sphinx_search/scripts/configs/server-sphinx.php.template
#token_files[] = dbSchema/db.template.xml

%dir %{prefix}/log
%dir %{prefix}/cache

%changelog
* Mon Dec  23 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 8.0-1
- First package
