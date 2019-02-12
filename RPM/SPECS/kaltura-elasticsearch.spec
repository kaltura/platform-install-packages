%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define es_user	elasticsearch
%define es_group elasticsearch
%define prefix /opt/kaltura
%define confdir %{prefix}/app/configurations/elasticsearch
%define populate_confdir %{prefix}/app/configurations/elastic/populate
%define logdir %{prefix}/log/elasticsearch
%define vardir %{prefix}/var/lib/elasticsearch
%define tmpdir %{vardir}/tmp

Summary: Kaltura Open Source Video Platform 
Name: kaltura-elasticsearch
Version: 1.0.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: kaltura-elastic-populate 
Source1: kaltura_synonyms_contraction.txt
Source2: elasticsearch.yml

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires(pre): kaltura-base, elasticsearch >= 6.0.0
%if 0%{?rhel}  == 6
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
%endif

%if 0%{?rhel}  == 7
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
Epoch: 1
%endif

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

This package configures everything needed for the Kaltura's Elasticsearch service.

%prep

%install
mkdir -p $RPM_BUILD_ROOT/%{logdir} $RPM_BUILD_ROOT/%{vardir} $RPM_BUILD_ROOT/%{tmpdir} $RPM_BUILD_ROOT/%{confdir}/elastic/populate $RPM_BUILD_ROOT%{_sysconfdir}/elasticsearch/analysis 

echo "ES_JAVA_OPTS=\"-Djna.tmpdir=$BASE_DIR/var/lib/elasticsearch/tmp -Djava.io.tmpdir=$BASE_DIR/var/lib/elasticsearch/tmp\"" >> $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/elasticsearch


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
service elasticsearch restart

if [ ! -d /usr/share/elasticsearch/plugins/analysis-icu ];then
        /usr/share/elasticsearch/bin/elasticsearch-plugin  install analysis-icu
fi

%preun

%postun

%files
%defattr(-, %{es_user}, %{es_group} , 0775)
%dir %{logdir} 
%dir %{vardir}
%dir %{tmpdir}
%dir %{confdir}/elastic/populate 
%dir %{_sysconfdir}/elasticsearch/analysis 

%changelog
* Mon Dec 10 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 1.0.0-1
- First release
