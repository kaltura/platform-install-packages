# Available build options, you will need rpm-build >= 4.0.3 for this to work.
# Example: rpmbuild -ba --with email jam.spec
#
#  Storage Options
#  ===============
#  --with email
#  --with files
#  --with snmp
#  --with spread
#  --with stomp
#  --with tokyo
#  --with zeromq2
#  --with elasticsearch

#
# These setup the storage backends to off by default
#
%bcond_with email
%bcond_with files
%bcond_with snmp
%bcond_with spread
%bcond_with stomp
%bcond_with tokyo
%bcond_with zeromq2
%bcond_with elasticsearch


Name:      php-jam
Version:   1.0.0
Release:   2
Packager:  Jess Portnoy <jess.portnoy@kaltura.com>
Summary:   PHP monitoring system that supports storing PHP errors (events) into different storage backends. 
License:   PHP License
Group:     Web/Applications
URL:       http://github.com/mkoppanen/php-jam
Source:    jam-%{version}.tgz
Prefix:    %{_prefix}
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel, make, gcc, /usr/bin/phpize, libuuid-devel

%description
Monitoring extension for PHP

%package devel
Summary: Development headers for %{name}
Group:   Web/Applications
Requires: %{name} = %{version}-%{release}

%description devel
Development headers for %{name}

### Conditional build for email
%if %{with email}
%package email
Summary: Email storage engine for %{name}
Group:   Web/Applications
Requires: %{name} = %{version}-%{release}

%description email
%{name} backend implementation which sends email.
%endif

### Conditional build for files
%if %{with files}
%package files
Summary: File storage engine for %{name}
Group:   Web/Applications
Requires: %{name} = %{version}-%{release}

%description files
%{name} backend implementation which stores events in files.
%endif

### Conditional build for snmp
%if %{with snmp}
%package snmp
Summary: SNMP storage engine for %{name}
Group:   Web/Applications
Requires: %{name} = %{version}-%{release}

%description snmp
%{name} backend implementation which sends events as SNMP traps.
%endif

### Conditional build for spread
%if %{with spread}
%package spread
Summary: Spread storage engine for %{name}
Group:   Web/Applications
Requires: %{name} = %{version}-%{release}

%description Spread
%{name} backend implementation which sends events via spread.
%endif

### Conditional build for stomp
%if %{with stomp}
%package stomp
Summary: Stomp storage engine for %{name}
Group:   Web/Applications
Requires: %{name} = %{version}-%{release}

%description stomp
%{name} backend implementation which sends events via stomp.
%endif

### Conditional build for zeromq2
%if %{with zeromq2}
%package zeromq2
Summary: zeromq2 storage engine for %{name}
Group:   Web/Applications
Requires: %{name} = %{version}-%{release}

%description zeromq2
%{name} backend implementation which sends events via zeromq2.
%endif

### Conditional build for zeromq2
%if %{with elasticsearch}
%package elasticsearch
Summary: Elasticsearch storage engine for %{name}
Group:   Web/Applications
Requires: %{name} = %{version}-%{release}
BuildRequires: php-devel, make, gcc, /usr/bin/phpize, libcurl-devel, json-c-devel

%description elasticsearch
%{name} backend implementation which sends events to elasticsearch.
%endif
%prep
%setup -q -n jam-%{version}

%build
/usr/bin/phpize && %configure -C && %{__make} %{?_smp_mflags}

# Clean the buildroot so that it does not contain any stuff from previous builds
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

# Install the extension
%{__make} install INSTALL_ROOT=%{buildroot}

# Create the ini location
%{__mkdir} -p %{buildroot}/etc/php.d

# Preliminary extension ini
echo "extension=jam.so" > %{buildroot}/%{_sysconfdir}/php.d/jam.ini
echo ';jam.storage_modules="elasticsearch,email"' >> %{buildroot}/%{_sysconfdir}/php.d/jam.ini
echo ';jam.appname="JaM"' >> %{buildroot}/%{_sysconfdir}/php.d/jam.ini
echo ';You can determine what errors each backend will store, if you uncomment this, only E_ERROR events will be emailed' >> %{buildroot}/%{_sysconfdir}/php.d/jam.ini
echo ";jam.module_error_reporting='email=E_ERROR'" >> %{buildroot}/%{_sysconfdir}/php.d/jam.ini

%if %{with email}
	pushd storage/email
	/usr/bin/phpize && cp ../../config.cache . && %configure -C && %{__make} %{?_smp_mflags}
	%{__make} install INSTALL_ROOT=%{buildroot}
	popd
	echo "extension=jam_email.so" > %{buildroot}/%{_sysconfdir}/php.d/jam_email.ini
	echo ';jam_email.to_address="you@exmaple.com"' >> %{buildroot}/%{_sysconfdir}/php.d/jam_email.ini
%endif

%if %{with files}
	pushd storage/files
	/usr/bin/phpize && cp ../../config.cache . && %configure -C && %{__make} %{?_smp_mflags}
	%{__make} install INSTALL_ROOT=%{buildroot}
	popd
	echo "extension=jam_files.so" > %{buildroot}/%{_sysconfdir}/php.d/jam_files.ini
	echo ';jam_files.storage_path="/path/to/storage"' >> %{buildroot}/%{_sysconfdir}/php.d/jam_files.ini
%endif

%if %{with snmp}
	pushd storage/snmp
	/usr/bin/phpize && cp ../../config.cache . && %configure -C && %{__make} %{?_smp_mflags}
	%{__make} install INSTALL_ROOT=%{buildroot}
	popd
%endif

%if %{with spread}
	pushd storage/spread
	/usr/bin/phpize && cp ../../config.cache . && %configure -C && %{__make} %{?_smp_mflags}
	%{__make} install INSTALL_ROOT=%{buildroot}
	popd
%endif

%if %{with stomp}
	pushd storage/stomp
	/usr/bin/phpize && cp ../../config.cache . && %configure -C && %{__make} %{?_smp_mflags}
	%{__make} install INSTALL_ROOT=%{buildroot}
	popd
%endif

%if %{with elasticsearch}
	pushd storage/elasticsearch
	/usr/bin/phpize && cp ../../config.cache . && %configure -C && %{__make} %{?_smp_mflags}
	%{__make} install INSTALL_ROOT=%{buildroot}
	popd
	echo "extension=jam_elasticsearch.so" > %{buildroot}/%{_sysconfdir}/php.d/jam_elasticsearch.ini
	echo ';jam_elasticsearch.host="http://localhost:9200/jam/log"' >> %{buildroot}/%{_sysconfdir}/php.d/jam_elasticsearch.ini
%endif

%if %{with zeromq2}
	pushd storage/zeromq2
	/usr/bin/phpize && cp ../../config.cache . && %configure -C && %{__make} %{?_smp_mflags}
	%{__make} install INSTALL_ROOT=%{buildroot}
	popd
%endif


%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%{_libdir}/php/modules/jam.so
%{_sysconfdir}/php.d/jam.ini

%files devel
%{_includedir}/php/ext/jam/php_jam.h
%{_includedir}/php/ext/jam/php_jam_storage.h

%if %{with email}
%files email
%{_libdir}/php/modules/jam_email.so
%{_sysconfdir}/php.d/jam_email.ini
%endif

%if %{with files}
%files files
%{_libdir}/php/modules/jam_files.so
%{_sysconfdir}/php.d/jam_files.ini
%endif

%if %{with snmp}
%files snmp
%{_libdir}/php/modules/jam_snmp.so
%endif

%if %{with spread}
%files spread
%{_libdir}/php/modules/jam_spread.so
%endif

%if %{with stomp}
%files stomp
%{_libdir}/php/modules/jam_stomp.so
%endif

%if %{with elasticsearch}
%files elasticsearch
%{_libdir}/php/modules/jam_elasticsearch.so
%{_sysconfdir}/php.d/jam_elasticsearch.ini
%endif

%if %{with zeromq2}
%files zeromq2
%{_libdir}/php/modules/jam_zeromq2.so
%endif



%changelog
* Tue Dec 29 2015 Jess Portnoy <jess.portnoy@kaltura.com>
 - First JaM build.
