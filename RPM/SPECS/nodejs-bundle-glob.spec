%global npm_name glob
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 7.0.5
Release: 1
Summary: a little globber
License: ISC
URL: git://github.com/isaacs/node-glob.git
Source0: http://registry.npmjs.org/glob/-/glob-7.0.5.tgz
Source1: http://registry.npmjs.org/minimatch/-/minimatch-3.0.4.tgz
Source2: http://registry.npmjs.org/inflight/-/inflight-1.0.6.tgz
Source3: http://registry.npmjs.org/inherits/-/inherits-2.0.3.tgz
Source4: http://registry.npmjs.org/fs.realpath/-/fs.realpath-1.0.0.tgz
Source5: http://registry.npmjs.org/once/-/once-1.4.0.tgz
Source6: http://registry.npmjs.org/path-is-absolute/-/path-is-absolute-1.0.1.tgz
Source7: http://registry.npmjs.org/brace-expansion/-/brace-expansion-1.1.8.tgz
Source8: http://registry.npmjs.org/wrappy/-/wrappy-1.0.2.tgz
Source9: http://registry.npmjs.org/balanced-match/-/balanced-match-1.0.0.tgz
Source10: http://registry.npmjs.org/concat-map/-/concat-map-0.0.1.tgz
Source11: glob-7.0.5-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(glob) = 7.0.5
Provides: bundled-npm(minimatch) = 3.0.4
Provides: bundled-npm(inflight) = 1.0.6
Provides: bundled-npm(inherits) = 2.0.3
Provides: bundled-npm(fs.realpath) = 1.0.0
Provides: bundled-npm(once) = 1.4.0
Provides: bundled-npm(path-is-absolute) = 1.0.1
Provides: bundled-npm(brace-expansion) = 1.1.8
Provides: bundled-npm(wrappy) = 1.0.2
Provides: bundled-npm(balanced-match) = 1.0.0
Provides: bundled-npm(concat-map) = 0.0.1
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

%setup -T -q -a 11 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd node_modules/glob
cp -pfr LICENSE README.md changelog.md common.js glob.js package.json sync.js node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf README.md changelog.md LICENSE ../../
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
%doc changelog.md

%changelog
* Thu Nov 2 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 7.0.5-1
- First release 
