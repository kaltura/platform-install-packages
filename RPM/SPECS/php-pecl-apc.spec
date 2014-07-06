%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)
%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%define pecl_name APC

Name:           php-pecl-apc
Version:        3.1.9
Release:        1
Summary:        Bindings for the libapc library

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/apc
Source0:        http://pecl.php.net/get/APC-%{version}.tgz
Source1:        PHP-LICENSE-3.01


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  php-devel php-pear
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:       php-pecl(apc) = %{version}

%if %{?php_zend_api}0
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%else
# for EL-5
Requires:       php-api = %{php_apiver}
%endif


%description
APC is a free, open, and robust framework for caching and optimizing PHP intermediate code.

%package devel
Summary: Header files and static library for the ffmpeg codec library
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
Header files for APC

%prep
%setup -q -n APC-%{version}



%{__install} -m 644 -c %{SOURCE1} LICENSE




%build
phpize
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# install config file
%{__install} -d %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/apc.ini << 'EOF'
; Enable apc extension module
extension=apc.so
EOF



%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE CHANGELOG
%config(noreplace) %{_sysconfdir}/php.d/apc.ini
%{php_extdir}/apc.so

%files devel
/usr/include/php/ext/apc/apc_serializer.h

%changelog
* Sun Jul 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 3.1.9-1
- For PHP 5_4

