%define php_modules mcrypt
%define extensiondir %(php-config --extension-dir 2>/dev/null || echo "undefined")
%define php_api %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

%define real_name php

Summary: PHP Mcrypt extension. 
Name: php-mcrypt
Version: 5.3.3
Release: 4 
License: The PHP License
Group: Development/Languages
URL: http://www.php.net/

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc. 

Source: http://www.php.net/distributions/php-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php-api = %{php_api}
%{?_with_mcrypt:BuildRequires: libmcrypt-devel}


BuildRequires: php-devel = %{version}
Provides: php-mcrypt 
Requires: libmcrypt
BuildRequires: libmcrypt-devel
%description
PHP is an HTML-embedded scripting language.

This package contains the Mcrypt PHP extension, which
has not been included in the basic PHP package for CentOS/RHEL/Fedora.

%prep
%setup -qn %{real_name}-%{version}

%build
export CFLAGS="%{optflags} -fno-strict-aliasing -Wno-pointer-sign"

for mod in %{php_modules}; do
    pushd ext/$mod/
    rm -rf tests/

    phpize
    %configure \
        --with-libdir="%{_lib}" \
        --with-mcrypt \

    # cause libtool to avoid passing -rpath when linking
    # (this hack is well-known as "libtool rpath workaround")
    sed -i 's|^hardcode_libdir_flag_spec|hardcode_libdir_flag_spec=" -D__LIBTOOL_IS_A_FOOL__ "|' libtool

    %{__make} %{?_smp_mflags}
    popd
done

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{extensiondir}
%{__install} -d %{buildroot}%{_sysconfdir}/php.d/
for module in %{php_modules}; do
    %{__install} -Dp -m0755 ext/$module/modules/*.so %{buildroot}%{extensiondir}
    cat <<EOF >%{buildroot}%{_sysconfdir}/php.d/$module.ini
; Enable $module extension module
extension=$module.so
EOF
done

%clean
%{__rm} -rf %{buildroot}

%files -n php-mcrypt
%defattr(-, root, root, 0775)
%config(noreplace) %{_sysconfdir}/php.d/mcrypt.ini
%{extensiondir}/mcrypt.so


%changelog
* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 5.3.3-3
- It does not PROVIDE libmcrypt, it requires it.

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 5.3.3-2
- Quiet setup and fixed extension directive.

* Sun Jan 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 5.3.3-1
- Initial package.
