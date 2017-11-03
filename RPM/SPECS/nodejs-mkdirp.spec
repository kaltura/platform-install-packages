%global npm_name mkdirp
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 0.5.1
Release: 1
Summary: Recursively mkdir, like `mkdir -p`
License: MIT
URL: https://github.com/substack/node-mkdirp.git
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
cp -pfr .travis.yml LICENSE bin examples index.js package.json readme.markdown test %{buildroot}%{nodejs_sitelib}/%{npm_name}
# If any binaries are included, symlink them to bindir here
mkdir -p %{buildroot}%{nodejs_sitelib}/${npm_name}/bin 
mkdir -p %{buildroot}%{_bindir}/ 
install -p -D -m0755 bin/cmd.js %{buildroot}%{nodejs_sitelib}/%{npm_name}/bin/cmd.js
ln -sf %{nodejs_sitelib}/%{npm_name}/bin/cmd.js %{buildroot}%{_bindir}/cmd.js


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}
%{_bindir}/cmd.js
%doc LICENSE
%doc readme.markdown

%changelog
* Thu Nov 2 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 0.5.1-1
- First release 
