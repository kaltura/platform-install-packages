%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define prefix /opt/kaltura/push-server
%define confdir %{prefix}/config
%define logdir %{prefix}/log

Summary: Kaltura Push Server 
Name: kaltura-push-server 
Version: 1.0.8
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-v%{version}.tar.gz
URL: https://github.com/kaltura/pub-sub-server
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: nodejs >= 6.0.0 nodejs-forever nodejs-os nodejs-continuation-local-storage nodejs-crypto nodejs-amqp nodejs-util nodejs-node-ini nodejs-socket.io nodejs-cron nodejs-uws 
Requires(post): chkconfig
BuildRequires: nodejs-packaging
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

This package provides the Push Server.

%prep
%setup -qn pub-sub-server-%{version}

%install
mkdir -p $RPM_BUILD_ROOT%{confdir}
mkdir -p $RPM_BUILD_ROOT%{logdir}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}

sed -e "s#@LOG_DIR@#%{logdir}#g" -e "s#@PUB_SUB_PREFIX@#%{prefix}#g" -e 's#@NODE_MODULES_PATH@#/usr/lib/node_modules#g'  %{_builddir}/pub-sub-server-%{version}/bin/push-server.template.sh > $RPM_BUILD_ROOT%{_initrddir}/kaltura-push-server
chmod +x $RPM_BUILD_ROOT%{_initrddir}/kaltura-push-server
cp -r %{_builddir}/pub-sub-server-%{version}/* $RPM_BUILD_ROOT%{prefix}/
rm $RPM_BUILD_ROOT%{prefix}/bin/push-server.template.sh $RPM_BUILD_ROOT%{prefix}/bin/upgrade-push-server.sh
chmod +x $RPM_BUILD_ROOT%{prefix}/bin/configure-rabbitmq.sh



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


%post
/sbin/chkconfig --add kaltura-push-server

%preun
/sbin/service kaltura-push-server stop > /dev/null 2>&1
/sbin/chkconfig --del kaltura-push-server

%postun

%files
%{prefix}/*
%{_initrddir}/kaltura-push-server
%config %{confdir}/*


%doc %{prefix}/pub_sub_server_deployment.md
%doc %{prefix}/LICENSE
%doc %{prefix}/README.md

%changelog
* Tue Aug  23 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 1.0.8-1
- Add binding command to bind between the kaltura exchange and the queue

* Tue May  23 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 1.0.2-1
- First release
