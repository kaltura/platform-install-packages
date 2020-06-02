%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define kaltura_prefix /opt/kaltura
%define archive_dir_name playkit-js-bundle-builder
%define prefix %{kaltura_prefix}/%{archive_dir_name}
%define confdir %{prefix}/config
%define logdir %{prefix}/log
%define piddir %{prefix}/var/run

Summary: Kaltura PlayKit Bundler 
Name: kaltura-playkit-bundler 
Version: 1.2.0
Release: 2
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-v%{version}.tar.gz
Source1: kaltura-playkit-bundler
URL: https://github.com/kaltura/%{archive_dir_name}
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: nodejs >= 10.0.0, kaltura-base
Requires(post): chkconfig
AutoReq: no 

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

This package provides the PlayKit bundler.

%prep
%setup -qn %{archive_dir_name}-%{version}

%install
mkdir -p $RPM_BUILD_ROOT%{confdir}
mkdir -p $RPM_BUILD_ROOT%{logdir}
mkdir -p $RPM_BUILD_ROOT%{piddir}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}

sed -e "s#@BUNDLE_BUILDER_PREFIX@#%{prefix}#g" %{SOURCE1} > $RPM_BUILD_ROOT%{_initrddir}/%{name}
sed -e "s#@LOG_DIR@#%{logdir}#g" -e "s#@HTTP_PORT@#8880#g" -e "s#@HTTPS_PORT@#8889#g" %{_builddir}/%{archive_dir_name}-%{version}/config/default.template.json > %{_builddir}/%{archive_dir_name}-%{version}/config/default.json
chmod +x $RPM_BUILD_ROOT%{_initrddir}/%{name}
cp -r %{_builddir}/%{archive_dir_name}-%{version}/* $RPM_BUILD_ROOT%{prefix}/


%clean
#rm -rf %{buildroot}

%pre
# we really only want this when upgrading but since we have to use '|| true' anyhow, it doesn't matter
service %{name} stop || true
# maybe one day we will support SELinux in which case this can be ommitted.
if which getenforce >> /dev/null 2>&1; then
	
	if [ `getenforce` = 'Enforcing' ];then
		echo "You have SELinux enabled, please change to permissive mode with:
# setenforce permissive
and then edit /etc/selinux/config to make the change permanent."
		exit 1;
	fi
fi


%post
cd %{prefix} && npm install yarn -g && yarn install -g forever gulp@3.9.1
/sbin/chkconfig --add %{name}
if [ -r %{kaltura_prefix}/app/configurations/local.ini ];then
	SALT=`grep remote_addr_header_salt %{kaltura_prefix}/app/configurations/local.ini|sed 's@^remote_addr_header_salt\s*=\s*\(.*\)$@\1@g'| sed 's@"@@g'`
	sed -i "s#@APP_REMOTE_ADDR_HEADER_SALT@#$SALT#g" %{confdir}/default.json
	service %{name} restart
fi

%preun
/sbin/service %{name} stop > /dev/null 2>&1
/sbin/chkconfig --del %{name}

%postun

%files
%{prefix}/*
%{_initrddir}/%{name}
%config %{confdir}/*
%defattr(-, %{kaltura_user}, %{kaltura_group} , 0755)
%dir %{logdir}
%dir %{piddir}


%doc %{prefix}/bundle_builder_server_deployment.md
%doc %{prefix}/LICENSE
%doc %{prefix}/README.md

%changelog
* Tue Jun 2 2020 jess.portnoy@kaltura.com <Jess Portnoy> - v1.2.0-2
- Deploying using `yarn` rather than `npm`

* Mon Mar 16 2020 jess.portnoy@kaltura.com <Jess Portnoy> - v1.2.0-1
- feat(FEC-9465): Internationalization (i18n) - player localization (#8)
- fix(FEC-9458): bundle builder doesn't order dependencies correctly (#8)

* Wed Mar 6 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v1.1.1-10
- Override the vanila init script with one that is able to run this as a none privileged user ['kaltura']

* Mon Feb 11 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v1.1.1
- First release
