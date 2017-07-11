%global npm_name cluster
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 0.7.7
Release: 1
Summary: extensible multi-core server manager
License: FIXME
URL: http://learnboost.github.com/cluster
Source0: http://registry.npmjs.org/cluster/-/cluster-0.7.7.tgz
Source1: http://registry.npmjs.org/mkdirp/-/mkdirp-0.5.1.tgz
Source2: http://registry.npmjs.org/log/-/log-1.4.0.tgz
Source3: http://registry.npmjs.org/minimist/-/minimist-0.0.8.tgz
Source4: cluster-0.7.7-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(cluster) = 0.7.7
Provides: bundled-npm(mkdirp) = 0.5.1
Provides: bundled-npm(log) = 1.4.0
Provides: bundled-npm(minimist) = 0.0.8
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

%setup -T -q -a 4 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd node_modules/cluster
cp -pfr .gitmodules .npmignore History.md LICENSE Makefile Readme.md docs examples index.js lib nohup.out package.json test node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf History.md Readme.md LICENSE ../../
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
%doc Readme.md

%changelog
* Wed Jun 21 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 0.7.7-1
- First release 
