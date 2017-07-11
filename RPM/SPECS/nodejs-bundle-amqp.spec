%global npm_name amqp
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 0.2.6
Release: 1
Summary: AMQP driver for node
License: FIXME
URL: http://github.com/postwait/node-amqp/issues
Source0: http://registry.npmjs.org/amqp/-/amqp-0.2.6.tgz
Source1: http://registry.npmjs.org/lodash/-/lodash-4.17.4.tgz
Source2: amqp-0.2.6-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(amqp) = 0.2.6
Provides: bundled-npm(lodash) = 4.17.4
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
cd node_modules/amqp
cp -pfr .jshintrc .npmignore .travis.yml CONTRIBUTING.md History.md LICENSE-MIT Makefile README.md amqp-0-9-1-rabbit.xml amqp-0-9-1.xml amqp.js jspack.js lib package.json qparser.rb runTests.sh test test2 test2src util node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf CONTRIBUTING.md History.md README.md LICENSE-MIT ../../
# If any binaries are included, symlink them to bindir here


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}

%doc LICENSE-MIT
%doc CONTRIBUTING.md
%doc History.md
%doc README.md

%changelog
* Tue Jul 11 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 0.2.6-1
- First release 
