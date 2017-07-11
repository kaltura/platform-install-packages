%global npm_name util
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 0.10.3
Release: 1
Summary: Node
License: MIT
URL: https://github.com/defunctzombie/node-util
Source0: http://registry.npmjs.org/util/-/util-0.10.3.tgz
Source1: http://registry.npmjs.org/inherits/-/inherits-2.0.1.tgz
Source2: util-0.10.3-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(util) = 0.10.3
Provides: bundled-npm(inherits) = 2.0.1
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
cd node_modules/util
cp -pfr .npmignore .travis.yml .zuul.yml LICENSE README.md package.json support test util.js node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf README.md LICENSE ../../
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
* Tue Jul 11 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 0.10.3-1
- First release 
