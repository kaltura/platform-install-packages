%global npm_name strip-ansi
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 3.0.1
Release: 1
Summary: Strip ANSI escape codes
License: MIT
URL: FIXME
Source0: http://registry.npmjs.org/strip-ansi/-/strip-ansi-3.0.1.tgz
Source1: http://registry.npmjs.org/ansi-regex/-/ansi-regex-2.1.1.tgz
Source2: strip-ansi-3.0.1-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(strip-ansi) = 3.0.1
Provides: bundled-npm(ansi-regex) = 2.1.1
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
cd node_modules/strip-ansi
cp -pfr index.js license package.json readme.md node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf readme.md license ../../
# If any binaries are included, symlink them to bindir here


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}

%doc license
%doc readme.md

%changelog
* Tue Apr 10 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 3.0.1-1
- First release 
