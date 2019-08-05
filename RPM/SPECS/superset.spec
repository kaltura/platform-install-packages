%global __os_install_post %{nil}

Name:           superset
Version:        0.28.1
Release:        1%{?dist}
Summary:        Superset
Group:			System Environment/Daemons       
License:        ASL 2.0
URL:            https://superset.apache.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	python-devel
BuildRequires:  libffi-devel 
BuildRequires:  cyrus-sasl-devel
BuildRequires:	gcc-c++
BuildRequires:	python3-pip
AutoReqProv: 	no
Requires:       python36

%description
Apache Superset is a modern, enterprise-ready business intelligence web application

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}/usr/share/superset/bin/
%{__mkdir} -p %{buildroot}/usr/share/superset/log/
%{__mkdir} -p %{buildroot}/etc/sysconfig/
%{__mkdir} -p %{buildroot}/usr/lib/systemd/system/
%{__mkdir} -p %{buildroot}/run/superset/
%{__mkdir} -p %{buildroot}/usr/bin/
%{__mkdir} -p %{buildroot}/etc/logrotate.d/

pip3 install --target %{buildroot}/usr/share/superset/lib gunicorn sqlalchemy-clickhouse kylinpy sqlalchemy-redshift sqlalchemy-greenplum superset

%{__cp} -rp %{_topdir}/bin/superset %{buildroot}/etc/sysconfig/
%{__cp} -rp %{_topdir}/superset.service %{buildroot}/usr/lib/systemd/system/
chmod 644 %{buildroot}/usr/lib/systemd/system/*

%{__cp} -rp %{_topdir}/bin/superset %{buildroot}/usr/share/superset/bin/
%{__cp} -rp %{_topdir}/bin/superset %{buildroot}/usr/bin/superset

%{__cp} -rp %{_topdir}/logrotate/* %{buildroot}/etc/logrotate.d/

%pre
if ! /usr/bin/id superset &>/dev/null; then
    /usr/sbin/useradd -r -d /usr/share/superset -s /bin/sh -c "superset" superset|| \
        %logmsg "Unexpected error adding user \"superset\". Aborting installation."
fi

%post
systemctl daemon-reload

%preun
systemctl stop superset

%postun
systemctl daemon-reload
if [ $1 -eq 0 ]; then
	/usr/sbin/userdel superset || %logmsg "User \"superset\" could not be deleted."
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,superset,superset,-)
/usr/share/superset/
/run/superset/

%defattr(-,root,root,-)
/etc/sysconfig/*
/usr/lib/systemd/system/*
/usr/bin/*
/etc/logrotate.d/*

%changelog
* Tue Jul 23 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.28.1-1
- Initial release. Spec is based on https://github.com/xiaomatech/superset/blob/master/superset.spec


