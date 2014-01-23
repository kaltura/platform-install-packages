%define prefix /opt/kaltura
Summary: Kaltura Open Source Video Platform - Analytics 
Name: kaltura-dwh
Version: 9.7.0
Release: 6 
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.bz2
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: kaltura-base,kaltura-pentaho,java-1.7.0-openjdk, kaltura-postinst 
BuildArch: noarch

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


The Kaltura platform enables video management, publishing, syndication and monetization, 
as well as providing a robust framework for managing rich-media applications, 
and developing a variety of online workflows for video. 

This package configures the Data Warehouse [DWH] analytics component. 

%prep
%setup -q

%build

%install
# for Apache access logs.
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/logs
mkdir -p $RPM_BUILD_ROOT%{prefix}/dwh
cp -r %{_builddir}/%{name}-%{version}/* $RPM_BUILD_ROOT%{prefix}/dwh/
cp -r %{_builddir}/%{name}-%{version}/.kettle $RPM_BUILD_ROOT%{prefix}/dwh/

# goes to crontab
#@DWH_DIR@/etlsource/execute/etl_daily.sh -p @DWH_DIR@
#@DWH_DIR@/etlsource/execute/etl_hourly.sh -p @DWH_DIR@
#@DWH_DIR@/etlsource/execute/etl_perform_retention_policy.sh -p @DWH_DIR@
#@DWH_DIR@/etlsource/execute/etl_update_dims.sh -p @DWH_DIR@

%clean
rm -rf %{buildroot}

%pre
# maybe one day we will support SELinux in which case this can be ommitted.
if which getenforce 2>/dev/null; then
	
	if [ `getenforce` = 'Enforcing' ];then
		echo "You have SELinux enabled, please change to permissive mode with:
# setenforce permissive
and then edit /etc/selinux/config to make the change permanent."
		exit 1;
	fi
fi

%post
if [ "$1" = 1 ];then
echo "#####################################################################################################################################
Installation of %{name} %{version} completed
Please run: 
# %{prefix}/bin/%{name}-config.sh [/path/to/answer/file]
To finalize the setup.
#####################################################################################################################################
"
fi

%preun
if [ "$1" = 0 ] ; then
	rm -f %{_sysconfdir}/cron.d/kaltura-dwh
fi

%files
%dir %{prefix}/web/logs
%{prefix}/dwh
#cron/dwh.template
##.kettle/kettle.template.properties


%changelog
* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-6
- Plus .kettle config.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-5
- Install actual %%{prefix}/dwh dir

* Thu Jan 16 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-3
- Added creation of %%{prefix}/web/logs

* Mon Dec 23 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-1
- First package
