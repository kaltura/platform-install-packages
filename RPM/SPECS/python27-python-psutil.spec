%define python27_sitelib %(python -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")
%{!?py2ver: %global py2ver %(python -c "import sys ; print sys.version[:3]")}
%filter_from_requires s|^python(abi)|python27-python(abi)|
%filter_setup

%global modname psutil

Name:           python27-python-%{modname}
Summary:        Cross-platform lib for process and system monitoring in Python
Version:        5.4.2
Release:        3
License:        MIT
Group:          System Environment/Libraries
URL:            https://github.com/globocom/m3u8
Source0:        %{modname}-%{version}.tar.gz


BuildRequires:  python27-scldevel
BuildRequires:  python27-python-setuptools
#BuildRequires:  setuptools
Requires: python27-python


%description
psutil (process and system utilities) is a cross-platform library for retrieving information on 
running processes and system utilization (CPU, memory, disks, network, sensors) in Python. 
It is useful mainly for system monitoring, profiling and limiting process resources.

%prep
%setup -q -n %{modname}-%{version}


%build
python setup.py build 


%install
%{__mkdir} -p %{buildroot}%{python27_sitelib}/%{modname}
python setup.py install --skip-build --root %{buildroot}
cp -p %{modname}/__init__.py %{buildroot}%{python27_sitelib}/%{modname}/


%files
#%{python27_sitelib}/tests/*
%{python27_sitelib}/%{modname}/*
%{python27_sitelib}/%{modname}-%{version}-py2.7.egg-info


%changelog
* Wed Dec 13 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 5.4.2-1
- First release

