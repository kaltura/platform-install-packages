%global npm_name once
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 1.4.0
Release: 1
Summary: Run a function exactly one time
License: ISC
URL: git://github.com/isaacs/once
Source0: http://registry.npmjs.org/%{npm_name}/-/%{npm_name}-%{version}.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

%{?nodejs_find_provides_and_requires}

%define npm_cache_dir /tmp/npm_cache_%{name}-%{version}-%{release}

%description
%{summary}

%prep
%setup -q -n package

%build
%nodejs_symlink_deps --build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr LICENSE README.md once.js package.json %{buildroot}%{nodejs_sitelib}/%{npm_name}
# If any binaries are included, symlink them to bindir here


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}

%doc LICENSE
%doc README.md

%changelog
* Tue Apr 10 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 1.4.0-1
- First release 
