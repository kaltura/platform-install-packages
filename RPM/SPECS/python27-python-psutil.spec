%define python27_sitelib %(python -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib())")
%{!?py2ver: %global py2ver %(python -c "import sys ; print sys.version[:3]")}

%global modname psutil

Name:           python27-python-%{modname}
Summary:        Cross-platform lib for process and system monitoring in Python
Version:        5.4.2
Release:        1
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
python setup.py build bdist_egg


%install

%{__mkdir} -p %{buildroot}%{python27_sitelib}
easy_install-%{py2ver} -m --prefix %{buildroot}/opt/rh/python27/root/usr/ dist/*.egg
%{__chmod} 0644 %{buildroot}%{python27_sitelib}/%{modname}-%{version}-*.egg/%{modname}/*.py

%check
#python setup.py test


%files
%{python27_sitelib}/%{modname}-%{version}-*.egg


%changelog
* Wed Dec 13 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 5.4.2-1
- First release

