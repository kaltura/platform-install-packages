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
for i in admin_console alpha api_v3 batch configurations deployment generator infra plugins start tests ui_infra var_console vendor;do 
	mv  %{_builddir}/%{name}-%{version}/$i $RPM_BUILD_ROOT/%{prefix}/app
done

%clean
rm -rf %{buildroot}

%post

# create user/group, and update permissions
groupadd -r %{sphinx_group} 2>/dev/null || true
useradd -M -r -d /opt/kaltura -s /bin/bash -c "Kaltura server" -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true
usermod -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true
chown -R %{kaltura_user}:%{sphinx_group} %{prefix}-%{version}/log %{prefix}-%{version}/cache 
# now replace tokens

%preun

%files
%{prefix}/app
%config %{prefix}/app/configurations/base.ini
%config %{prefix}/app/configurations/local.template.ini
%config %{prefix}/app/configurations/cron/api.template

#token_files[] = @APP_DIR@/configurations/logrotate/kaltura_*.template
#token_files[] = @APP_DIR@/deployment/base/scripts/init_content/*.template.xml
#token_files[] = @APP_DIR@/deployment/base/scripts/init_data/*.template.ini
#token_files[] = @APP_DIR@/plugins/sphinx_search/scripts/configs/server-sphinx.php.template
#token_files[] = @APP_DIR@/tests/monitoring/config.template.ini
#token_files[] = @APP_DIR@/tests/sanity/lib/*.template.ini
#token_files[] = @DWH_DIR@/.kettle/kettle.template.properties
#token_files[] = dbSchema/db.template.xml

%dir %{prefix}/log
%dir %{prefix}/cache

%changelog
* Mon Dec  23 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 8.0-1
- First package
