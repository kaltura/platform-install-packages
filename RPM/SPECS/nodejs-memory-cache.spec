%global npm_name memory-cache
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 0.1.6
Release: 1
Summary: A simple in-memory cache
License: BSD-2-Clause
URL: git://github.com/ptarjan/node-cache.git
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
cp -pfr .jsbeautifyrc .jshintrc .npmignore .travis.yml LICENSE.md README.md gulpfile.js index.js package.json test.js %{buildroot}%{nodejs_sitelib}/%{npm_name}
# If any binaries are included, symlink them to bindir here


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}

%doc LICENSE.md
%doc LICENSE.md
%doc README.md

%changelog
* Thu Apr 27 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 0.1.6-1
- First release 
