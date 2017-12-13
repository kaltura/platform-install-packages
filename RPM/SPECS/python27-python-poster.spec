%define python27_sitelib %(python -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib())")
%{!?py2ver: %global py2ver %(python -c "import sys ; print sys.version[:3]")}

%global modname poster

Name:           python27-python-%{modname}
Summary:        Streaming HTTP uploads and multipart/form-data encoding
Version:        0.8.1
Release:        1
License:        MIT
Group:          System Environment/Libraries
URL:            http://atlee.ca/software/poster
Source0:        http://pypi.python.org/packages/source/p/%{modname}/%{modname}-%{version}.tar.gz


BuildArch:      noarch
BuildRequires:  python27-scldevel
BuildRequires:  python27-python-setuptools
#BuildRequires:  setuptools
Requires: python27-python


%description
The modules in the Python standard library don't provide a way to upload large files 
via HTTP without having to load the entire file into memory first.
poster provides support for both streaming POST requests as well as multipart/form-data 
encoding of string or file parameters.

%prep
%setup -q -n %{modname}-%{version}



%build
python setup.py build bdist_egg


%install

%{__mkdir} -p %{buildroot}%{python27_sitelib}
easy_install-%{py2ver} -m --prefix %{buildroot}/opt/rh/python27/root/usr/ dist/*.egg
%{__chmod} 0644 %{buildroot}%{python27_sitelib}/%{modname}-%{version}-*.egg

%check
#python setup.py test


%files
%{python27_sitelib}/%{modname}-%{version}-*.egg


%changelog
* Wed Dec 13 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 0.8.1-1
- First release

