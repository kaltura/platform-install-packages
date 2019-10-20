%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define prefix /opt/kava
%define confdir %{prefix}/conf
%define logdir %{prefix}/log
%define webdir /opt/kaltura/web 
%define repo_name kava-public

Summary: Kaltura Open Source Video Platform 
Name: kaltura-kava
Version: 1.0.1
Release: 3
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.gz


URL: https://github.com/kaltura/%{repo_name}/tree/%{version}
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: php70-php-pecl-memcached, php70-php-pecl-mysql, php70-php-pecl-rdkafka, php70-php-pecl-ip2location, memcached 

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

This is the base KAVA package, needed for analytics.

%prep
%setup -qn %{repo_name}-%{version}


%install
mkdir -p $RPM_BUILD_ROOT%{prefix}
for i in enrichment lib conf ingestion vendor ;do 
	mv  %{_builddir}/%{repo_name}-%{version}/$i $RPM_BUILD_ROOT%{prefix}/
done

mkdir -p $RPM_BUILD_ROOT%{logdir}
mkdir -p $RPM_BUILD_ROOT%{webdir}/kava/playsViews
mkdir -p $RPM_BUILD_ROOT%{webdir}/kava/bandwidth/migration
mkdir -p $RPM_BUILD_ROOT%{webdir}/kava/transcoding/migration
mkdir -p $RPM_BUILD_ROOT%{webdir}/kava/batch
mkdir -p $RPM_BUILD_ROOT%{webdir}/kava/entryLifecycle
mkdir -p $RPM_BUILD_ROOT%{webdir}/kava/userLifecycle/logs
mkdir -p $RPM_BUILD_ROOT%{webdir}/kava/transcoding
mkdir -p $RPM_BUILD_ROOT%{webdir}/kava/transcoding/logs
mkdir -p $RPM_BUILD_ROOT%{webdir}/logs
mkdir -p $RPM_BUILD_ROOT%{webdir}/kava/bandwidth/enriched
mkdir -p $RPM_BUILD_ROOT%{webdir}/kava/reach
mkdir -p $RPM_BUILD_ROOT%{prefix}/ingestion/var/tmp
mkdir -p $RPM_BUILD_ROOT%{prefix}/var/tmp
mkdir -p $RPM_BUILD_ROOT/opt/kaltura/log/kava

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
getent group %{kaltura_group} >/dev/null || groupadd -r %{kaltura_group} -g7373 2>/dev/null
getent passwd %{kaltura_user} >/dev/null || useradd -m -r -u7373 -d %{prefix} -s /bin/bash -c "Kaltura server" -g %{kaltura_group} %{kaltura_user} 2>/dev/null



%post




%preun
if [ "$1" = 0 ] ; then
	echo "remove"
fi

%postun

%files
%{prefix}
%{webdir}

%config %{confdir}/*


%defattr(-, %{kaltura_user}, %{kaltura_group} , 0775)
%dir %{logdir}
%dir %{webdir}
%dir %{prefix}/ingestion/var/tmp
%dir /opt/kaltura/log/kava


%changelog
* Sun Oct 20 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 1.0.1-1
- First release
