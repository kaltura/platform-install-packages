%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define prefix /opt/kaltura/async_api_proxy
%define confdir %{prefix}/config
%define logdir %{prefix}/log

Summary: Kaltura Async Api Proxy 
Name: kaltura-async-api-proxy 
Version: 1.0.0
Release: 2
License: AGPLv3+
Group: Server/Platform 
Source0: async-api-proxy-v%{version}.tar.gz
URL: https://github.com/kaltura/AsyncApiProxy
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: nodejs >= 6.0.0 nodejs-forever nodejs-bundle-config nodejs-os nodejs-simple-rate-limiter nodejs-bundle-continuation-local-storage nodejs-bundle-express nodejs-uuid nodejs-bundle-request nodejs-crypto nodejs-is-subset nodejs-bluebird nodejs-memory-cache nodejs-ipaddr.js 
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

This package provides to Async Api Proxy Server.

%prep
%setup -qn AsyncApiProxy-%{version}

%install
mkdir -p $RPM_BUILD_ROOT%{confdir}
mkdir -p $RPM_BUILD_ROOT%{logdir}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}

sed -e "s#@LOG_DIR@#%{logdir}#g" -e "s#@ASYNC_API_PROXY_PREFIX@#%{prefix}#g"  %{_builddir}/AsyncApiProxy-%{version}/bin/async-proxy-server.template.sh > $RPM_BUILD_ROOT%{_initrddir}/async-proxy-server
chmod +x $RPM_BUILD_ROOT%{_initrddir}/async-proxy-server
rm -rf %{_builddir}/AsyncApiProxy-%{version}/bin 
cp -r %{_builddir}/AsyncApiProxy-%{version}/* $RPM_BUILD_ROOT%{prefix}/
#cd $RPM_BUILD_ROOT%{prefix} 
#npm install
#find $RPM_BUILD_ROOT%{prefix}/node_modules -name package.json -exec rm {} \;



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


%preun

%postun

%files
%{prefix}/*
%{_initrddir}/async-proxy-server
%config %{confdir}/*


%doc %{prefix}/async_proxy_server_deployment.md
%doc %{prefix}/LICENSE
%doc %{prefix}/README.md

%changelog
* Wed Apr 26 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 1.0-1
- First release
