%global npm_name cron
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 1.2.1
Release: 1
Summary: Cron jobs for your node
License: MIT
URL: http://github.com/ncb000gt/node-cron/issues
Source0: http://registry.npmjs.org/cron/-/cron-1.2.1.tgz
Source1: http://registry.npmjs.org/moment-timezone/-/moment-timezone-0.5.13.tgz
Source2: http://registry.npmjs.org/moment/-/moment-2.18.1.tgz
Source3: cron-1.2.1-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(cron) = 1.2.1
Provides: bundled-npm(moment-timezone) = 0.5.13
Provides: bundled-npm(moment) = 2.18.1
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

%setup -T -q -a 3 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd node_modules/cron
cp -pfr .eslintrc.json .npmignore .travis.yml Makefile README.md bower.json lib package.json test.js tests wercker.yml node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf README.md  ../../
# If any binaries are included, symlink them to bindir here


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}

%doc 
%doc README.md

%changelog
* Tue Jul 11 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 1.2.1-1
- First release 
