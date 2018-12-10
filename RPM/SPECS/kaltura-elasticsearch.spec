%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define es_user	elasticsearch
%define es_group elasticsearch
%define prefix /opt/kaltura
%define confdir %{prefix}/app/configurations/elasticsearch
%define logdir %{prefix}/log/elasticsearch
%define vardir %{prefix}/var/lib/elasticsearch
%define tmpdir %{vardir}/tmp
%define codename Naos

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
Requires: kaltura-base, elasticsearch >= 6.0.0
%if 0%{?rhel}  == 6
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl >= 1.0.1
BuildRequires: openssl-devel >= 1.0.1
%endif

%if 0%{?rhel}  == 7
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: systemd
Requires: openssl >= 1.0.1
BuildRequires: systemd
BuildRequires: openssl-devel >= 1.0.1
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
mkdir -p $RPM_BUILD_ROOT/%{logdir} $RPM_BUILD_ROOT/%{vardir} $RPM_BUILD_ROOT/%{tmpdir} $RPM_BUILD_ROOT/%{confdir}/elastic/populate



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

getent group %{apache_user} >/dev/null || groupadd -g 48 -r %{apache_group}
getent passwd %{apache_user} >/dev/null || \
  useradd -r -u 48 -g %{apache_group} -s /sbin/nologin \
    -d /var/www -c "Apache" %{apache_user}
usermod -a -G %{kaltura_group} %{apache_user}

usermod -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true
if [ ! -d /usr/share/elasticsearch/plugins/analysis-icu ];then
        /usr/share/elasticsearch/bin/elasticsearch-plugin  install analysis-icu
fi

%post



%preun

%postun

%files

%changelog
* Mon Dec 10 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 1.0.0-1
- First release
