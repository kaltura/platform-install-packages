%define python27_sitelib %(python -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")
%{!?py2ver: %global py2ver %(python -c "import sys ; print sys.version[:3]")}
%filter_from_requires s|python(abi)|python27-python(abi)|g
%filter_setup
%global modname pycrypto

Name:           python27-python-%{modname}
Summary:        Cryptographic modules for Python.
Version:        2.6.1
Release:        2
License:        Public Domain
Group:          System Environment/Libraries
URL:            http://www.pycrypto.org
Source0:        %{modname}-%{version}.tar.gz


BuildRequires:  python27-scldevel
BuildRequires:  python27-python-setuptools
#BuildRequires:  setuptools
Requires: python27-python


%description
This is a collection of both secure hash functions (such as SHA256 and RIPEMD160), 
and various encryption algorithms (AES, DES, RSA, ElGamal, etc.). 

%prep
%setup -q -n %{modname}-%{version}



%build
python setup.py build


%install

%{__mkdir} -p %{buildroot}%{python27_sitelib}
python setup.py install --prefix %{buildroot}/opt/rh/python27/root/usr/

%check
#python setup.py test


%files
%{python27_sitelib}/Crypto
%{python27_sitelib}/%{modname}-%{version}*egg-info


%changelog
* Wed Dec 13 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 2.6.1-1
- First release

