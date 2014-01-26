%define prefix /opt/kaltura
Summary: Kaltura Open Source Video Platform - Analytics 
Name: kaltura-dwh
Version: 9.7.0 
Release: 8 
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/dwh/archive/%{name}-master.zip
URL: https://github.com/kaltura/dwh/tree/master 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: kaltura-base,kaltura-pentaho,jre, kaltura-postinst 
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
%setup -qn dwh-master

%build

%install
# for Apache access logs.
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/logs
mkdir -p $RPM_BUILD_ROOT%{prefix}/dwh
cp -r %{_builddir}/dwh-master/* $RPM_BUILD_ROOT%{prefix}/dwh/
cp -r %{_builddir}/dwh-master/.kettle $RPM_BUILD_ROOT%{prefix}/dwh/

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
if [ "$1" = 1 ];then
echo "#####################################################################################################################################
Installation of %{name} %{version} completed
Please run: 
# %{prefix}/bin/%{name}-config.sh [/path/to/answer/file]
To finalize the setup.
#####################################################################################################################################
"
fi
# Alas, we only work well with Sun's Java so, first lets find the latest version we have for it [this package is included in Kaltura's repo, as taken from Oracle's site
LATEST_JAVA=`ls -d /usr/java/jre*|tail -1`
alternatives --install /usr/bin/java java $LATEST_JAVA/bin/java  20000

%preun
if [ "$1" = 0 ] ; then
	rm -f %{_sysconfdir}/cron.d/kaltura-dwh
fi

%files
%dir %{prefix}/web/logs
%{prefix}/dwh


%changelog
* Sun Jan 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-8
- Sources moved to GIT.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-6
- Plus .kettle config.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-5
- Install actual %%{prefix}/dwh dir

* Thu Jan 16 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-3
- Added creation of %%{prefix}/web/logs

* Mon Dec 23 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-1
- First package
