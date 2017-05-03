%global npm_name config
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 1.25.1
Release: 1
Summary: Configuration control for production node deployments
License: MIT
URL: http://lorenwest.github.com/node-config
Source0: http://registry.npmjs.org/config/-/config-1.25.1.tgz
Source1: http://registry.npmjs.org/json5/-/json5-0.4.0.tgz
Source2: config-1.25.1-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(config) = 1.25.1
Provides: bundled-npm(json5) = 0.4.0
AutoReq: no 
AutoProv: no 


%define npm_cache_dir /tmp/npm_cache_%{name}-%{version}-%{release}

%description
%{summary}

%prep
mkdir -p %{npm_cache_dir}
for tgz in %{sources}; do
  echo $tgz | grep -q registry.npmjs.org || npm cache add --cache ./%{npm_cache_dir} $tgz
done

%setup -T -q -a 2 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd node_modules/config
cp -pfr .npmignore .travis.yml History.md LICENSE README.md defer.js lib package.json raw.js tools node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf History.md README.md LICENSE ../../
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
%doc History.md
%doc README.md

%changelog
* Thu Apr 27 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 1.25.1-1
- First release 
