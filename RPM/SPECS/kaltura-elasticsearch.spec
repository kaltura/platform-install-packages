%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define es_user	elasticsearch
%define es_group elasticsearch
%define prefix /opt/kaltura
%define confdir %{prefix}/app/configurations/elastic
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
Source2: elasticsearch.template.yml
Source3: aliases.json

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires(pre): kaltura-base, kaltura-postinst, elasticsearch >= 6.0.0, java-1.8.0-openjdk-headless
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
mkdir -p $RPM_BUILD_ROOT/%{logdir} $RPM_BUILD_ROOT/%{vardir} $RPM_BUILD_ROOT/%{tmpdir} $RPM_BUILD_ROOT/%{confdir}/populate $RPM_BUILD_ROOT%{_sysconfdir}/elasticsearch/analysis $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig $RPM_BUILD_ROOT/%{confdir}/aliases $RPM_BUILD_ROOT%{_sysconfdir}/init.d

#echo "ES_JAVA_OPTS=\"-Djna.tmpdir=$BASE_DIR/var/lib/elasticsearch/tmp -Djava.io.tmpdir=$BASE_DIR/var/lib/elasticsearch/tmp\"" >> $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/elasticsearch 

chmod +x %{SOURCE0}
cp %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/init.d 
cp %{SOURCE1} $RPM_BUILD_ROOT/%{confdir}/
cp %{SOURCE2} $RPM_BUILD_ROOT/%{confdir}/elasticsearch.template.yml
cp %{SOURCE3} $RPM_BUILD_ROOT/%{confdir}/aliases/aliases.json

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
/sbin/service kaltura-elastic-populate stop > /dev/null 2>&1
/sbin/chkconfig --del kaltura-elastic-populate

%postun

%files
%defattr(-, %{es_user}, %{es_group} , 0775)
%dir %{logdir} 
%dir %{vardir}
%dir %{tmpdir}
%dir %{_sysconfdir}/elasticsearch 
%dir %{_sysconfdir}/elasticsearch/analysis 
%defattr(-, %{kaltura_user}, %{es_group} , 0775)
%dir %{confdir}
%config %{confdir}/*
%{_sysconfdir}/init.d/kaltura-elastic-populate

%changelog
* Fri Feb 15 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 1.0.0-1
- First release
