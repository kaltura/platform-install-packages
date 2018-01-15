%define python27_sitelib %(python -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib())")
%{!?py2ver: %global py2ver %(python -c "import sys ; print sys.version[:3]")}
%filter_from_requires s|^python(abi)|python27-python(abi)|
%filter_setup

%global modname iso8601

Name:           python27-python-%{modname}
Summary:        Simple module to parse ISO 8601 dates
Version:        0.1.12
Release:        2
License:        MIT
Group:          System Environment/Libraries
URL:            https://github.com/globocom/m3u8
Source0:        %{modname}-%{version}.tar.gz


BuildArch:      noarch
BuildRequires:  python27-scldevel
BuildRequires:  python27-python-setuptools
#BuildRequires:  setuptools
Requires: python27-python


%description
Simple module to parse ISO 8601 dates

%prep
%setup -q -n %{modname}-%{version}

%build
python setup.py build 


%install
%{__mkdir} -p %{buildroot}%{python27_sitelib}/%{modname}
python setup.py install --skip-build --root %{buildroot}
cp -p %{modname}/__init__.py %{buildroot}%{python27_sitelib}/%{modname}/
ls -al %{buildroot}%{python27_sitelib}/%{modname}/


%files
%{python27_sitelib}/%{modname}/*
%{python27_sitelib}/%{modname}-%{version}-py2.7.egg-info


%changelog
* Wed Dec 13 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 0.1.12-1
- First release

